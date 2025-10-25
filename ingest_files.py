from rag_store import add_document
import glob

for path in glob.glob("project_files/*.txt"):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        add_document(f"file-{path}", text, {"type": "project_file", "path": path})

print("✅ Project files ingested into RAG")
