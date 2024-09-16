import time
import pygetwindow as gw
import webbrowser

from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class EdgeHandler:
    """
    Microsoft Edge ブラウザの操作を自動化するためのハンドラークラス。
    Seleniumを使用してEdgeブラウザの制御を行います。
    """

    def __init__(self, wait_time_after_switch=2):
        """
        EdgeHandlerの初期化
        :param wait_time_after_switch: ウィンドウ切り替え後の待機時間（秒）
        """
        self.wait_time_after_switch = wait_time_after_switch

    def activate_edge(self):
        """Microsoft Edge ウィンドウをアクティブ化する"""
        edge_windows = gw.getWindowsWithTitle("Edge")
        if edge_windows:
            edge_window = edge_windows[0]
            if not edge_window.isActive:
                edge_window.activate()
            logger.info("Edge window activated")
            time.sleep(self.wait_time_after_switch)
        else:
            logger.warning("No Edge window found")

    def open_url_in_browser(self, url):
        """システムのデフォルトブラウザで指定されたURLを開く"""
        try:
            webbrowser.open(url)
            logger.info(f"URL opened in default browser: {url}")
            time.sleep(self.wait_time_after_switch)
        except Exception as e:
            logger.error(f"Error opening URL in default browser: {e}")

    def print_page_source(self):
        """現在のページソースをログに出力する"""
        logger.debug("Page source:")
        logger.debug(self.driver.page_source)
        logger.debug("End of page source")

    def activate_or_open_edge(self, url=None):
        """Edgeをアクティブ化し、URLが指定されている場合は開く"""
        self.activate_edge()
        if url:
            self.open_url_with_driver(url)

    def switch_to_default_content(self):
        """デフォルトのコンテンツに戻る"""
        self.driver.switch_to.default_content()
        logger.info("Switched back to default content")
