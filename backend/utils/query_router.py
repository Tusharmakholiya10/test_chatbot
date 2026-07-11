import re


class QueryRouter:

    def __init__(self):

        self.categories = {

            "about": [
                "about",
                "institute",
                "history",
                "vision",
                "mission",
                "organization",
                "lbs"
            ],

            "courses": [
                "course",
                "courses",
                "python",
                "excel",
                "advanced excel",
                "tally",
                "gst",
                "graphic",
                "design",
                "photoshop",
                "web",
                "full stack",
                "mern",
                "react",
                "artificial intelligence",
                "machine learning",
                "data analytics",
                "certificate",
                "diploma",
                "duration",
                "fee",
                "fees",
                "cost",
                "price",
                "eligibility"
            ],

            "contact": [
                "contact",
                "phone",
                "mobile",
                "email",
                "address",
                "location",
                "office",
                "call",
                "reach"
            ],

            "faculty": [
                "faculty",
                "teacher",
                "trainer",
                "mentor",
                "staff",
                "instructor"
            ],

            "branches": [
                "branch",
                "branches",
                "campus",
                "centre",
                "center"
            ],

            "journey": [
                "admission",
                "apply",
                "registration",
                "register",
                "documents",
                "process",
                "placement",
                "certificate verification"
            ],

            "ebooks": [
                "ebook",
                "ebook",
                "book",
                "books",
                "study material",
                "notes"
            ],

            "highlights": [
                "achievement",
                "highlight",
                "success",
                "placement record"
            ]

        }
        

    def clean(self, query):

        query = query.lower()

        query = re.sub(r'[^a-z0-9 ]', ' ', query)

        query = re.sub(r'\s+', ' ', query)

        return query.strip()

    def detect(self, query):

        query = self.clean(query)
        query_words = set(query.split())

        scores = {}
        matched = {}

        for category, keywords in self.categories.items():

            score = 0
            found = []

            for keyword in keywords:

                keyword = self.clean(keyword)

                # Multi-word phrase
                if " " in keyword:
                    if keyword in query:
                        score += 2
                        found.append(keyword)

                # Single word
                else:
                    if keyword in query_words:
                        score += 1
                        found.append(keyword)

            scores[category] = score
            matched[category] = found

        best_category = max(scores, key=scores.get)

        if scores[best_category] == 0:

            return {
                "category": "general",
                "confidence": 0.0,
                "matched_keywords": []
            }

        confidence = round(
            scores[best_category] / max(scores.values()),
            2
        )

        return {
            "category": best_category,
            "confidence": confidence,
            "matched_keywords": matched[best_category]
        }


query_router = QueryRouter()