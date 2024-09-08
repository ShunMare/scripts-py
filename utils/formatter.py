class Formatter:
    @staticmethod
    def format_heading_result(data):
        """
        見出し結果を視覚的にわかりやすい形式にフォーマットする
        """
        formatted = f"URL: {data['url']}\n\n"
        formatted += "H2 見出し:\n"
        for i, h2 in enumerate(data["h2"], 1):
            formatted += f"{i}. {h2}\n"
        formatted += "\nH3 見出し:\n"
        for i, h3 in enumerate(data["h3"], 1):
            formatted += f"{i}. {h3}\n"
        return formatted
