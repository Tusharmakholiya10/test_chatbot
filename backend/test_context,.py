from utils.knowledge_search import knowledge_search
from utils.context_builder import context_builder

query = "Python course"

results = knowledge_search.search(query, "courses")

context = context_builder.build(results)

print(context)