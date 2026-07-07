import json
from pathlib import Path


class KnowledgeLoader:
    def __init__(self):
        self.knowledge = {}
        self.load_all()

    def load_json(self, filename):
        """Load a single JSON file."""
        base_path = Path(__file__).parent.parent / "knowledge"
        file_path = base_path / filename

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")
            return {}

    def load_all(self):
        """Load every knowledge file."""
        files = [
            "institute.json",
            "about.json",
            "highlights.json",
            "courses.json",
            "faculty.json",
            "branches.json",
            "contact.json",
            "ebooks.json",
            "journey.json",
            
        ]

        for file in files:
            key = file.replace(".json", "")
            self.knowledge[key] = self.load_json(file)

        print("✅ Knowledge Base Loaded Successfully")

    def get(self):
        return self.knowledge


# Global instance
knowledge_loader = KnowledgeLoader()