# -*- coding: utf-8 -*-
import os
import json
import re
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# --- CONFIGURATION AND CONSTANTS ---
load_dotenv()
INPUT_FILE = "n8n_docs_combined.md"
FINAL_OUTPUT_FILE = "n8n_qa_dataset.jsonl"
PARTIAL_OUTPUT_FILE = "n8n_qa_dataset_partial.jsonl"
LLM_MODEL = "gpt-4o"
TEMPERATURE = 0.0
CHUNK_SIZE = 4000
CHUNK_OVERLAP = 200

# --- VALIDATED PROMPT TEMPLATE ---
PROMPT_TEMPLATE = """
Act as an expert data engineer specializing in creating high-quality datasets to feed RAG (Retrieval-Augmented Generation) systems. Your mission is to process snippets of n8n's technical documentation and transform them into structured, self-contained JSON objects.

For each relevant piece of information in the provided text, generate a JSON object that strictly follows this structure. The output MUST be a JSON list of objects.
{{
  "content_type": "(String) Classify the content. Options: 'General Concept', 'Node Reference', 'How-To Guide', 'Code Example', 'Configuration'.",
  "section_title": "(String) The title or header from the documentation section where you extracted the information.",
  "user_question": "(String) Formulate a clear and direct question that a real user would ask to find this information.",
  "concise_answer": "(String) Provide a direct and summary answer to the question. It should be an easy-to-understand paragraph.",
  "structured_data": {{
    "key_parameters": [
      {{"name": "(String) Name of the parameter, field, or setting.", "description": "(String) Explanation of what it does.", "example": "(String or Null) An example value."}}
    ] or null,
    "code_block": "(String or Null) If there is a relevant code block, include it here exactly as is, preserving all syntax, or null if not applicable."
  }},
  "keywords": ["(List of Strings) A list of 3 to 5 relevant keywords to facilitate searching."]
}}

CRITICAL RULES:
1.  **Extract "Hard Data":** Pay special attention to extracting parameter tables, code blocks, default values, and configuration examples. These must go into the "structured_data" field.
2.  **Do Not Invent Information:** If a field within the structure does not apply to the text snippet (e.g., no code is present), its value MUST be `null`.
3.  **JSON-Only Output:** Your entire output must be a valid list of JSON objects: `[ {{ ... }}, {{ ... }} ]`. Do not include any introductory text, explanations, or conclusions. Your response begins with `[` and ends with `]`.

--- TEXT TO PROCESS: ---
{context}
---
"""

def clean_llm_response(response_content):
    """
    Cleans the LLM's response by removing Markdown code blocks
    and any surrounding text before or after the main JSON content.
    """
    match = re.search(r'```(json)?\s*([\s\S]*?)\s*```', response_content, re.DOTALL)
    if match:
        return match.group(2).strip()
    return response_content.strip()

def pre_run_checks():
    """Verifies all preconditions before spending money on the API."""
    print("--- Performing pre-run checks ---")
    if not os.getenv("OPENAI_API_KEY"):
        print("Critical Error: OPENAI_API_KEY environment variable is not set.")
        return False
    print("OK: OpenAI API Key found.")
    if not os.path.exists(INPUT_FILE):
        print(f"Critical Error: Input file '{INPUT_FILE}' not found.")
        return False
    print(f"OK: Input file '{INPUT_FILE}' found.")
    if os.path.getsize(INPUT_FILE) == 0:
        print(f"Critical Error: Input file '{INPUT_FILE}' is empty.")
        return False
    print(f"OK: Input file is not empty (Size: {os.path.getsize(INPUT_FILE)} bytes).")
    print("--- All checks passed. Starting process. ---\n")
    return True

def main():
    """Main function that orchestrates the entire generation process."""
    if not pre_run_checks():
        return

    print("Step 1: Loading and splitting the document...")
    loader = UnstructuredMarkdownLoader(INPUT_FILE)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(docs)
    print(f"Document split into {len(chunks)} chunks.")

    llm = ChatOpenAI(model=LLM_MODEL, temperature=TEMPERATURE)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | llm
    
    processed_indices = set()
    if os.path.exists(PARTIAL_OUTPUT_FILE):
        print(f"\nFound previous progress file '{PARTIAL_OUTPUT_FILE}'. Loading results...")
        with open(PARTIAL_OUTPUT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    processed_indices.add(data['chunk_index'])
                except (json.JSONDecodeError, KeyError):
                    print(f"Warning: Malformed line found in partial file, skipping.")
        print(f"Resuming process, skipping {len(processed_indices)} already processed chunks.")

    print(f"\nStep 2: Processing chunks with {LLM_MODEL}...")
    try:
        for i, chunk in enumerate(chunks):
            if i in processed_indices:
                continue

            try:
                print(f"Processing chunk {i + 1}/{len(chunks)}...")
                response = chain.invoke({"context": chunk.page_content})
                cleaned_content = clean_llm_response(response.content)
                generated_json = json.loads(cleaned_content)
                
                if isinstance(generated_json, list):
                    validated_items = [item for item in generated_json if 'user_question' in item and 'concise_answer' in item]
                    if validated_items:
                        with open(PARTIAL_OUTPUT_FILE, "a", encoding="utf-8") as f:
                            for item in validated_items:
                                record = {'chunk_index': i, 'content': item}
                                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                        print(f" -> Success. Saved {len(validated_items)} new records.")
                    else:
                        print(f" -> Warning: The generated list did not contain valid objects.")
                else:
                    print(f" -> Warning: The result was not a list. Skipping.")

            except json.JSONDecodeError:
                print(f" -> Decoding Error after cleaning. LLM returned invalid format. Skipping chunk.")
            except Exception as e:
                print(f" -> Unexpected Error: {e}. Skipping chunk.")
    
    finally:
        print("\nProcessing finished or interrupted.")
        if 'i' in locals() and i == len(chunks) - 1:
            print("Process completed. Consolidating the final file...")
            final_data = []
            if os.path.exists(PARTIAL_OUTPUT_FILE):
                with open(PARTIAL_OUTPUT_FILE, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            final_data.append(json.loads(line)['content'])
                        except (json.JSONDecodeError, KeyError):
                            continue
            
            with open(FINAL_OUTPUT_FILE, "w", encoding="utf-8") as f:
                for item in final_data:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")

            os.remove(PARTIAL_OUTPUT_FILE)
            print(f"\nProcess finished! Final file '{FINAL_OUTPUT_FILE}' was generated with {len(final_data)} records.")
        else:
             total_records = 0
             if os.path.exists(PARTIAL_OUTPUT_FILE):
                with open(PARTIAL_OUTPUT_FILE, 'r', encoding='utf-8') as f:
                    total_records = sum(1 for line in f)
             print(f"Process was interrupted. Current progress ({total_records} records) is saved in '{PARTIAL_OUTPUT_FILE}'.")


if __name__ == "__main__":
    main()