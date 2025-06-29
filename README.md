# n8n Docs Dataset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/bryramirezp/n8n-docs-dataset/blob/main/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/bryramirezp/n8n-docs-dataset)](https://github.com/bryramirezp/n8n-docs-dataset/commits/main)
[![GitHub repo size](https://img.shields.io/github/repo-size/bryramirezp/n8n-docs-dataset)](https://github.com/bryramirezp/n8n-docs-dataset)

---

## Dataset Philosophy and Methodology

This dataset is not just a simple text extraction. It has been conceived and structured following a methodology of debugging and enrichment to maximize its strategic value. Below is the analysis that guides the creation and maintenance of this resource.

### 1. The Strategic Purpose: What is this Dataset Useful for?

A Question-Answering (QA) pair dataset focused on n8n is an extremely valuable asset. Its primary utility is the **fine-tuning** of a Large Language Model (LLM) to create an expert virtual assistant specialized in n8n.

The key objectives achieved with a good dataset are:

* **Create an "n8n Expert" on demand:** An LLM fine-tuned with this dataset can answer user questions with a level of precision and context that a generic model cannot achieve. It will understand n8n's jargon, specific nodes, common use cases, and best practices.
* **Reduce Support Load:** It automates responses to frequent and complex questions that would typically fall on community forums, Discord, or support teams.
* **Accelerate the User Learning Curve:** New and advanced users alike can get instant, contextual help to build workflows, debug errors, or implement complex logic.
* **Dynamic Documentation Generation:** The dataset's high-quality answers can serve as a basis for generating code examples, tutorials, and documentation snippets.
* **Model Benchmarking:** It allows for evaluating how well different LLMs "understand" n8n before and after fine-tuning, serving as a standardized performance test.

### 2. Common Limitations and Flaws: What Problems Are We Trying to Solve?

A dataset, no matter how large, can have critical flaws that, if not corrected, will negatively impact the final model. This project focuses on identifying and mitigating the following common problems:

* **Biased and Superficial Coverage:**
    * **Common Flaw:** The dataset focuses excessively on basic nodes and ignores more complex nodes or advanced use cases.
    * **Consequence Avoided:** The resulting model is competent for both beginner tasks and real-world problems involving complex workflows.
* **Outdated Information:**
    * **Common Flaw:** n8n evolves quickly. A dataset might contain information about parameters or interfaces that no longer exist.
    * **Consequence Avoided:** The model will not "hallucinate" or provide incorrect instructions, thereby building user trust.
* **Lack of "Real-World" and Debugging Cases:**
    * **Common Flaw:** Most questions are theoretical ("What does Node X do?") instead of practical ("How do I process this nested JSON and handle errors?").
    * **Consequence Avoided:** The assistant becomes a problem-solver, not just a dictionary.
* **Factual and Code Errors:**
    * **Common Flaw:** Answers contain incorrect code expressions or flawed conceptual explanations.
    * **Consequence Avoided:** The model learns correct information and becomes a reliable source.
* **Inconsistent Terminology:**
    * **Common Flaw:** Terms like "workflow," "scenario," or "flow" are used interchangeably.
    * **Consequence Avoided:** Consistent terminology aligned with the official n8n documentation is used, preventing confusion for both the model and the end-user.

### 3. The Debugging and Enrichment Plan: How is the Dataset Improved?

To address the issues above, the improvement plan focuses on a rigorous process of auditing and enrichment:

* **Coverage & Freshness Audit:**
    * **Action:** Programmatically cross-reference the dataset's topics against the complete list of nodes and features in the official n8n documentation.
    * **Result:** Generate a "heatmap" that shows which areas are well-covered, which are superficial, and which are missing, in order to guide enrichment.
* **Real-World Use Case Enrichment:**
    * **Action:** Systematically mine the n8n community forum and other channels to extract real, complex problems that users have faced.
    * **Result:** Create new, high-quality QA pairs based on debugging, architecture, and complex data transformation problems.
* **Technical & Factual Validation:**
    * **Action:** Every QA pair, especially those with code, is reviewed and tested by an expert to ensure it works as described.
    * **Result:** A 100% verified dataset that builds trust.
* **Standardization & Formatting:**
    * **Action:** Ensure the entire dataset follows a clean, unified JSONL structure.
    * **Result:** A dataset that is ready to be consumed by any fine-tuning platform without requiring additional pre-processing.

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
    > You are an 'n8n Expert Technical Assistant'. Your only source of truth is the knowledge provided in the uploaded files. Your answers must be based exclusively on the `concise_answer` and `structured_data` from the records you find. If you cannot find the information in your knowledge base, you must state: "I could not find a precise answer to that question in my knowledge base." You are forbidden from using your general pre-trained knowledge about n8n.

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
* **A Code Editor:** **Visual Studio Code is highly recommended**. It has an excellent integrated terminal (you can open it with `Ctrl+` \` or `View > Terminal`), and it allows you to easily control file encoding, which is critical for this project.

### Step 1: Consolidate the Official n8n Documentation

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
    From inside the `n8n-docs/docs` directory, run the command for your operating system.
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

1.  **Clone this repository, enter the directory, and move the source file:**
    ```bash
    git clone [https://github.com/bryramirezp/n8n-docs-dataset.git](https://github.com/bryramirezp/n8n-docs-dataset.git)
    cd n8n-docs-dataset
    mv ../n8n_docs_combined.md .
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the virtual environment
    python -m venv venv
    
    # Activate it
    # On Windows (PowerShell):
    .\venv\Scripts\Activate.ps1
    # If you get an execution policy error, run the following command and then try activating again:
    # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your OpenAI API Key:**
    Creating the `.env` file correctly is critical. The file **must** be saved with **UTF-8** encoding. The most reliable way to do this is by creating the file manually in a code editor like VS Code.

    1.  **Create the file:** In your code editor, create a new file in the project root. Name it exactly `.env`.
    2.  **Add your key:** Paste the following line into the file, replacing `sk-...` with your actual key.
        ```
        OPENAI_API_KEY="sk-..."
        ```
    3.  **Save the file**, ensuring the encoding is `UTF-8`.

    > #### Troubleshooting Encoding Errors
    > If you run the script and get a `UnicodeDecodeError`, it means the `.env` file was saved with the wrong encoding (like `UTF-8 with BOM`). Here is the foolproof way to fix it in VS Code:
    >
    > 1.  Open the `.env` file in Visual Studio Code.
    > 2.  In the status bar at the bottom-right, click where it says `UTF-8 with BOM` or any other encoding.
    > 3.  A menu will open at the top. Select **"Save with Encoding"**.
    > 4.  From the list that appears, choose **"UTF-8"**.
    >
    > Done! This will save the file in the correct format, and your Python script will now run without problems.

### Step 3: Run the Script and Generate the Dataset

With everything in place, you are ready to generate the dataset.

1.  **Execute the script:**
    In your terminal (with the `venv` still active), run the following command:
    ```bash
    python generate_dataset.py
    ```

2.  **Monitor the progress:**
    The script will print status updates to the terminal as it loads the file, splits it into chunks, and processes each chunk. This is the longest part of the process and can take several minutes.

3.  **Verify the output:**
    Once the script shows the "Process finished!" message, a new file named `n8n_qa_dataset.jsonl` will appear in your project folder. This file is your final, ready-to-use dataset.

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
