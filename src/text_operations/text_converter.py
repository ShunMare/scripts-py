from bs4 import Tag, NavigableString
import re
from typing import List
import html
from bs4 import BeautifulSoup
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class TextConverter:
    @classmethod
    def convert_to_markdown(cls, element: Tag) -> str:
        """
        HTMLエレメントをMarkdown形式に変換します。

        :param element: 変換するBeautifulSoupのTagオブジェクト
        :return: 変換されたMarkdown文字列
        """
        logger.info("HTMLエレメントのMarkdown変換を開始します。")
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
            logger.info("HTMLコンテンツを正常に変換しました。")

        except Exception as e:
            logger.error(f"HTMLコンテンツの変換中にエラーが発生しました: {str(e)}")
            html_str = ""

        return html_str
