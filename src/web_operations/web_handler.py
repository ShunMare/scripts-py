import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Optional, Dict, Any
from src.log_operations.log_handlers import CustomLogger
from src.file_operations.file_processor import FileHandler

logger = CustomLogger(__name__)
file_handler = FileHandler()


class WebFetcher:
    """Webページの取得を担当するクラス"""

    @staticmethod
    def fetch_page(url: str) -> Optional[str]:
        """
        指定されたURLのWebページを取得します。
        :param url: 取得するWebページのURL
        :return: 取得したWebページのHTML内容、エラー時はNone
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            logger.debug(f"ページを正常に取得しました: {url}")
            return response.text
        except requests.RequestException as e:
            logger.error(f"ページの取得中にエラーが発生しました {url}: {e}")
            return None


class HTMLParser:
    """HTML解析を担当するクラス"""

    def __init__(self):
        """
        初期化メソッド
        """
        self.soup = None

    def set_html_content(self, html_content: str):
        """
        HTML内容を設定します。
        :param html_content: 解析するHTML内容
        """
        self.soup = BeautifulSoup(html_content, "html.parser")
        logger.debug("HTMLコンテンツが設定されました")

    def find_tag_content(self, tag: str, **attrs) -> Optional[str]:
        """
        指定されたタグの内容を返します。
        :param tag: 検索するHTMLタグ
        :param attrs: タグの属性（オプション）
        :return: タグの内容、見つからない場合はNone
        """
        if not self.soup:
            logger.error("HTMLコンテンツが設定されていません")
            return None

        result = self.soup.find(tag, attrs)
        if result:
            logger.debug(f"タグ {tag} の内容を見つけました")
            return result.get_text(strip=True)
        else:
            logger.debug(f"タグ {tag} の内容が見つかりませんでした")
            return None

    def find_all_tag_contents(self, tag: str, **attrs) -> List[str]:
        """
        指定されたタグのすべての内容をリストで返します。
        :param tag: 検索するHTMLタグ
        :param attrs: タグの属性（オプション）
        :return: タグの内容のリスト
        """
        if not self.soup:
            logger.error("HTMLコンテンツが設定されていません")
            return []

        results = self.soup.find_all(tag, attrs)
        logger.debug(f"{len(results)}個の {tag} タグを見つけました")
        return [result.get_text(strip=True) for result in results]

    def find_element_attributes(
        self,
        content: str = "",
        tag: str = "",
        class_list: List[str] = None,
        attribute: str = "aria-label",
    ) -> List[str]:
        """
        指定されたタグ、クラス、および属性を持つ要素から属性の値を抽出します。
        :param content: HTML内容（省略時は初期化時のコンテンツを使用）
        :param tag: 検索するHTMLタグ
        :param class_list: タグが持つべきクラスのリスト
        :param attribute: 検索する属性名（デフォルトは "aria-label"）
        :return: 指定された属性の値のリスト
        """
        if content:
            soup = BeautifulSoup(content, "html.parser")
        else:
            soup = self.soup

        if not tag:
            logger.debug("タグが指定されていません。")
            return []

        if class_list is None:
            class_list = []

        elements = soup.find_all(
            tag,
            class_=lambda x: x and all(cls in x.split() for cls in class_list),
        )
        logger.debug(
            f"{len(elements)} 個の <{tag} class='{' '.join(class_list)}'> 要素が見つかりました。"
        )

        attribute_values = []
        for elem in elements:
            attr_value = elem.get(attribute)
            if attr_value:
                attribute_values.append(attr_value)
                logger.debug(f"{attribute} 属性の値を取得しました: {attr_value[:50]}...")
            else:
                logger.debug(
                    f"<{tag} class='{' '.join(class_list)}'> 要素に {attribute} 属性が見つかりませんでした。"
                )

        return attribute_values

    def find_elements_with_attributes(
        self,
        content: str = "",
        tag: str = "div",
        class_name: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None,
    ) -> List[BeautifulSoup]:
        """
        指定されたタグ、クラス、および属性を持つ要素を見つけます。

        :param content: HTML内容（省略時は初期化時のコンテンツを使用）
        :param tag: 検索するHTMLタグ（デフォルトは "div"）
        :param class_name: タグが持つべきクラス名（オプション）
        :param attributes: 検索する属性と値のディクショナリ（オプション）
        :return: 条件に合致するBeautifulSoup要素のリスト
        """
        search_args = {"name": tag}

        if class_name:
            search_args["class_"] = class_name
        if attributes:
            search_args.update(attributes)
        if content:
            soup = BeautifulSoup(content, "html.parser")
        else:
            soup = self.soup

        elements = soup.find_all(**search_args)
        logger.debug(f"{len(elements)} 個の <{tag}> 要素が見つかりました。")
        for i, elem in enumerate(elements, 1):
            logger.debug(f"要素 {i}: {elem.get_text()[:50]}...")
        return elements

    @staticmethod
    def get_element_contents(elements: List[BeautifulSoup]) -> List[str]:
        """
        要素のコンテンツを抽出します。

        :param elements: BeautifulSoup要素のリスト
        :return: 各要素のテキストコンテンツのリスト
        """
        contents = [elem.get_text(strip=True) for elem in elements]

        for i, content in enumerate(contents, 1):
            logger.debug(f"コンテンツ {i}: {content[:50]}...")

        return contents


class LinkExtractor:
    """リンクの抽出を担当するクラス"""

    def __init__(self, html_content: str, base_url: str):
        """
        :param html_content: 解析するHTML内容
        :param base_url: リンクの基準となるURL
        """
        self.soup = BeautifulSoup(html_content, "html.parser")
        self.base_url = base_url

    def extract_links(self) -> List[str]:
        """
        ページ内のすべてのリンクを抽出します。
        :return: 絶対URLのリスト
        """
        links = self.soup.find_all("a", href=True)
        absolute_links = [urljoin(self.base_url, link["href"]) for link in links]
        logger.debug(f"{len(absolute_links)}個のリンクを抽出しました")
        return absolute_links


class ImageExtractor:
    """画像の抽出を担当するクラス"""

    def __init__(self, html_content: str, base_url: str):
        """
        :param html_content: 解析するHTML内容
        :param base_url: 画像URLの基準となるURL
        """
        self.soup = BeautifulSoup(html_content, "html.parser")
        self.base_url = base_url

    def extract_image_urls(self) -> List[str]:
        """
        ページ内のすべての画像URLを抽出します。
        :return: 絶対URLのリスト
        """
        images = self.soup.find_all("img", src=True)
        image_urls = [urljoin(self.base_url, img["src"]) for img in images]
        logger.debug(f"{len(image_urls)}個の画像URLを抽出しました")
        return image_urls


class WebScraper:
    """Webスクレイピングの全体的な処理を統括するクラス"""

    @staticmethod
    def scrape(
        url: str,
        tags_to_extract: List[str],
        aria_tags: Optional[Dict[str, List[str]]] = None,
    ) -> Dict[str, Any]:
        """
        Webページをスクレイピングし、指定されたタグの情報を抽出します。
        :param url: スクレイピング対象のURL
        :param tags_to_extract: 抽出したいタグのリスト
        :param aria_tags: aria-label を抽出したいタグとクラスの辞書（オプション）
        例: {'div': ['content', 'user-select-text']}
        :return: 抽出された情報を含む辞書
        """
        html_content = WebFetcher.fetch_page(url)
        if not html_content:
            logger.error("ページの取得に失敗しました。スクレイピングを中止します。")
            return {}

        parser = HTMLParser(html_content)
        link_extractor = LinkExtractor(html_content, url)
        image_extractor = ImageExtractor(html_content, url)

        results = {}

        for tag in tags_to_extract:
            if tag == "title":
                results[tag] = parser.find_tag_content("title")
                logger.debug(f"ページタイトル: {results[tag]}")
            elif tag == "links":
                results[tag] = link_extractor.extract_links()
                logger.debug(f"抽出されたリンク数: {len(results[tag])}")
            elif tag == "images":
                results[tag] = image_extractor.extract_image_urls()
                logger.debug(f"抽出された画像URL数: {len(results[tag])}")
            else:
                content = parser.find_tag_content(tag)
                if content:
                    results[tag] = content
                    logger.debug(f"{tag}の内容: {content[:50]}...")
                else:
                    logger.debug(f"{tag}の内容が見つかりませんでした")

        if aria_tags:
            for tag, classes in aria_tags.items():
                aria_labels = parser.find_aria_labels(tag, classes)
                results[f"{tag}_aria_labels"] = aria_labels
                logger.debug(
                    f"抽出された {tag} タグの aria-label 数: {len(aria_labels)}"
                )

        return results

    @staticmethod
    def find_elements_with_attributes(
        html_content: str, tag: str, classes: List[str], attribute: str
    ) -> List[str]:
        """
        指定されたタグ、クラス、および属性を持つ要素を抽出します。

        :param html_content: 解析するHTML内容
        :param tag: 検索するHTMLタグ
        :param classes: 要素が持つべきクラスのリスト
        :param attribute: 抽出したい属性
        :return: 指定された属性の値のリスト
        """
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            elements = soup.find_all(
                tag, class_=lambda x: x and all(cls in x.split() for cls in classes)
            )

            attribute_values = [
                elem.get(attribute) for elem in elements if elem.has_attr(attribute)
            ]

            logger.debug(
                f"{len(attribute_values)} 個の {tag} タグ（クラス: {', '.join(classes)}）から {attribute} 属性を抽出しました"
            )
            return attribute_values

        except Exception as e:
            logger.error(f"要素の抽出中にエラーが発生しました: {str(e)}")
            return []

    @staticmethod
    def scrape_with_attributes(
        url: str, tag: str, classes: List[str], attribute: str
    ) -> List[str]:
        """
        指定されたURLからHTMLを取得し、指定されたタグ、クラス、属性を持つ要素を抽出します。

        :param url: スクレイピング対象のURL
        :param tag: 検索するHTMLタグ
        :param classes: 要素が持つべきクラスのリスト
        :param attribute: 抽出したい属性
        :return: 指定された属性の値のリスト
        """
        html_content = WebFetcher.fetch_page(url)
        if not html_content:
            logger.error("ページの取得に失敗しました。スクレイピングを中止します。")
            return []

        return WebScraper.find_elements_with_attributes(
            html_content, tag, classes, attribute
        )

    @staticmethod
    def find_elements(content: str, tag_name: str, class_list: list) -> list:
        """
        HTMLファイルから指定されたタグと指定されたクラスを全て持つ要素を探します。

        :param file_path: HTMLファイルのパス
        :param tag_name: 探したいHTMLタグ名
        :param class_list: 要素が持つべきクラスのリスト
        :return: 条件に合致する要素のリスト
        """
        try:
            soup = BeautifulSoup(content, "html.parser")
            elements = soup.find_all(
                tag_name,
                class_=lambda x: x and all(cls in x.split() for cls in class_list),
            )

            logger.debug(f"{len(elements)} 個の要素が見つかりました。")
            return elements

        except Exception as e:
            logger.error(f"要素の探索中にエラーが発生しました: {str(e)}")
            raise

    @staticmethod
    def find_attributes(content: str, tag: str, attribute: str, **attrs) -> List[str]:
        """
        指定されたタグの指定された属性の内容をリストで返します。
        :param content: 解析するHTML内容
        :param tag: 検索するHTMLタグ
        :param attribute: 取得したい属性（例えば href, src など）
        :param attrs: タグの追加属性（オプション）
        :return: 指定された属性の内容のリスト
        """
        try:
            soup = BeautifulSoup(content, "html.parser")
            elements = soup.find_all(tag, attrs)
            attribute_values = [
                element.get(attribute) for element in elements if element.get(attribute)
            ]
            logger.debug(
                f"{len(attribute_values)} 個の {tag} タグの {attribute} 属性を見つけました"
            )
            return attribute_values
        except Exception as e:
            logger.error(f"属性の抽出中にエラーが発生しました: {str(e)}")
            return []
