# n8n Docs Dataset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/bryramirezp/n8n-docs-dataset/blob/main/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/bryramirezp/n8n-docs-dataset)](https://github.com/bryramirezp/n8n-docs-dataset/commits/main)
[![GitHub repo size](https://img.shields.io/github/repo-size/bryramirezp/n8n-docs-dataset)](https://github.com/bryramirezp/n8n-docs-dataset)

---

This project provides the key to building your own expert AI partner for n8n workflow creation. It contains a high-quality, structured dataset of the entire n8n documentation, ready to be used as the core knowledge for powerful Custom GPTs, Gems, or other AI assistants.

You get a pre-processed, valuable dataset for immediate use, and this repository also explains how to regenerate this knowledge base yourself, ensuring your AI partner always has the most up-to-date information from the official docs.

## Key Features

* **🧠 Structured & Intelligent:** Instead of a wall of text, this dataset breaks down the documentation into atomic, structured JSON objects. Each object contains not just text, but also metadata, keywords, and extracted entities like code blocks and parameters.
* **🤖 Machine-Readable & Optimized for AI:** The JSONL format is ideal for feeding into LLMs, reducing the risk of hallucinations and enabling more accurate, fact-based responses from your AI assistant.
* **📚 Comprehensive & Consolidated:** Provides a single, unified source file from the many scattered documentation pages, solving a key problem for the community.
* **🔧 Maintainable & Reproducible:** The included Python script (`generate_dataset.py`) is not a one-off tool. It's a resilient, reusable asset that allows anyone to regenerate this dataset from the latest n8n documentation, ensuring your knowledge base never becomes stale.

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

This path is for developers who want to create a fresh dataset from the most current n8n documentation. This process ensures you are working with the latest possible information.

### Prerequisites

Before you begin, ensure you have the following installed. You can check by opening a terminal (or PowerShell on Windows) and running these commands:

* **Python (3.8 or higher):**
    ```bash
    python --version
    ```
* **PIP (Python's package manager):**
    ```bash
    pip --version
    ```
* **A Code Editor:** **Visual Studio Code is highly recommended**. It has an excellent integrated terminal (you can open it with `Ctrl+` \` or `View > Terminal`), which makes running all the commands in one place simple and efficient.

### Step 1: Consolidate the Official n8n Documentation

First, you need a local copy of the official n8n documentation, which you will then combine into a single source file.

1.  **Clone the official `n8n-docs` repository:**
    ```bash
    git clone https://github.com/n8n-io/n8n-docs.git
    ```

2.  **Navigate into the `docs` directory:**
    ```bash
    cd n8n-docs/docs
    ```

3.  **Consolidate all Markdown files into one:**
    From inside the `n8n-docs/docs` directory, run the command for your operating system. This will create a single file named `n8n_docs_combined.md` in the parent directory of your `n8n-docs` folder.

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
    
4.  **Return to your starting directory:**
    ```bash
    cd ../../ 
    ```

### Step 2: Set Up the Generation Project

Now you will set up this repository to process the file you just created.

1.  **Clone this repository:**
    ```bash
    git clone https://github.com/bryramirezp/n8n-docs-dataset.git
    ```

2.  **Enter the project directory and move the source file:**
    ```bash
    # Move into the project folder
    cd n8n-docs-dataset

    # Move the consolidated doc file into this folder
    # Use 'move' on Windows CMD or 'mv' on PowerShell/macOS/Linux
    mv ../n8n_docs_combined.md .
    ```

3.  **Create and activate a virtual environment:**
    A virtual environment is crucial for keeping project dependencies isolated.
    ```bash
    # Create the virtual environment
    python -m venv venv
    
    # Activate it
    # On Windows (PowerShell):
    .\venv\Scripts\Activate.ps1
    # If you get an execution policy error, run the following command and then try activating again:
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    
    # On macOS/Linux:
    source venv/bin/activate
    ```
    You'll know it's active when you see `(venv)` at the beginning of your terminal prompt.

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure your OpenAI API Key:**
    You need to create a `.env` file to securely store your OpenAI API key. The file must be saved with **UTF-8** encoding.

    **Method 1: Manual Creation**
    * In your code editor (like VS Code), create a new file named `.env` in the project root.
    * Add the following line, replacing `sk-...` with your actual secret key:
        ```
        OPENAI_API_KEY="sk-..."
        ```
    * Ensure you save the file with UTF-8 encoding. In VS Code, you can check and change the encoding in the bottom-right status bar.

    **Method 2: Quick Command**
    You can create the file with the correct content and encoding in one step. **Remember to replace `sk-...` with your actual key inside the quotes.**

    * **On Linux, macOS, or Git Bash (Windows):**
        ```bash
        echo 'OPENAI_API_KEY="sk-..."' > .env
        ```
    * **On Windows PowerShell (Recommended):**
        ```powershell
        'OPENAI_API_KEY="sk-..."' | Out-File -FilePath .env -Encoding utf8
        ```

### Step 3: Run the Script and Generate the Dataset

With everything in place, you are ready to generate the dataset.

1.  **Execute the script:**
    In your terminal (with the `venv` still active), run the following command:
    ```bash
    python generate_dataset.py
    ```

2.  **Monitor the progress:**
    The script will print status updates to the terminal, showing you that it's loading the file, splitting it into chunks, and processing each chunk with the LLM. This is the longest part of the process and can take several minutes.

3.  **Verify the output:**
    Once the script shows the "Process finished!" message, a new file named `n8n_qa_dataset.jsonl` will appear in your project folder. You can open it to inspect the structured Q&A pairs. This file is your final, ready-to-use dataset.

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
