import time
import pygetwindow as gw
import pyperclip
import pyautogui
import webbrowser

from src.log_operations.log_handlers import CustomLogger
from src.input_operations.keyboard_handler import KeyboardHandler

logger = CustomLogger(__name__)


class EdgeHandler:
    """
    Microsoft Edge ブラウザの操作を自動化するためのハンドラークラス。
    Seleniumを使用してEdgeブラウザの制御を行います。
    """

    def __init__(self):
        """
        EdgeHandlerの初期化
        :param wait_time_after_switch: ウィンドウ切り替え後の待機時間（秒）
        """
        self.wait_time_after_prompt_short = 1
        self.wait_time_after_prompt_medium = 5
        self.wait_time_after_prompt_long = 100
        self.wait_time_after_switch = 2

    def set_wait_time_after_prompt_short(self, wait_time_after_prompt_short):
        self.wait_time_after_prompt_short = wait_time_after_prompt_short

    def set_wait_time_after_prompt_long(self, wait_time_after_prompt_long):
        self.wait_time_after_prompt_long = wait_time_after_prompt_long

    def set_wait_time_after_prompt_medium(self, wait_time_after_prompt_medium):
        self.wait_time_after_prompt_medium = wait_time_after_prompt_medium

    def wait_time_after_switch(self, wait_time_after_switch):
        self.wait_time_after_switch = wait_time_after_switch

    def activate_edge(self):
        """Microsoft Edge ウィンドウをアクティブ化する"""
        edge_windows = gw.getWindowsWithTitle("Edge")
        if edge_windows:
            edge_window = edge_windows[0]
            if not edge_window.isActive:
                edge_window.activate()
            logger.debug("Edge window activated")
            time.sleep(self.wait_time_after_switch)
        else:
            logger.debug("No Edge window found")

    def open_url_in_browser(self, url):
        """システムのデフォルトブラウザで指定されたURLを開く"""
        try:
            webbrowser.open(url)
            logger.debug(f"URL opened in default browser: {url}")
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
        logger.debug("Switched back to default content")

    def ui_save_html(self, filename):
        """
        生成されたコンテンツをファイルに保存する
        :param filename: 保存するファイルの名前（パスを含む）
        """
        self.activate_edge()
        time.sleep(self.wait_time_after_prompt_medium)
        pyautogui.hotkey("ctrl", "s")
        time.sleep(self.wait_time_after_prompt_medium)
        pyperclip.copy(filename)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(self.wait_time_after_prompt_medium)
        pyautogui.press("enter")
        time.sleep(self.wait_time_after_prompt_long)
        logger.debug(f"save {filename} as html in downloads")

    def close_tab(self):
        self.activate_edge()
        time.sleep(self.wait_time_after_prompt_short)
        pyautogui.hotkey("ctrl", "w")
        time.sleep(self.wait_time_after_prompt_short)
        logger.debug("close tab")
