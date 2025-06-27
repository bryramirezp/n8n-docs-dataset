n8n Docs Dataset
An open-source project that provides a high-quality, structured JSONL dataset of the entire n8n documentation, ready to be used as a knowledge base for AI applications and RAG (Retrieval-Augmented Generation) systems. This repository includes the Python script used to generate and maintain the dataset, designed to transform technical markdown into a clean, machine-readable format.

Motivation & Community Need
The official n8n documentation is excellent for humans but challenging for AI. This project was born from a clear need within the n8n community (as seen in forums like Reddit) for an easy way to consolidate and feed the documentation into AI models to build more intelligent, context-aware workflows. This project bridges that gap.

Key Features: Why This Project Matters
🧠 Structured & Intelligent: Instead of a wall of text, this dataset breaks down the documentation into atomic, structured JSON objects. Each object contains not just text, but also metadata, keywords, and extracted entities like code blocks and parameters.

🤖 Machine-Readable & Optimized for AI: The JSONL format is ideal for feeding into LLMs, reducing the risk of hallucinations and enabling more accurate, fact-based responses from your AI assistant.

📚 Comprehensive & Consolidated: Provides a single, unified source file from the many scattered documentation pages, solving a key problem for the community.

🔧 Maintainable & Reproducible: The included Python script (generate_dataset.py) is not a one-off tool. It's a resilient, reusable asset that allows anyone to regenerate this dataset from the latest n8n documentation, ensuring your knowledge base never becomes stale.

Project Status & Dataset Statistics
Last Generated: June 27, 2025

n8n-docs Version: Based on commit [Enter Commit Hash Here] from the official repo.

Total Records: 716

Source File Size: ~3.8 MB

(Note: To find the commit hash, navigate to your local clone of the n8n-io/n8n-docs repository and run git rev-parse HEAD).

Getting Started: Choose Your Path
Path 1: The AI Builder (Quick Start)
Goal: You want to build an AI assistant now and don't need to run any code.

Download the Dataset: Go to the root of this repository and download the n8n_qa_dataset.jsonl file.

Upload to your AI Platform: Upload this file directly to the "Knowledge" section of your AI tool. For example, you can create a new Custom GPT by going to chat.openai.com/gpts/editor.

Use a Strong System Prompt: To ensure your assistant relies on this high-quality data, configure it with precise instructions.

Example System Prompt for a Custom GPT:

Your role is 'n8n Expert Technical Assistant'. Your only source of truth is the knowledge provided in the uploaded files. When a user asks a question about n8n, you must search your knowledge base for the most relevant structured record. Your answer should be based exclusively on the concise_answer and structured_data from that record. If the information is not in the knowledge base, you must respond exactly with: "I could not find a precise answer to that question in my knowledge base." You are forbidden from using your general pre-trained knowledge about n8n.

Path 2: The Developer (Full Replication)
Goal: You want to create a fresh dataset from scratch using the most current version of the n8n docs.

Stage A: Create the Source Document
First, you need to clone the official n8n documentation repository and consolidate all markdown files.

Clone the official n8n-docs repository:

git clone https://github.com/n8n-io/n8n-docs.git

Consolidate the Markdown Files: Navigate into the n8n-docs/docs directory. From there, run the appropriate command for your operating system.

On macOS or Linux:

cd n8n-docs/docs
find . -name "*.md" -print0 | xargs -0 cat > ../../n8n_docs_combined.md

This command will create n8n_docs_combined.md in the parent directory. Move this file into your n8n-docs-dataset project folder.

On Windows (using PowerShell):

cd n8n-docs\docs
$outputFile = "..\..\n8n_docs_combined.md"
# Ensure the output file is empty before starting
Clear-Content -Path $outputFile -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Filter "*.md" | ForEach-Object { Get-Content $_.FullName | Add-Content -Path $outputFile }

This will also create the consolidated file in the parent directory. Move this file into your n8n-docs-dataset project folder.

Stage B: Run the Generation Script
Now that you have the source file inside this project's folder, you can run the Python script.

Clone this repository:

git clone https://github.com/bryramirezp/n8n-docs-dataset.git
cd n8n-docs-dataset

Set up the environment:

python -m venv venv
# On Windows: .\venv\Scripts\Activate.ps1
# On macOS/Linux: source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Configure your API Key:

Create a file named .env in the project root.

Add your OpenAI API key to it: OPENAI_API_KEY="sk-..."

Run the script:

Cost & Model Considerations:

Be aware that running this script incurs costs through the OpenAI API. In a test run processing the full documentation (~3.8MB of text), the total cost was approximately $2.00 USD using the default gpt-4o model.

This is an estimate. Your actual cost will vary based on the documentation's exact size and current OpenAI API pricing. For a significantly more cost-effective option, you can edit generate_dataset.py and change the LLM_MODEL variable to "gpt-4o-mini". This model is much cheaper but may have a slightly higher rate of formatting errors.

python generate_dataset.py

The script will find n8n_docs_combined.md, process it, and generate your new n8n_qa_dataset.jsonl.

Dataset Structure
Each line in the n8n_qa_dataset.jsonl file is a JSON object with the following structure:

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

Contributing
Contributions are welcome! If you find a bug, have a suggestion for improving the script, or want to enhance the dataset, please feel free to:

Open an Issue to discuss the change.

Submit a Pull Request with your improvements.

License
This project is licensed under the MIT License. See the LICENSE file for details.
