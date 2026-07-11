import re
from backend.utils.knowledge_loader import knowledge_loader


class KnowledgeSearch:

    def __init__(self):
        self.loader = knowledge_loader

        # Importance of different fields
        self.field_weights = {
            "name": 100,
            "title": 100,
            "short_name": 80,
            "category": 60,
            "skills": 50,
            "technologies": 50,
            "topics": 50,
            "description": 25,
            "career_opportunities": 20,
            "duration": 15,
            "mode": 15,
            "certificate": 10,
            "placement_support": 10
        }

    # ---------------------------------------------------

    def tokenize(self, text):

        text = str(text).lower()
        text = re.sub(r"[^a-z0-9 ]", " ", text)

        return set(text.split())

    # ---------------------------------------------------

    def field_score(self, query_tokens, value, weight):

        if value is None:
            return 0

        if isinstance(value, list):
            value = " ".join(map(str, value))

        tokens = self.tokenize(value)

        overlap = query_tokens & tokens

        return len(overlap) * weight

    # ---------------------------------------------------

    def score_record(self, query, record, category):

        score = 0

        query_tokens = self.tokenize(query)

        # -------------------------
        # TITLE BONUS
        # -------------------------

        title_tokens = self.tokenize(record["title"])

        overlap = query_tokens & title_tokens

        score += len(overlap) * 120

        # -------------------------
        # FIELD BONUS
        # -------------------------

        fields = record["fields"]

        if isinstance(fields, dict):

            for field, weight in self.field_weights.items():

                if field in fields:

                    score += self.field_score(
                        query_tokens,
                        fields[field],
                        weight
                    )

        # -------------------------
        # CONTENT BONUS
        # -------------------------

        text_tokens = self.tokenize(record["normalized_text"])

        overlap = query_tokens & text_tokens

        score += len(overlap) * 10

        # -------------------------
        # EXACT PHRASE
        # -------------------------

        if query.lower() in record["normalized_text"]:
            score += 40

        # -------------------------
        # SECTION BONUS
        # -------------------------

        if category != "general":

            if record["section"] == category:
                score += 30

        return score

    # ---------------------------------------------------

    def search(self, query, category="general", top_k=5):

        if category == "general":
            records = self.loader.get_records()
        else:
            records = self.loader.get_section(category)

        scored = []

        for record in records:

            score = self.score_record(query, record, category)

            if score > 0:
                scored.append((score, record))

        scored.sort(key=lambda x: x[0], reverse=True)

        if not scored:
            return []

        # ----------------------------
        # Remove weak matches
        # ----------------------------

        best_score = scored[0][0]

        threshold = best_score * 0.40

        filtered = []

        for score, record in scored:

            if score >= threshold:
                filtered.append(record)

        return filtered[:top_k]


knowledge_search = KnowledgeSearch()