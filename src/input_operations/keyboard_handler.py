import time
import pyautogui
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class KeyboardHandler:
    def __init__(self, short_wait_time=0.5):
        self.short_wait_time = short_wait_time
        logger.info(
            f"KeyboardHandler initialized with short_wait_time: {short_wait_time}"
        )

    def press_hotkey(self, key_combination):
        """指定されたキー操作を実行し、待機時間を設ける"""
        pyautogui.hotkey(*key_combination)
        time.sleep(self.short_wait_time)

    def move_to_generate_button(self):
        """プロンプトの生成ボタンに移動する"""
        for _ in range(3):
            self.press_hotkey(["shift", "tab"])
        logger.info("Moved to generate button")

    def move_to_copy_button(self):
        """プロンプトのコピーボタンに移動する"""
        for _ in range(7):
            self.press_hotkey(["shift", "tab"])
        logger.info("Moved to copy button")

    def reload_page(self, wait_time_after_reload):
        """ページをリロードする"""
        pyautogui.hotkey("ctrl", "r")
        time.sleep(wait_time_after_reload)
        logger.info(f"Page reloaded, waited for {wait_time_after_reload} seconds")

    def copy_to_clipboard(self):
        """選択された内容をクリップボードにコピーする"""
        pyautogui.hotkey("ctrl", "c")
        time.sleep(1)
        logger.info("Content copied to clipboard")
