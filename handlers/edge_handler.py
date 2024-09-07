import time
import pygetwindow as gw
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import webbrowser


class EdgeHandler:
    def __init__(
        self, wait_time_after_switch=2, driver_path="C:/path/to/msedgedriver.exe"
    ):
        self.wait_time_after_switch = wait_time_after_switch
        self.driver_path = driver_path
        self.driver = None

    def start_edge_driver(self):
        """Selenium Edge WebDriverを起動する"""
        service = Service(self.driver_path)
        options = webdriver.EdgeOptions()
        options.add_argument("start-maximized")
        self.driver = webdriver.Edge(service=service, options=options)
        print("Edge WebDriverが起動しました")

    def activate_edge(self):
        """Microsoft Edge ウィンドウをアクティブ化する"""
        edge_windows = gw.getWindowsWithTitle("Edge")
        if edge_windows:
            edge_window = edge_windows[0]
            if not edge_window.isActive:
                edge_window.activate()
            print("Edge window activated")
            time.sleep(self.wait_time_after_switch)
        else:
            print("No Edge window found")

    def open_url_in_browser(self, url):
        """システムのデフォルトブラウザで指定されたURLを開く"""
        try:
            webbrowser.open(url)
            print(f"デフォルトブラウザでURLを開きました: {url}")
            time.sleep(self.wait_time_after_switch)
        except Exception as e:
            print(f"デフォルトブラウザでURLを開く際にエラーが発生しました: {e}")

    def open_url_with_driver(self, url):
        """指定されたURLをMicrosoft Edgeで開く"""
        if self.driver is None:
            self.start_edge_driver()
        try:
            self.driver.get(url)
            print(f"EdgeでURLを開きました: {url}")
            time.sleep(self.wait_time_after_switch)
        except Exception as e:
            print(f"EdgeでURLを開く際にエラーが発生しました: {e}")

    def print_page_source(self):
        print("ページソース:")
        print(self.driver.page_source)
        print("ページソース終了")

    def find_element_with_multiple_methods(self, selector, timeout=20):
        methods = [
            (By.CSS_SELECTOR, selector),
            (By.XPATH, f"//*[contains(@class, '{selector}')]"),
            (By.XPATH, f"//*[contains(text(), '{selector}')]"),
            (By.XPATH, f"//button[contains(@class, '{selector}')]"),
            (By.XPATH, f"//button[contains(text(), '{selector}')]"),
        ]
        for by, sel in methods:
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by, sel))
                )
                print(f"要素が見つかりました。方法: {by}, セレクタ: {sel}")
                return element
            except TimeoutException:
                print(f"要素が見つかりませんでした。方法: {by}, セレクタ: {sel}")
        return None

    def activate_or_open_edge(self, url=None):
        """Edgeをアクティブ化し、URLが指定されている場合は開く"""
        self.activate_edge()
        if url:
            self.open_url_in_edge(url)

    def press_button(self, selector, timeout=20):
        print(f"ボタンを押そうとしています: {selector}")
        element = self.find_element_with_multiple_methods(selector, timeout)
        if element:
            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(true);", element
                )
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", element)
                print(f"ボタンがクリックされました: {selector}")
            except Exception as e:
                print(f"ボタンをクリックする際にエラーが発生しました: {e}")
        else:
            print(f"ボタンが見つかりませんでした: {selector}")

    def check_and_switch_frames(self):
        frames = self.driver.find_elements(By.TAG_NAME, "iframe")
        print(f"見つかったiframeの数: {len(frames)}")
        for i, frame in enumerate(frames):
            try:
                self.driver.switch_to.frame(frame)
                print(f"フレーム {i} に切り替えました")
                self.print_page_source()
                self.driver.switch_to.default_content()
            except Exception as e:
                print(f"フレーム {i} への切り替え時にエラーが発生しました: {e}")

    def switch_to_frame(self, frame_selector, by=By.CSS_SELECTOR, timeout=20):
        try:
            frame = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, frame_selector))
            )
            self.driver.switch_to.frame(frame)
            print(f"Switched to frame: {frame_selector}")
        except Exception as e:
            print(f"Error switching to frame: {e}")

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()
        print("Switched back to default content")

    def quit_edge_driver(self):
        """Edge WebDriverを終了する"""
        if self.driver:
            self.driver.quit()
            print("Edge WebDriverを閉じました")
