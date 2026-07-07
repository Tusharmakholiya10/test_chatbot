import json


class ContextBuilder:

    def build(self, search_results):
        """
        Converts search results into readable context
        that Gemini can understand.
        """

        if not search_results:
            return "No relevant institute information was found."

        context = []

        for result in search_results:

            section = result.get("section", "").upper()
            data = result.get("data", {})

            context.append(f"\n===== {section} =====")

            if isinstance(data, dict):

                for key, value in data.items():

                    if isinstance(value, list):
                        value = ", ".join(str(v) for v in value)

                    context.append(f"{key}: {value}")

            else:
                context.append(str(data))

        return "\n".join(context)


context_builder = ContextBuilder()