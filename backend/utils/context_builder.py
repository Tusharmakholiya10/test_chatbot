class ContextBuilder:

    def __init__(self):
        pass

    # ---------------------------------------------

    def format_value(self, value):

        if value is None:
            return "N/A"

        if isinstance(value, bool):
            return "Yes" if value else "No"

        if isinstance(value, list):

            if len(value) == 0:
                return "N/A"

            return "\n".join(f"• {v}" for v in value)

        if isinstance(value, dict):

            lines = []

            for k, v in value.items():
                lines.append(f"{k.replace('_',' ').title()}: {v}")

            return "\n".join(lines)

        return str(value)

    # ---------------------------------------------

    def build_record(self, record):

        lines = []

        lines.append(f"===== {record['section'].upper()} =====")

        lines.append("")

        lines.append(f"Title: {record['title']}")

        lines.append("")

        fields = record["fields"]

        if isinstance(fields, dict):

            SKIP_FIELDS = {
                "id",
                "slug",
                "keywords",
                "search_keywords"
            }

            for key, value in fields.items():

                if key in SKIP_FIELDS:
                    continue

                key = key.replace("_", " ").title()

                lines.append(f"{key}:")

                lines.append(self.format_value(value))

                lines.append("")

        return "\n".join(lines)

    # ---------------------------------------------

    def build(self, records):

        if not records:
            return "No relevant knowledge found."

        context = []

        for record in records:

            context.append(self.build_record(record))

        return "\n\n".join(context)


context_builder = ContextBuilder()