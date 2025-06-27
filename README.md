# n8n AI Knowledge Base

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/your-username/n8n-ai-knowledge-base/blob/main/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/your-username/n8n-ai-knowledge-base)](https://github.com/your-username/n8n-ai-knowledge-base/commits/main)
[![GitHub repo size](https://img.shields.io/github/repo-size/your-username/n8n-ai-knowledge-base)](https://github.com/your-username/n8n-ai-knowledge-base)

**Note:** Remember to replace `your-username` in the badges above with your actual GitHub username.

---

An open-source project that provides a high-quality, structured JSONL dataset of the entire n8n documentation, ready to be used as a knowledge base for AI applications and RAG (Retrieval-Augmented Generation) systems. This repository includes the Python script used to generate and maintain the dataset, designed to transform technical markdown into a clean, machine-readable format.

## Key Features: Why This Project Matters

The official n8n documentation is excellent for humans but challenging for AI. This project bridges that gap.

* **🧠 Structured & Intelligent:** Instead of a wall of text, this dataset breaks down the documentation into atomic, structured JSON objects. Each object contains not just text, but also metadata, keywords, and extracted entities like code blocks and parameters.
* **🤖 Machine-Readable & Optimized for AI:** The JSONL format is ideal for feeding into LLMs, reducing the risk of hallucinations and enabling more accurate, fact-based responses from your AI assistant.
* **📚 Comprehensive & Consolidated:** Provides a single, unified source file (`n8n_docs_combined.md`) from the many scattered documentation pages, solving a key problem for the community.
* **🔧 Maintainable & Reproducible:** The included Python script (`generate_dataset.py`) is not a one-off tool. It's a resilient, reusable asset that allows anyone to regenerate this dataset from the latest n8n documentation, ensuring your knowledge base never becomes stale.

## Getting Started: Choose Your Path

### Path 1: The AI Builder (Quick Start)

**Goal:** You want to build an AI assistant *now* and don't need to run any code.

1.  **Download the Dataset:** Go to the root of this repository and download the `n8n_qa_dataset.jsonl` file.
2.  **Upload to your AI Platform:** Upload this file directly to the "Knowledge" or "Documents" section of your AI tool (e.g., OpenAI's Custom GPTs, a custom RAG pipeline using LangChain, etc.).
3.  **Use a Strong System Prompt:** To ensure your assistant relies on this high-quality data, configure it with precise instructions.

    > **Example System Prompt for a Custom GPT:**
    >
    > Your role is 'n8n Expert Technical Assistant'. Your only source of truth is the knowledge provided in the uploaded files. When a user asks a question about n8n, you must search your knowledge base for the most relevant structured record. Your answer should be based exclusively on the `concise_answer` and `structured_data` from that record. If the information is not in the knowledge base, you must respond exactly with: "I could not find a precise answer to that question in my knowledge base." You are forbidden from using your general pre-trained knowledge about n8n.

### Path 2: The Developer (Full Replication)

**Goal:** You want to create a fresh dataset from scratch using the most current version of the n8n docs.

#### Stage A: Create the Source Document

First, you need to clone the official n8n documentation repository and consolidate all markdown files.

1.  **Clone the official n8n-docs repository:**
    ```bash
    git clone [https://github.com/n8n-io/n8n-docs.git](https://github.com/n8n-io/n8n-docs.git)
    ```

2.  **Consolidate the Markdown Files:** Navigate into the `n8n-docs/docs` directory. From there, run the appropriate command for your operating system.

    * **On macOS or Linux:**
        ```bash
        cd n8n-docs/docs
        find . -name "*.md" -print0 | xargs -0 cat > ../../n8n_docs_combined.md
        ```
        This command will create `n8n_docs_combined.md` in your project's root folder (`n8n-ai-knowledge-base`).

    * **On Windows (using PowerShell):**
        ```powershell
        cd n8n-docs\docs
        $outputFile = "..\..\n8n_docs_combined.md"
        # Ensure the output file is empty before starting
        Clear-Content -Path $outputFile -ErrorAction SilentlyContinue
        Get-ChildItem -Recurse -Filter "*.md" | ForEach-Object { Get-Content $_.FullName | Add-Content -Path $outputFile }
        ```
        This will also create the consolidated file in your project's root directory.

#### Stage B: Run the Generation Script

Now that you have the source file, you can run the Python script.

1.  **Clone this repository:**
    ```bash
    git clone [https://github.com/your-username/n8n-ai-knowledge-base.git](https://github.com/your-username/n8n-ai-knowledge-base.git)
    cd n8n-ai-knowledge-base
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

    > **Cost & Model Considerations:**
    >
    > Be aware that running this script incurs costs through the OpenAI API. In a test run processing the full documentation (`~3.8MB` of text), the total cost was **approximately $2.00 USD** using the default `gpt-4o` model.
    >
    > This is an estimate. Your actual cost will vary based on the documentation's exact size and current OpenAI API pricing. For a significantly more cost-effective option, you can edit `generate_dataset.py` and change the `MODEL_LLM` variable to `"gpt-4o-mini"`. This model is much cheaper but may have a slightly higher rate of formatting errors.

    ```bash
    python generate_dataset.py
    ```
    The script will find `n8n_docs_combined.md`, process it, and generate your new `n8n_qa_dataset.jsonl`.

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
