class ContextBuilder:

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def format_value(self, value):

        if value is None:
            return ""

        if isinstance(value, bool):
            return "Yes" if value else "No"

        if isinstance(value, list):
            return ", ".join(str(v) for v in value)

        if isinstance(value, dict):
            return ", ".join(f"{k}: {v}" for k, v in value.items())

        return str(value)

    # ---------------------------------------------------------

    def build_record(self, record):

        fields = record.get("fields", {})

        lines = []

        lines.append(f"SECTION: {record['section'].title()}")
        lines.append(f"TITLE: {record['title']}")

        important_order = [

            "name",
            "category",
            "duration",
            "level",
            "mode",
            "description",
            "skills",
            "technologies",
            "career_opportunities",
            "certificate",
            "placement_support",
            "phone",
            "email",
            "address"

        ]

        for field in important_order:

            if field in fields:

                value = self.format_value(fields[field])

                if value:
                    label = field.replace("_", " ").title()
                    lines.append(f"{label}: {value}")

        return "\n".join(lines)

    # ---------------------------------------------------------

    def build(self, records):

        if not records:
            return "No relevant knowledge found."

        return "\n\n-----------------------------\n\n".join(
            self.build_record(record)
            for record in records
        )


context_builder = ContextBuilder()