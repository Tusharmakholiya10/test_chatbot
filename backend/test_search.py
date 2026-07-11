from utils.knowledge_search import knowledge_search

questions = [

    ("Python course", "courses"),

    ("Graphic Designing", "courses"),

    ("MERN Stack", "courses"),

    ("Contact Number", "contact"),

    ("Placement", "journey"),

    ("Branch", "branches"),

    ("Faculty", "faculty"),

    ("About LBS", "about"),

    ("Data Analytics", "general")

]

for q, section in questions:

    print("\n" + "="*70)

    print("QUESTION :", q)

    results = knowledge_search.search(q, section)

    for r in results:

        print()

        print("SECTION :", r["section"])
        print("TITLE   :", r["title"])