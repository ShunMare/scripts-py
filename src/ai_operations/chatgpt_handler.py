import time
import pyautogui
import time
import pyperclip
import logging

from src.input_operations.keyboard_handler import KeyboardHandler
from src.web_operations.edge_handler import EdgeHandler
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)
keyboard_handler = KeyboardHandler()
edge_handler = EdgeHandler()

class ChatGPTHandler:
    """
    ChatGPTとのインタラクションを自動化するためのハンドラークラス。
    Edgeブラウザ上でのChatGPTの操作を管理します。
    """

    def __init__(
        self,
        wait_time_after_reload,
        wait_time_after_prompt_short,
        wait_time_after_prompt_long,
        model_type="4o",
        short_wait_time=0.5,
    ):
        """
        ChatGPTHandlerの初期化
        :param wait_time_after_reload: ページリロード後の待機時間
        :param wait_time_after_prompt_short: プロンプト送信後の短い待機時間
        :param wait_time_after_prompt_long: プロンプト送信後の長い待機時間
        :param model_type: 使用するChatGPTのモデルタイプ（'4o'または'4omini'）
        :param short_wait_time: 短い操作間の待機時間
        """
        self.wait_time_after_reload = wait_time_after_reload
        self.wait_time_after_prompt_short = wait_time_after_prompt_short
        self.wait_time_after_prompt_long = wait_time_after_prompt_long
        self.model_type = model_type
        self.short_wait_time = short_wait_time
        logging.info(f"ChatGPTHandler initialized with model type: {model_type}")

    def press_hotkey(self, key_combination, duration=0.5):
        """
        指定されたキー操作を実行し、待機時間を設ける
        :param key_combination: 押下するキーの組み合わせ
        :param duration: キーを押し続ける時間（秒）。Noneの場合はデフォルトの動作
        """
        pyautogui.hotkey(*key_combination, duration=duration)
        time.sleep(self.short_wait_time)
        logging.debug(
            f"Hotkey pressed: {key_combination}, Duration: {duration if duration is not None else 'default'}"
        )

    def move_to_generate_button(self):
        """プロンプトの生成ボタンに移動する"""
        for _ in range(3):
            self.press_hotkey(["shift", "tab"])
        logging.info("Moved to generate button")

    def move_to_copy_button(self):
        """プロンプトのコピーボタンに移動する"""
        if self.model_type == "4o":
            repeat_count = 5
        elif self.model_type == "4omini":
            repeat_count = 5
        else:
            logging.error(f"Invalid ChatGPT model type: {self.model_type}")
            raise ValueError(f"Invalid ChatGPT model type: {self.model_type}")

        for _ in range(repeat_count):
            self.press_hotkey(["shift", "tab"])
        logging.info("Moved to copy button")

    def paste_and_send_message(self):
        """クリップボードの内容を貼り付け、送信する"""
        pyautogui.hotkey("ctrl", "v")
        time.sleep(self.short_wait_time)
        pyautogui.press("tab")
        time.sleep(self.short_wait_time)
        pyautogui.press("enter")
        logging.info("Message pasted and sent")

    def get_generated_content(self):
        """
        生成されたコンテンツをコピーして返す
        :return: 生成されたコンテンツの文字列
        """
        edge_handler.activate_edge()
        keyboard_handler.reload_page(self.wait_time_after_reload)
        self.move_to_copy_button()
        self.press_hotkey(["enter"])
        generated_content = pyperclip.paste()
        logging.info("Generated content copied from clipboard")
        return generated_content

    def send_prompt_and_generate_content(self, prompt, repeat_count):
        """
        プロンプトを送信し、生成ボタンを押す処理を行う
        :param prompt: 送信するプロンプト
        :param repeat_count: 生成ボタンを押す回数
        """
        edge_handler.activate_edge()
        keyboard_handler.reload_page(self.wait_time_after_reload)
        pyperclip.copy(prompt)
        self.paste_and_send_message()
        logging.info("Prompt sent and message generation initiated")
        time.sleep(self.wait_time_after_prompt_long)

        for i in range(repeat_count):
            edge_handler.activate_edge()
            keyboard_handler.reload_page(self.wait_time_after_reload)
            self.move_to_generate_button()
            self.press_hotkey(["space"])
            logging.info(f"Generation button pressed (iteration {i+1}/{repeat_count})")
            time.sleep(self.wait_time_after_prompt_short)
