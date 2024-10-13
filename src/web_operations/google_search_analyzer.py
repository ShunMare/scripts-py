import requests
import string
import time
import logging
from typing import List, Dict, Union
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class GoogleSearchAnalyzer:
    """
    Google検索の自動補完機能を利用して関連キーワードを取得し、
    検索結果から見出しを抽出するクラス
    """

    def __init__(
        self, language: str = "ja", country: str = "jp", max_suggestions: int = 10
    ):
        """
        初期化メソッド

        :param language: 検索言語（デフォルト: 日本語）
        :param country: 検索対象国（デフォルト: 日本）
        :param max_suggestions: 取得する最大サジェスト数
        """
        self.language = language
        self.country = country
        self.max_suggestions = max_suggestions
        self.base_url = "https://suggestqueries.google.com/complete/search"
        self.search_url = "https://www.google.com/search"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_suggestions(self, keyword: str) -> List[str]:
        """
        指定されたキーワードに対するGoogleの自動補完サジェストを取得

        :param keyword: 検索キーワード
        :return: サジェストのリスト
        """
        params = {
            "client": "firefox",
            "q": keyword,
            "hl": self.language,
            "gl": self.country,
        }
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            logger.debug(f"Request URL: {response.url}")
            logger.debug(f"Response status code: {response.status_code}")
            if response.status_code == 200:
                suggestions = response.json()[1]
                logger.debug(f"Received suggestions: {suggestions}")
                return suggestions
            else:
                logger.debug(f"Received non-200 status code: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Error fetching suggestions for '{keyword}': {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        return []

    def get_extended_suggestions(self, keyword: str) -> List[str]:
        """
        キーワードとアルファベットを組み合わせた拡張サジェストを取得

        :param keyword: 検索キーワード
        :return: 重複を除いた拡張サジェストのリスト
        """
        suggestions = set()
        suggestions.update(self.get_suggestions(keyword))

        for letter in string.ascii_lowercase:
            if len(suggestions) >= self.max_suggestions:
                break
            new_keyword = f"{keyword} {letter}"
            suggestions.update(self.get_suggestions(new_keyword))
            time.sleep(0.1)

        return list(suggestions)[: self.max_suggestions]

    def get_related_keyword(self, keyword: str) -> List[str]:
        logger.debug(f"Getting related keywords for: {keyword}")
        suggestions = self.get_extended_suggestions(keyword)
        time.sleep(0.5)
        logger.debug(f"Found {len(suggestions)} related keywords")
        return suggestions

    def get_related_keywords_string(
        self, keyword: str, related_keywords: List[str]
    ) -> str:
        """
        関連キーワードを文字列として返す

        :param keyword: 元のキーワード
        :param related_keywords: 関連キーワードのリスト
        :return: フォーマットされた関連キーワードの文字列
        """
        result = f"\nRelated search keywords for '{keyword}':\n"
        if related_keywords:
            for i, related_keyword in enumerate(related_keywords, 1):
                result += f"{i}. {related_keyword}\n"
        else:
            result += "No related keywords found.\n"

        return result

    def extract_headings(
        self, keyword: str, heading_types: List[str] = ["h2", "h3"]
    ) -> List[str]:
        """
        指定されたキーワードでGoogle検索を行い、検索結果ページから指定された見出しを抽出

        :param keyword: 検索キーワード
        :param heading_types: 抽出する見出しのタイプのリスト（デフォルト: ['h2', 'h3']）
        :return: 抽出された見出しのリスト
        """
        params = {
            "q": keyword,
            "hl": self.language,
            "gl": self.country,
        }
        try:
            response = requests.get(
                self.search_url, params=params, headers=self.headers
            )
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                headings = []
                for heading_type in heading_types:
                    headings.extend(
                        [h.text.strip() for h in soup.find_all(heading_type)]
                    )
                return headings
        except requests.RequestException as e:
            logger.error(f"Error fetching search results for '{keyword}': {e}")
        return []

    def extract_heading(
        self, keyword: str, num_results: int = 10
    ) -> List[Dict[str, Union[str, List[str]]]]:
        """
        指定されたキーワードでGoogle検索を行い、上位の検索結果から見出しを抽出

        :param keyword: 検索キーワード
        :param num_results: 取得する検索結果の数（デフォルト: 10）
        :return: URL、h2見出し、h3見出しを含む辞書のリスト
        """
        params = {
            "q": keyword,
            "hl": self.language,
            "gl": self.country,
            "num": num_results,
        }
        results = []
        try:
            response = requests.get(
                self.search_url, params=params, headers=self.headers
            )
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                search_results = soup.find_all("div", class_="g")

                for result in search_results[:num_results]:
                    url_element = result.find("a")
                    if url_element and "href" in url_element.attrs:
                        url = url_element["href"]
                        try:
                            page_response = requests.get(
                                url, headers=self.headers, timeout=5
                            )
                            if page_response.status_code == 200:
                                page_soup = BeautifulSoup(
                                    page_response.text, "html.parser"
                                )
                                h2_headings = [
                                    h2.text.strip() for h2 in page_soup.find_all("h2")
                                ]
                                h3_headings = [
                                    h3.text.strip() for h3 in page_soup.find_all("h3")
                                ]
                                results.append(
                                    {"url": url, "h2": h2_headings, "h3": h3_headings}
                                )
                        except requests.RequestException:
                            logger.debug(f"Error fetching content from {url}")
                        time.sleep(1)
        except requests.RequestException as e:
            logger.error(f"Error fetching search results for '{keyword}': {e}")
        return results

    def print_heading_results(self, results: List[Dict[str, Union[str, List[str]]]]):
        """
        見出し抽出結果を整形して表示

        :param results: URL、h2見出し、h3見出しを含む辞書のリスト
        """
        for i, result in enumerate(results, 1):
            print(f"\n記事 {i}:")
            print(f"URL: {result['url']}")
            print("h2見出し:")
            for h2 in result["h2"]:
                print(f"  - {h2}")
            print("h3見出し:")
            for h3 in result["h3"]:
                print(f"  - {h3}")

    def print_results(
        self, results: Dict[str, List[str]], result_type: str = "関連検索ワード"
    ):
        """
        結果を整形して表示

        :param results: キーワードと結果のマッピング
        :param result_type: 結果のタイプ（例: "関連検索ワード" や "見出し"）
        """
        print(f"\n{result_type}の結果:")
        for keyword, items in results.items():
            print(f"キーワード '{keyword}' の{result_type}:")
            if items:
                for i, item in enumerate(items, 1):
                    print(f"{i}. {item}")
            else:
                print(f"{result_type}が見つかりませんでした。")
