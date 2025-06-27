# n8n Docs Dataset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/bryramirezp/n8n-docs-dataset/blob/main/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/bryramirezp/n8n-docs-dataset)](https://github.com/bryramirezp/n8n-docs-dataset/commits/main)
[![GitHub repo size](https://img.shields.io/github/repo-size/bryramirezp/n8n-docs-dataset)](https://github.com/bryramirezp/n8n-docs-dataset)

A high-quality, structured JSONL dataset of the n8n documentation, optimized for AI applications and RAG (Retrieval-Augmented Generation) systems.

This repository provides both the pre-processed dataset and the Python script used to generate it, allowing for immediate use and future maintenance.

## Project Status

| Metric | Value |
| :--- | :--- |
| **Total Records** | 716 |
| **Source Docs Date** | `2025-06-08` |
| **Source File Size** | `3.77 MB` |
| **Repository Size** | `26.1 MB` |
| **Default LLM** | `gpt-4o` |

---

## Quick Start: Using the Dataset

This path is for users who want to use the dataset immediately without running any code.

1.  **Download the Dataset:** From the root of this repository, download the `n8n_qa_dataset.jsonl` file.
2.  **Upload to your AI Platform:** Upload this file directly to the "Knowledge" section of your chosen AI tool (e.g., [OpenAI's Custom GPTs](https://chat.openai.com/gpts/editor), a custom RAG pipeline, etc.).
3.  **Use a Strong System Prompt:** To ensure your assistant relies on this high-quality data, configure it with precise instructions.

    > **Example System Prompt:**
    >
    > You are an 'n8n Expert Technical Assistant'. Your only source of truth is the knowledge provided in the uploaded files. Your answers must be based exclusively on the `concise_answer` and `structured_data` from the records you find. If the information is not in your knowledge base, you must state: "I could not find a precise answer to that question in my knowledge base." You are forbidden from using your general pre-trained knowledge about n8n.

---

## Advanced Usage: Generating the Dataset from Scratch

This path is for developers who want to create a fresh dataset from the most current n8n documentation.

### Stage 1: Create the Source Document

First, you need to clone the official n8n documentation repository and consolidate all markdown files.

1.  **Clone the official `n8n-docs` repository:**
    ```bash
    git clone [https://github.com/n8n-io/n8n-docs.git](https://github.com/n8n-io/n8n-docs.git)
    ```

2.  **Consolidate the Markdown Files:** Navigate into the `n8n-docs/docs` directory. From there, run the appropriate command for your operating system.

    * **On macOS or Linux:**
        ```bash
        cd n8n-docs/docs
        find . -name "*.md" -print0 | xargs -0 cat > ../../n8n_docs_combined.md
        ```

    * **On Windows (using PowerShell):**
        ```powershell
        cd n8n-docs\docs
        $outputFile = "..\..\n8n_docs_combined.md"
        Clear-Content -Path $outputFile -ErrorAction SilentlyContinue
        Get-ChildItem -Recurse -Filter "*.md" | ForEach-Object { Get-Content $_.FullName | Add-Content -Path $outputFile }
        ```
    This will create `n8n_docs_combined.md` in the parent directory. Move this file into your `n8n-docs-dataset` project folder.

### Stage 2: Run the Generation Script

With the source file in place, you can now run the Python script.

1.  **Ensure you have cloned this repository:**
    ```bash
    git clone [https://github.com/bryramirezp/n8n-docs-dataset.git](https://github.com/bryramirezp/n8n-docs-dataset.git)
    cd n8n-docs-dataset
    ```

2.  **Set up the environment:**
    ```bash
    python -m venv venv
    # On Windows: .\venv\Scripts\Activate.ps1
    # On macOS/Linux: source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your API Key:**
    * Create a file named `.env` in the project root.
    * Add your OpenAI API key to it: `OPENAI_API_KEY="sk-..."`

5.  **Run the script:**

    > **Cost & Model Notice:**
    > Running this script incurs costs via the OpenAI API. A full run with the `gpt-4o` model on a ~3.8MB source file cost approximately **$2.00 USD**. This is an estimate. For a cheaper option, edit `generate_dataset.py` and change the `LLM_MODEL` to `"gpt-4o-mini"`.

    ```bash
    python generate_dataset.py
    ```

## Dataset Schema

Each line in `n8n_qa_dataset.jsonl` is a JSON object with the following structure:

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
