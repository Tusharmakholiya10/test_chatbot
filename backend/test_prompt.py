from utils.knowledge_search import knowledge_search
from utils.context_builder import context_builder
from utils.prompt_builder import prompt_builder

question = "What is the duration of the Python course?"

records = knowledge_search.search(question, "courses")

context = context_builder.build(records)

prompt = prompt_builder.build(question, context)

print(prompt)