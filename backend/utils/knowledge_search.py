import re
from difflib import SequenceMatcher
from utils.knowledge_loader import knowledge_loader


class KnowledgeSearch:

    def __init__(self):
        self.knowledge = knowledge_loader.get()

    def clean(self, text):
        return re.sub(r'[^a-zA-Z0-9 ]', '', str(text).lower())

    def similarity(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def search(self, query, threshold=0.45):

        query = self.clean(query)

        results = []

        for section, data in self.knowledge.items():

            if isinstance(data, list):

                for item in data:

                    score = self.score_item(query, item)

                    if score >= threshold:

                        results.append({
                            "section": section,
                            "score": score,
                            "data": item
                        })

            elif isinstance(data, dict):

                score = self.score_item(query, data)

                if score >= threshold:

                    results.append({
                        "section": section,
                        "score": score,
                        "data": data
                    })

        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:5]

    def score_item(self, query, item):

        score = 0

        for value in item.values():

            if isinstance(value, list):

                for v in value:
                    s = self.similarity(query, self.clean(v))
                    score = max(score, s)

            else:

                s = self.similarity(query, self.clean(value))
                score = max(score, s)

        return score


knowledge_search = KnowledgeSearch()