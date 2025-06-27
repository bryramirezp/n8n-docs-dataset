# -*- coding: utf-8 -*-
import os
import json
import re
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# --- CONFIGURACIÓN Y CONSTANTES ---
load_dotenv()
ARCHIVO_ENTRADA = "n8n_docs_combined.md"
ARCHIVO_SALIDA_FINAL = "n8n_qa_dataset.jsonl"
ARCHIVO_SALIDA_PARCIAL = "n8n_qa_dataset_partial.jsonl"
MODELO_LLM = "gpt-4o"
TEMPERATURA = 0.0
CHUNK_SIZE = 4000
CHUNK_OVERLAP = 200

# --- PLANTILLA DE PROMPT (VALIDADA) ---
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
    Limpia la respuesta del LLM, eliminando los bloques de código Markdown
    y cualquier texto antes o después del JSON principal.
    """
    match = re.search(r'```(json)?\s*([\s\S]*?)\s*```', response_content, re.DOTALL)
    if match:
        return match.group(2).strip()
    return response_content.strip()

def pre_run_checks():
    """Verifica todas las pre-condiciones antes de gastar dinero en la API."""
    print("--- Realizando verificaciones pre-ejecución ---")
    if not os.getenv("OPENAI_API_KEY"):
        print("Error Crítico: La variable de entorno OPENAI_API_KEY no está configurada.")
        return False
    print("OK: Clave de API de OpenAI encontrada.")
    if not os.path.exists(ARCHIVO_ENTRADA):
        print(f"Error Crítico: El archivo de entrada '{ARCHIVO_ENTRADA}' no se encontró.")
        return False
    print(f"OK: Archivo de entrada '{ARCHIVO_ENTRADA}' encontrado.")
    if os.path.getsize(ARCHIVO_ENTRADA) == 0:
        print(f"Error Crítico: El archivo de entrada '{ARCHIVO_ENTRADA}' está vacío.")
        return False
    print(f"OK: Archivo de entrada no está vacío (Tamaño: {os.path.getsize(ARCHIVO_ENTRADA)} bytes).")
    print("--- Todas las verificaciones pasaron. Iniciando proceso. ---\n")
    return True

def main():
    """Función principal que orquesta todo el proceso de generación."""
    if not pre_run_checks():
        return

    print("Paso 1: Cargando y dividiendo el documento...")
    loader = UnstructuredMarkdownLoader(ARCHIVO_ENTRADA)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(docs)
    print(f"Documento dividido en {len(chunks)} fragmentos.")

    llm = ChatOpenAI(model=MODELO_LLM, temperature=TEMPERATURA)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | llm
    
    processed_indices = set()
    if os.path.exists(ARCHIVO_SALIDA_PARCIAL):
        print(f"\nSe encontró un archivo de progreso anterior '{ARCHIVO_SALIDA_PARCIAL}'. Cargando resultados...")
        with open(ARCHIVO_SALIDA_PARCIAL, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    processed_indices.add(data['chunk_index'])
                except (json.JSONDecodeError, KeyError):
                    print(f"Advertencia: Se encontró una línea malformada en el archivo parcial y se omitirá.")
        print(f"Se reanudará el proceso, omitiendo {len(processed_indices)} fragmentos ya procesados.")

    print(f"\nPaso 2: Procesando fragmentos con {MODELO_LLM}...")
    try:
        for i, chunk in enumerate(chunks):
            if i in processed_indices:
                continue

            try:
                print(f"Procesando fragmento {i + 1}/{len(chunks)}...")
                response = chain.invoke({"context": chunk.page_content})
                cleaned_content = clean_llm_response(response.content)
                generated_json = json.loads(cleaned_content)
                
                if isinstance(generated_json, list):
                    validated_items = [item for item in generated_json if 'user_question' in item and 'concise_answer' in item]
                    if validated_items:
                        with open(ARCHIVO_SALIDA_PARCIAL, "a", encoding="utf-8") as f:
                            for item in validated_items:
                                record = {'chunk_index': i, 'content': item}
                                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                        print(f" -> Éxito. Se guardaron {len(validated_items)} nuevos registros.")
                    else:
                        print(f" -> Advertencia: La lista generada no contenía objetos válidos.")
                else:
                    print(f" -> Advertencia: El resultado no era una lista. Se omite.")

            except json.JSONDecodeError:
                print(f" -> Error de Decodificación después de la limpieza. El LLM devolvió un formato inválido. Se omite el fragmento.")
            except Exception as e:
                print(f" -> Error Inesperado: {e}. Se omite el fragmento.")
    
    finally:
        print("\nProcesamiento completado o interrumpido.")
        # La copia final solo ocurre si el bucle termina sin interrupción manual (Ctrl+C)
        if 'i' in locals() and i == len(chunks) - 1:
            print("Proceso completado. Consolidando el archivo final...")
            final_data = []
            if os.path.exists(ARCHIVO_SALIDA_PARCIAL):
                with open(ARCHIVO_SALIDA_PARCIAL, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            final_data.append(json.loads(line)['content'])
                        except (json.JSONDecodeError, KeyError):
                            continue
            
            with open(ARCHIVO_SALIDA_FINAL, "w", encoding="utf-8") as f:
                for item in final_data:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")

            os.remove(ARCHIVO_SALIDA_PARCIAL)
            print(f"\n¡Proceso finalizado! Se generó el archivo final '{ARCHIVO_SALIDA_FINAL}' con {len(final_data)} registros.")
        else:
             total_registros = 0
             if os.path.exists(ARCHIVO_SALIDA_PARCIAL):
                with open(ARCHIVO_SALIDA_PARCIAL, 'r', encoding='utf-8') as f:
                    total_registros = sum(1 for line in f)
             print(f"El proceso se interrumpió. El progreso ({total_registros} registros) está guardado en '{ARCHIVO_SALIDA_PARCIAL}'.")


if __name__ == "__main__":
    main()