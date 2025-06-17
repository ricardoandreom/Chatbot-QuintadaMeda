from pathlib import Path

def load_documents_from_txt(folder_path="data"):
    documents = []
    for txt_file in Path(folder_path).glob("*.txt"):
        with open(txt_file, encoding="utf-8") as f:
            content = f.read()
            documents.append({"source": txt_file.name, "content": content})
    return documents
