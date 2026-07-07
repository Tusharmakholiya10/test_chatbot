# backend/test_search.py

from utils.knowledge_search import knowledge_search

queries = [

    "python",

    "graphic",

    "founder",

    "placement",

    "office",

    "data analyst"

]

for q in queries:

    print("="*50)

    print("Query:", q)

    result = knowledge_search.search(q)

    for r in result:

        print(r["section"], round(r["score"],2))