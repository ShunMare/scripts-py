from bs4 import Tag, NavigableString
import re
from typing import List
import html
from bs4 import BeautifulSoup
from src.log_operations.log_handlers import CustomLogger

logger = CustomLogger(__name__)


class TextConverter:
    @classmethod
    def convert_to_markdown(cls, element: Tag) -> str:
        """
        HTMLエレメントをMarkdown形式に変換します。

        :param element: 変換するBeautifulSoupのTagオブジェクト
        :return: 変換されたMarkdown文字列
        """
        logger.debug("HTMLエレメントのMarkdown変換を開始します。")
        markdown = cls._process_element(element)
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)
        markdown = re.sub(r"<[^>]+>", "", markdown)
        markdown = (
            markdown.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        return markdown.strip()

    @classmethod
    def _process_element(cls, el: Tag, level: int = 0) -> str:
        if isinstance(el, NavigableString):
            return str(el)

        result = []
        if el.name == "h1":
            result.append(f"# {el.get_text(strip=True)}\n\n")
        elif el.name == "h2":
            result.append(f"## {el.get_text(strip=True)}\n\n")
        elif el.name == "h3":
            result.append(f"### {el.get_text(strip=True)}\n\n")
        elif el.name == "p":
            result.append(f"{el.get_text(strip=True)}\n\n")
        elif el.name == "ul":
            result.extend(cls._process_list(el, level, is_ordered=False))
        elif el.name == "ol":
            result.extend(cls._process_list(el, level, is_ordered=True))
        elif el.name == "li":
            result.append(cls._process_list_item(el, level))
        elif el.name == "a":
            href = el.get("href", "")
            text = el.get_text(strip=True)
            result.append(f"[{text}]({href})")
        elif el.name in ["strong", "b"]:
            result.append(f"**{el.get_text(strip=True)}**")
        elif el.name in ["em", "i"]:
            result.append(f"*{el.get_text(strip=True)}*")
        elif el.name == "code":
            result.append(f"`{el.get_text(strip=True)}`")
        elif el.name == "pre":
            code = el.get_text(strip=True)
            result.append(f"```\n{code}\n```\n\n")
        else:
            for child in el.children:
                result.append(cls._process_element(child, level))

        return "".join(result)

    @classmethod
    def _process_list(cls, el: Tag, level: int, is_ordered: bool) -> List[str]:
        result = []
        for i, li in enumerate(el.find_all("li", recursive=False), 1):
            prefix = f"{i}. " if is_ordered else "- "
            content = cls._process_list_item(li, level + 1)
            result.append(f"{'  ' * level}{prefix}{content}\n")
        return result

    @classmethod
    def _process_list_item(cls, el: Tag, level: int) -> str:
        content = []
        for child in el.children:
            if isinstance(child, Tag):
                if child.name in ["ul", "ol"]:
                    content.append(
                        "\n"
                        + "".join(cls._process_list(child, level, child.name == "ol"))
                    )
                else:
                    content.append(cls._process_element(child, level).strip())
            else:
                content.append(child.strip())
        return " ".join(content).strip()

    @classmethod
    def convert_to_html(cls, markdown_text: str) -> str:
        """
        Markdown形式のテキストをHTML形式に変換します。

        :param markdown_text: 変換するMarkdownテキスト
        :return: 変換されたHTML文字列
        """
        logger.debug("Markdownテキストのhtml変換を開始します。")
        lines = markdown_text.splitlines()
        html_parts = []
        in_list = False
        list_type = None
        current_list = []

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if not line:
                if in_list:
                    html_parts.append(cls._process_list(current_list, list_type))
                    current_list = []
                    in_list = False
                    list_type = None
                html_parts.append("")
                i += 1
                continue

            if line.startswith("###"):
                if in_list:
                    html_parts.append(cls._process_list(current_list, list_type))
                    current_list = []
                    in_list = False
                    list_type = None
                html_parts.append(f"<h3>{line[3:].strip()}</h3>")
            elif line.startswith("##"):
                if in_list:
                    html_parts.append(cls._process_list(current_list, list_type))
                    current_list = []
                    in_list = False
                    list_type = None
                html_parts.append(f"<h2>{line[2:].strip()}</h2>")
            elif line.startswith("#"):
                if in_list:
                    html_parts.append(cls._process_list(current_list, list_type))
                    current_list = []
                    in_list = False
                    list_type = None
                html_parts.append(f"<h1>{line[1:].strip()}</h1>")

            elif line.startswith("- ") or line.startswith("* "):
                if not in_list or list_type != "ul":
                    if in_list:
                        html_parts.append(cls._process_list(current_list, list_type))
                        current_list = []
                    in_list = True
                    list_type = "ul"
                current_list.append(line[2:])

            elif re.match(r"^\d+\. ", line):
                if not in_list or list_type != "ol":
                    if in_list:
                        html_parts.append(cls._process_list(current_list, list_type))
                        current_list = []
                    in_list = True
                    list_type = "ol"
                current_list.append(line[line.index(".") + 2 :])

            else:
                if in_list:
                    html_parts.append(cls._process_list(current_list, list_type))
                    current_list = []
                    in_list = False
                    list_type = None

                paragraph = line
                while (
                    i + 1 < len(lines)
                    and lines[i + 1].strip()
                    and not lines[i + 1].strip().startswith(("#", "-", "*", "1"))
                ):
                    i += 1
                    paragraph += " " + lines[i].strip()

                paragraph = cls._process_inline_elements(paragraph)
                html_parts.append(f"<p>{paragraph}</p>")

            i += 1

        if in_list:
            html_parts.append(cls._process_list(current_list, list_type))

        html = "\n".join(filter(None, html_parts))
        logger.debug("Markdownテキストの変換が完了しました。")
        return html

    @classmethod
    def _process_inline_elements(cls, text: str) -> str:
        """
        インライン要素（強調、リンクなど）を処理します。

        :param text: 処理するテキスト
        :return: HTML形式に変換されたテキスト
        """
        text = text.replace("**", "<strong>", 1)
        while "**" in text:
            text = text.replace("**", "</strong>", 1)

        text = text.replace("*", "<em>", 1)
        while "*" in text:
            text = text.replace("*", "</em>", 1)
        text = text.replace("`", "<code>", 1)
        while "`" in text:
            text = text.replace("`", "</code>", 1)

        return text

    @classmethod
    def _process_list(cls, items: List[str], list_type: str) -> str:
        """
        リスト要素を処理します。

        :param items: リストアイテムのリスト
        :param list_type: リストのタイプ（'ul' または 'ol'）
        :return: HTML形式のリスト
        """
        if not items:
            return ""

        tag = list_type
        list_items = "\n".join(
            [f"<li>{cls._process_inline_elements(item)}</li>" for item in items]
        )
        return f"<{tag}>\n{list_items}\n</{tag}>"

    @classmethod
    def convert_html_to_string_array(cls, html_content):
        """
        単一のHTML要素を文字列に変換します。
        """
        html_str = ""
        try:
            if isinstance(html_content, BeautifulSoup):
                html_str = str(html_content)
            elif isinstance(html_content, str):
                html_str = html_content
            elif isinstance(html_content, bytes):
                html_str = html_content.decode("utf-8", errors="ignore")
            elif hasattr(html_content, "__html__"):
                html_str = html_content.__html__()
            else:
                html_str = str(html_content)
            html_str = html.unescape(html_str)
            logger.debug("HTMLコンテンツを正常に変換しました。")

        except Exception as e:
            logger.error(f"HTMLコンテンツの変換中にエラーが発生しました: {str(e)}")
            html_str = ""

        return html_str

    @staticmethod
    def split_string_to_lines(content: str) -> List[str]:
        """
        与えられた文字列を行ごとのリストに分割します。

        :param content: 分割する文字列
        :return: 行のリスト
        """
        logger.debug("Splitting string into lines")
        try:
            lines = content.splitlines()
            logger.debug(f"Successfully split string into {len(lines)} lines")
            return lines
        except Exception as e:
            logger.error(f"Error occurred while splitting string: {e}")
            return []
