from utils.query_router import query_router

questions = [
    "Tell me about Python",
    "Who is Devendra Mahori?",
    "Where is your institute located?",
    "How can I take admission?",
    "Do you provide eBooks?",
    "Tell me your achievements"
]

for question in questions:
    print("=" * 50)
    print("Question:", question)
    print("Category:", query_router.detect(question))