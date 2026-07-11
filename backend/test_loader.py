from utils.knowledge_loader import knowledge_loader

print("\n" + "=" * 60)
print("SECTION SUMMARY")
print("=" * 60)

for section, records in knowledge_loader.section_index.items():
    print(f"{section:15} : {len(records)}")

print("\n" + "=" * 60)
print("TOTAL RECORDS")
print("=" * 60)

print(len(knowledge_loader.get_records()))

print("\n" + "=" * 60)
print("FIRST 3 RECORDS")
print("=" * 60)

for record in knowledge_loader.get_records()[:3]:

    print()

    print("ID      :", record["id"])
    print("SECTION :", record["section"])
    print("TITLE   :", record["title"])
    print("TEXT    :", record["search_text"][:150] + "...")