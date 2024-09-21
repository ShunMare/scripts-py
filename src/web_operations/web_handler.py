import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Optional, Dict, Any
from src.log_operations.log_handlers import setup_logger
from src.file_operations.file_processor import FileHandler

logger = setup_logger(__name__)
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
            logger.info(f"ページを正常に取得しました: {url}")
            return response.text
        except requests.RequestException as e:
            logger.error(f"ページの取得中にエラーが発生しました {url}: {e}")
            return None


class HTMLParser:
    """HTML解析を担当するクラス"""

    def __init__(self, html_content: str):
        """
        :param html_content: 解析するHTML内容
        """
        self.soup = BeautifulSoup(html_content, "html.parser")

    def find_tag_content(self, tag: str, **attrs) -> Optional[str]:
        """
        指定されたタグの内容を返します。
        :param tag: 検索するHTMLタグ
        :param attrs: タグの属性（オプション）
        :return: タグの内容、見つからない場合はNone
        """
        result = self.soup.find(tag, attrs)
        if result:
            logger.info(f"タグ {tag} の内容を見つけました")
            return result.get_text(strip=True)
        else:
            logger.warning(f"タグ {tag} の内容が見つかりませんでした")
            return None

    def find_all_tag_contents(self, tag: str, **attrs) -> List[str]:
        """
        指定されたタグのすべての内容をリストで返します。
        :param tag: 検索するHTMLタグ
        :param attrs: タグの属性（オプション）
        :return: タグの内容のリスト
        """
        results = self.soup.find_all(tag, attrs)
        logger.info(f"{len(results)}個の {tag} タグを見つけました")
        return [result.get_text(strip=True) for result in results]

    def find_aria_labels(self, tag: str, class_list: List[str]) -> List[str]:
        """
        指定されたタグとクラスを持つ要素から aria-label 属性の値を抽出します。
        :param tag: 検索するHTMLタグ
        :param class_list: タグが持つべきクラスのリスト
        :return: aria-label 属性の値のリスト
        """
        elements = self.soup.find_all(
            tag,
            class_=lambda x: x and all(cls in x.split() for cls in class_list),
        )
        logger.info(
            f"{len(elements)} 個の <{tag} class='{ ' '.join(class_list) }'> 要素が見つかりました。"
        )

        aria_labels = []
        for elem in elements:
            aria_label = elem.get("aria-label")
            if aria_label:
                aria_labels.append(aria_label)
                logger.info(f"aria-label 属性の値を取得しました: {aria_label}")
            else:
                logger.warning(
                    f"<{tag} class='{ ' '.join(class_list) }'> 要素に aria-label 属性が見つかりませんでした。"
                )

        return aria_labels


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
        logger.info(f"{len(absolute_links)}個のリンクを抽出しました")
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
        logger.info(f"{len(image_urls)}個の画像URLを抽出しました")
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
                logger.info(f"ページタイトル: {results[tag]}")
            elif tag == "links":
                results[tag] = link_extractor.extract_links()
                logger.info(f"抽出されたリンク数: {len(results[tag])}")
            elif tag == "images":
                results[tag] = image_extractor.extract_image_urls()
                logger.info(f"抽出された画像URL数: {len(results[tag])}")
            else:
                content = parser.find_tag_content(tag)
                if content:
                    results[tag] = content
                    logger.info(f"{tag}の内容: {content[:50]}...")
                else:
                    logger.warning(f"{tag}の内容が見つかりませんでした")

        if aria_tags:
            for tag, classes in aria_tags.items():
                aria_labels = parser.find_aria_labels(tag, classes)
                results[f"{tag}_aria_labels"] = aria_labels
                logger.info(
                    f"抽出された {tag} タグの aria-label 数: {len(aria_labels)}"
                )

        return results

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

            logger.info(f"{len(elements)} 個の要素が見つかりました。")
            return elements

        except Exception as e:
            logger.error(f"要素の探索中にエラーが発生しました: {str(e)}")
            raise
