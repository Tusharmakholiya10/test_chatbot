from utils.query_router import query_router

questions = [

    "Tell me about LBS",

    "Contact details",

    "Python course",

    "What is MERN Stack?",

    "Admission process",

    "Faculty members",

    "Where is your branch?",

    "Do you have ebooks?",

    "Placement record",

    "Hello"

]

for q in questions:

    result = query_router.detect(q)

    print("=" * 70)

    print("Question :", q)

    print("Category :", result["category"])

    print("Confidence :", result["confidence"])

    print("Matched :", result["matched_keywords"])