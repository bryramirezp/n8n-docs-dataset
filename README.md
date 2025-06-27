# n8n Docs Dataset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/bryramirezp/n8n-docs-dataset/blob/main/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/bryramirezp/n8n-docs-dataset)](https://github.com/bryramirezp/n8n-docs-dataset/commits/main)
[![GitHub repo size](https://img.shields.io/github/repo-size/bryramirezp/n8n-docs-dataset)](https://github.com/bryramirezp/n8n-docs-dataset)

---

This project provides the key to building your own expert AI partner for n8n workflow creation. It contains a high-quality, structured dataset of the entire n8n documentation, ready to be used as the core knowledge for powerful Custom GPTs, Gems, or other AI assistants.

You get a pre-processed, valuable dataset for immediate use, and this repository also explains how to regenerate this knowledge base yourself, ensuring your AI partner always has the most up-to-date information from the official docs.

## Key Features

* **ｧ Structured & Intelligent:** Instead of a wall of text, this dataset breaks down the documentation into atomic, structured JSON objects. Each object contains not just text, but also metadata, keywords, and extracted entities like code blocks and parameters.
* **､ Machine-Readable & Optimized for AI:** The JSONL format is ideal for feeding into LLMs, reducing the risk of hallucinations and enabling more accurate, fact-based responses from your AI assistant.
* **答 Comprehensive & Consolidated:** Provides a single, unified source file from the many scattered documentation pages, solving a key problem for the community.
* **肌 Maintainable & Reproducible:** The included Python script (`generate_dataset.py`) is not a one-off tool. It's a resilient, reusable asset that allows anyone to regenerate this dataset from the latest n8n documentation, ensuring your knowledge base never becomes stale.

## Dataset at a Glance

This section provides transparency on the scale and freshness of the provided dataset.

| Metric | Value | Purpose |
| :--- | :--- | :--- |
| **Total Records** | `716` | Indicates the total number of structured Q&A pairs in the dataset. |
| **Source Docs Date** | `2025-06-08` | Shows the "freshness" of the data, based on the source files. |
| **Source File Size**| `3.77 MB` | The size of the raw, consolidated `n8n_docs_combined.md` file. |
| **Default LLM Used**| `gpt-4o` | The model used for generation, implying high-quality extraction. |

---

## 🚀 Quick Start: Use the Pre-built Dataset

This path is for users who want to build an AI assistant *now* and don't need to run any code.

1.  **Download the Dataset**
    From the root of this repository, download the `n8n_qa_dataset.jsonl` file.

2.  **Upload to your AI Platform**
    Upload this file directly to the "Knowledge" or "Files" section of your chosen AI tool (e.g., [OpenAI's Custom GPTs](https://chat.openai.com/gpts/editor), a custom RAG pipeline, etc.).

3.  **Use a Strong System Prompt**
    To ensure your assistant relies on this high-quality data, configure it with precise instructions.

    > **Example System Prompt:**
    >
    > You are an 'n8n Expert Technical Assistant'. Your only source of truth is the knowledge provided in the uploaded files. Your answers must be based exclusively on the `concise_answer` and `structured_data` from the records you find. If the information is not in your knowledge base, you must state: "I could not find a precise answer to that question in my knowledge base." You are forbidden from using your general pre-trained knowledge about n8n.

---

## 🛠️ Advanced Usage: Generate the Dataset from Scratch

This path is for developers who want to create a fresh dataset from the most current n8n documentation. This process is divided into two main stages.

### Stage 1: Consolidate the Official n8n Documentation

First, you need a local copy of the official n8n documentation, which you will then combine into a single source file.

1.  **Clone the official `n8n-docs` repository:**
    ```bash
    git clone [https://github.com/n8n-io/n8n-docs.git](https://github.com/n8n-io/n8n-docs.git)
    ```

2.  **Navigate into the `docs` directory:**
    ```bash
    cd n8n-docs/docs
    ```

3.  **Consolidate all Markdown files into one:**
    From inside the `n8n-docs/docs` directory, run the command appropriate for your operating system. This command will find every `.md` file and combine its content into a single file named `n8n_docs_combined.md` located two levels up (in the same directory as the `n8n-docs` folder).

    * **On macOS or Linux:**
        ```bash
        find . -name "*.md" -print0 | xargs -0 cat > ../../n8n_docs_combined.md
        ```

    * **On Windows (using PowerShell):**
        ```powershell
        $outputFile = "..\..\n8n_docs_combined.md"
        if (Test-Path $outputFile) { Clear-Content -Path $outputFile }
        Get-ChildItem -Recurse -Filter "*.md" | ForEach-Object { Get-Content $_.FullName | Add-Content -Path $outputFile }
        ```
    
    After this step, you can navigate back to your original project directory.
    ```bash
    cd ../../ 
    ```

### Stage 2: Run the Dataset Generation Script

Now that you have the source file, you can use the Python script from *this* repository to generate the structured dataset.

1.  **Clone this repository (if you haven't already):**
    ```bash
    git clone [https://github.com/bryramirezp/n8n-docs-dataset.git](https://github.com/bryramirezp/n8n-docs-dataset.git)
    cd n8n-docs-dataset
    ```

2.  **Move the source file into this project:**
    Move the `n8n_docs_combined.md` file you created in Stage 1 into the `n8n-docs-dataset` project folder.

3.  **Set up a Python virtual environment:**
    ```bash
    # Create the virtual environment
    python -m venv venv
    
    # Activate it
    # On Windows (PowerShell):
    .\venv\Scripts\Activate.ps1
    # On macOS/Linux:
    source venv/bin/activate
    ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure your API Key:**
    * Create a file named `.env` in the project root.
    * Add your OpenAI API key to it like this:
        ```
        OPENAI_API_KEY="sk-..."
        ```

6.  **Run the script:**
    > **Cost & Model Notice:**
    > Running this script incurs costs via the OpenAI API. A full run with the `gpt-4o` model on a ~3.8MB source file cost approximately **$2.00 USD**. This is an estimate. For a cheaper, faster option, you can edit `generate_dataset.py` and change the `LLM_MODEL` variable to `"gpt-4o-mini"`.

    ```bash
    python generate_dataset.py
    ```
    Once the script finishes, you will find the `n8n_qa_dataset.jsonl` file in your project directory, ready to be used.

## Dataset Schema

Each line in `n8n_qa_dataset.jsonl` is a JSON object with the following structure. This schema is designed to provide rich, contextual information for an AI assistant.

```json
{
  "content_type": "The category of the content (e.g., 'Node Reference', 'How-To Guide').",
  "section_title": "The original section title from the documentation.",
  "user_question": "A realistic question a user might ask about the content.",
  "concise_answer": "A direct, easy-to-understand answer to the user's question.",
  "structured_data": {
    "key_parameters": [
      {
        "name": "Parameter Name", 
        "description": "What the parameter does.", 
        "example": "Example value or usage."
      }
    ],
    "code_block": "A relevant block of code (e.g., JavaScript, JSON, Shell), if present."
  },
  "keywords": ["list", "of", "relevant", "keywords", "for", "retrieval"]
}
```
