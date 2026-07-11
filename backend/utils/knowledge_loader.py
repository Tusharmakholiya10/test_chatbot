import json
import re
from pathlib import Path


class KnowledgeLoader:

    def __init__(self):
        self.records = []
        self.section_index = {}

        self.load()

    # --------------------------------------------------------

    def clean(self, text):

        text = str(text).lower()

        text = re.sub(r"[^a-z0-9 ]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # --------------------------------------------------------

    def flatten(self, obj):

        if obj is None:
            return ""

        if isinstance(obj, (str, int, float, bool)):
            return str(obj)

        if isinstance(obj, list):
            return " ".join(self.flatten(x) for x in obj)

        if isinstance(obj, dict):
            return " ".join(self.flatten(v) for v in obj.values())

        return ""

    # --------------------------------------------------------

    def add_record(self, section, title, data):

        record = {

            "id": f"{section}_{len(self.records)+1}",

            "section": section,

            "title": title,

            "fields": data,

            "search_text": self.flatten(data),

            "normalized_text": self.clean(self.flatten(data)),

            "data": data

        }

        self.records.append(record)

        self.section_index.setdefault(section, []).append(record)

    # --------------------------------------------------------

    def read_json(self, filename):

        path = Path(__file__).parent.parent / "knowledge" / filename

        with open(path, encoding="utf-8") as f:
            return json.load(f)

    # --------------------------------------------------------
    # ABOUT
    # --------------------------------------------------------

    def load_about(self):

        data = self.read_json("about.json")

        self.add_record("about", "About", data["about"])

    # --------------------------------------------------------
    # CONTACT
    # --------------------------------------------------------

    def load_contact(self):

        data = self.read_json("contact.json")

        self.add_record("contact", "Contact", data["contact"])

    # --------------------------------------------------------
    # INSTITUTE
    # --------------------------------------------------------

    def load_institute(self):

        data = self.read_json("institute.json")

        self.add_record("institute", "Institution", data["institution"])

    # --------------------------------------------------------
    # BRANCHES
    # --------------------------------------------------------

    def load_branches(self):

        data = self.read_json("branches.json")

        for branch in data["branches"]:

            self.add_record(

                "branches",

                branch.get("name", "Branch"),

                branch

            )

    # --------------------------------------------------------
    # FACULTY
    # --------------------------------------------------------

    def load_faculty(self):

        data = self.read_json("faculty.json")

        for faculty in data["faculty"]:

            self.add_record(

                "faculty",

                faculty.get("name", "Faculty"),

                faculty

            )

    # --------------------------------------------------------
    # COURSES
    # --------------------------------------------------------

    def load_courses(self):

        data = self.read_json("courses.json")

        for course in data["courses"]:

            self.add_record(

                "courses",

                course.get("name", "Course"),

                course

            )

    # --------------------------------------------------------
    # EBOOKS
    # --------------------------------------------------------

    def load_ebooks(self):

        data = self.read_json("ebooks.json")

        for ebook in data["ebooks"]:

            self.add_record(

                "ebooks",

                ebook.get("title", "Ebook"),

                ebook

            )

    # --------------------------------------------------------
    # HIGHLIGHTS
    # --------------------------------------------------------

    def load_highlights(self):

        data = self.read_json("highlights.json")

        for key, value in data["highlights"].items():

            self.add_record(

                "highlights",

                key.replace("_", " ").title(),

                value

            )

    # --------------------------------------------------------
    # JOURNEY
    # --------------------------------------------------------

    def load_journey(self):

        data = self.read_json("journey.json")

        for key, value in data.items():

            self.add_record(

                "journey",

                key.replace("_", " ").title(),

                value

            )

    # --------------------------------------------------------

    def load(self):

        self.load_about()
        self.load_branches()
        self.load_contact()
        self.load_courses()
        self.load_ebooks()
        self.load_faculty()
        self.load_highlights()
        self.load_institute()
        self.load_journey()

        print(f"✅ Loaded {len(self.section_index)} sections")
        print(f"✅ Created {len(self.records)} searchable records")

    # --------------------------------------------------------

    def get_records(self):

        return self.records

    def get_section(self, section):

        return self.section_index.get(section, [])


knowledge_loader = KnowledgeLoader()