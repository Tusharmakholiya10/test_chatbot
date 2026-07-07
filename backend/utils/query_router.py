import re


class QueryRouter:

    def __init__(self):

        self.intent_keywords = {

            "courses": [
                "course",
                "courses",
                "python",
                "tally",
                "excel",
                "graphic",
                "design",
                "data analyst",
                "full stack",
                "adca",
                "dit",
                "personality",
                "typing",
                "nursery",
                "ai",
                "development",
                "program"
            ],

            "faculty": [
                "teacher",
                "faculty",
                "trainer",
                "mentor",
                "devendra",
                "mahori",
                "kunal",
                "aman",
                "priya",
                "tansi"
            ],

            "contact": [
                "phone",
                "mobile",
                "contact",
                "email",
                "call",
                "address",
                "location"
            ],

            "branches": [
                "branch",
                "branches",
                "bin",
                "pithoragarh",
                "center"
            ],

            "journey": [
                "admission",
                "register",
                "enroll",
                "join",
                "steps",
                "procedure"
            ],

            "ebooks": [
                "ebook",
                "book",
                "pdf",
                "notes"
            ],

            "highlights": [
                "award",
                "achievement",
                "recognition",
                "placement",
                "impact"
            ],

            "about": [
                "about",
                "vision",
                "mission",
                "history",
                "legacy",
                "institute"
            ]
        }

    def detect(self, query):
        """
        Detect which knowledge category the user's query belongs to.
        Returns the most relevant category.
        """

        query = re.sub(r'[^a-zA-Z0-9 ]', '', query.lower())

        scores = {}

        for category, keywords in self.intent_keywords.items():

            scores[category] = 0

            for keyword in keywords:

                if keyword in query:
                    scores[category] += 1

        best_category = max(scores, key=scores.get)

        if scores[best_category] == 0:
            return "general"

        return best_category


# Global instance
query_router = QueryRouter()