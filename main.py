import json
import os
from collections import defaultdict

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from rich import print
from rich.pretty import Pretty

from services.ai_doc_parser import AIDocumentParser
from services.embeddingService import EmbeddingService


# --- 1. LOAD AND PROCESS DOCUMENTS ---
def load_resume_data(data_path: str):
    all_resume_texts = []

    # Load from all files in the directory
    for filename in os.listdir(data_path):
        filepath = os.path.join(data_path, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
            docs = loader.load()
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(filepath)
            docs = loader.load()
        else:
            continue  # Skip non-supported file types

        # Combine all page contents for this file into a single string
        resume_text = "\n".join(doc.page_content for doc in docs)
        all_resume_texts.append({"filename": filename, "content": resume_text})

    return all_resume_texts


if __name__ == "__main__":
    # Create the vector store (or load if it exists)
    # Initialize the resume parser
    aiDocParser = AIDocumentParser()
    embeddingService = EmbeddingService()

    if embeddingService.collection.count() == 0:
        RESUME_DATA_PATH = "resumes"
        documents = load_resume_data(RESUME_DATA_PATH)

        for doc in documents:
            resume_text = doc["content"]
            # result = resumeParser.extract_resume_structured_details(resume_text)
            result = aiDocParser.parse_resume(resume_text)
            embeddingService.embed_resume_text(result)

    # Load the job description
    # with open("job_description.txt", "r") as f:
    #     job_description = f.read()

    # job_description = aiDocParser.parse_jd(job_description)
    # print(Pretty(job_description,))

    while True:

        query_text = input("\nEnter your query: ")

        # --- PERFORM THE VECTOR SEARCH ---
        results = embeddingService.collection.query(
            query_texts=[query_text],
            n_results=5,  # Ask for the top 5 most similar results
        )

        print("\n[bold cyan]-- Complete ChromaDB Response --[/bold cyan]")
        # The 'rich' library will pretty-print the dictionary
        # Display each result with its metadata and distance
        if results["documents"] and len(results["documents"]) > 0:
            for i in range(len(results["documents"][0])):
                print(f"[bold green]Result {i+1}:[/bold green]")
                print(f"[yellow]Document:[/yellow] {results['documents'][0][i]}")
                print(f"[yellow]Metadata:[/yellow] {results['metadatas'][0][i] if results['metadatas'] and len(results['metadatas']) > 0 else 'No metadata'}")
                print(f"[yellow]Distance:[/yellow] {results['distances'][0][i] if results['distances'] and len(results['distances']) > 0 else 'No distance'}")
                print("-" * 50)
        else:
            print("[yellow]No results found.[/yellow]")
        print("[bold cyan]--------------------------------[/bold cyan]\n")
