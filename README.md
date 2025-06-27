# n8n AI Knowledge Base

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/tu-usuario/n8n-ai-knowledge-base)
![Repo size](https://img.shields.io/github/repo-size/tu-usuario/n8n-ai-knowledge-base)

---

An open-source project that provides a high-quality, structured JSONL dataset of the entire n8n documentation, ready to be used as a knowledge base for AI applications and RAG (Retrieval-Augmented Generation) systems. This repository includes the Python script used to generate and maintain the dataset, designed to transform technical markdown into a clean, machine-readable format.

## The Problem

The official n8n documentation is comprehensive but exists as a large collection of interconnected web pages. This format is ideal for human reading but presents a significant challenge for AI systems. Feeding documentation to an LLM requires a consolidated, clean, and structured format to avoid errors and get precise, factual responses. As seen in the n8n community, many users are looking for an easy way to use the documentation to power their AI-driven workflow builders.

## The Solution

This project solves that problem by providing two key assets:

1.  **A Pre-processed, Structured Dataset (`n8n_qa_dataset.jsonl`):** A ready-to-use JSONL file containing the entire n8n documentation converted into a list of structured objects. Each object contains not just a question and answer, but also metadata, keywords, and structured data like code blocks and parameters.

2.  **A Robust Generation Script (`generar_dataset.py`):** The Python script used to create the dataset. It's designed to be resilient, with error handling and partial-save features, allowing advanced users to regenerate the dataset from updated documentation in the future.

## Getting Started

You can use this project in two primary ways, depending on your needs.

### Use Case 1: I just want the data for my AI Assistant

This is the fastest way to get started. You don't need to run any code.

1.  **Download the Dataset:** Go to the root of this repository and download the `n8n_qa_dataset.jsonl` file.
2.  **Upload to your AI Platform:** Upload this file to the "Knowledge" or "Documents" section of your AI tool (e.g., OpenAI's Custom GPTs, a custom RAG pipeline using LangChain, etc.).
3.  **Use a Strong System Prompt:** When configuring your AI assistant, use precise instructions to ensure it relies on the provided knowledge.

    **Example System Prompt for a Custom GPT:**
    > Your role is 'n8n Expert Technical Assistant'. Your only source of truth is the knowledge provided in the uploaded files. When a user asks a question about n8n, you must search your knowledge base for the most relevant structured record. Your answer should be based exclusively on the `concise_answer` and `structured_data` from that record. If the information is not in the knowledge base, you must respond exactly with: "I could not find a precise answer to that question in my knowledge base." You are forbidden from using your general pre-trained knowledge about n8n.

### Use Case 2: I want to run or modify the generation script

This is for advanced users who want to regenerate the dataset from a different source document or with modified parameters.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/tu-usuario/n8n-ai-knowledge-base.git](https://github.com/tu-usuario/n8n-ai-knowledge-base.git)
    cd n8n-ai-knowledge-base
    ```

2.  **Set up the environment:**
    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate it (Windows)
    .\venv\Scripts\Activate.ps1
    
    # Activate it (macOS/Linux)
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your API Key:**
    * Create a file named `.env` in the root of the project.
    * Add your OpenAI API key to it: `OPENAI_API_KEY="sk-..."`

5.  **Provide the Source Document:**
    * Place your consolidated markdown file named `n8n_docs_combined.md` in the root of the project.

6.  **Run the script:**
    ```bash
    python generar_dataset.py
    ```

## Dataset Structure

Each line in the `n8n_qa_dataset.jsonl` file is a JSON object with the following structure:

```json
{
  "content_type": "The category of the content (e.g., 'Node Reference', 'How-To Guide').",
  "section_title": "The original section title from the documentation.",
  "user_question": "A realistic question a user might ask.",
  "concise_answer": "A direct, easy-to-understand answer.",
  "structured_data": {
    "key_parameters": [
      {"name": "Parameter Name", "description": "What the parameter does.", "example": "Example value"}
    ],
    "code_block": "A relevant block of code, if present."
  },
  "keywords": ["list", "of", "relevant", "keywords"]
}
