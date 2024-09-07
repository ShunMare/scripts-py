import time
import pyautogui
import time
import pyperclip
import logging

# ログの設定
logging.basicConfig(
    level=logging.DEBUG,  # ログの詳細度をDEBUGレベルに設定
    format="%(asctime)s [%(levelname)s] %(message)s",  # ログのフォーマットを指定
    handlers=[
        logging.StreamHandler(),  # コンソールに出力
        logging.FileHandler("bing_handler.log"),  # ファイルに出力
    ],
)


class BingHandler:
    def __init__(
        self,
        edge_handler,
        keyboard_handler,
        wait_time_after_reload,
        wait_time_after_prompt_short,
        wait_time_after_prompt_long,
        short_wait_time=0.5,
    ):
        self.edge_handler = edge_handler
        self.keyboard_handler = keyboard_handler
        self.wait_time_after_reload = wait_time_after_reload
        self.wait_time_after_prompt_short = wait_time_after_prompt_short
        self.wait_time_after_prompt_long = wait_time_after_prompt_long
        self.short_wait_time = short_wait_time

        logging.debug(
            f"BingHandler initialized with wait times: "
            f"reload={wait_time_after_reload}, short={wait_time_after_prompt_short}, "
            f"long={wait_time_after_prompt_long}"
        )

    def press_hotkey(self, key_combination):
        """指定されたキー操作を実行し、待機時間を設ける"""
        pyautogui.hotkey(*key_combination)
        time.sleep(self.short_wait_time)
        logging.debug(f"Pressed hotkey: {key_combination}")

    def move_to_generate_button(self):
        """プロンプトの生成ボタンに移動する"""
        for _ in range(3):
            self.press_hotkey(["shift", "tab"])
        logging.info("Moved to generate button")

    def press_sign_in_button(self):
        """サインインボタンを押す"""
        for _ in range(1):
            self.press_hotkey(["shift", "tab"])
            time.sleep(self.short_wait_time)
        pyautogui.press("space")
        time.sleep(self.wait_time_after_reload)
        logging.info("Pressed sign-in button")

    def press_conversation_style_button(self):
        """会話スタイルボタンを押す"""
        for _ in range(1):
            self.press_hotkey(["shift", "tab"])
            time.sleep(self.short_wait_time)
        pyautogui.press("space")
        time.sleep(self.short_wait_time)
        logging.info("Pressed conversation style button")

    def move_to_copy_button(self):
        """プロンプトのコピーボタンに移動する"""
        for _ in range(7):
            self.press_hotkey(["shift", "tab"])
        logging.info("Moved to copy button")

    def move_to_inout_box(self):
        """プロンプトのインプットに移動する"""
        for _ in range(8):
            self.press_hotkey(["tab"])
        logging.info("Moved to input box")

    def paste_and_send_message(self):
        """クリップボードの内容を貼り付け、送信する"""
        pyautogui.hotkey("ctrl", "v")
        time.sleep(self.short_wait_time)
        for i in range(3):
            pyautogui.press("tab")
            time.sleep(self.short_wait_time)
        pyautogui.press("enter")
        logging.info("Pasted and sent message")

    def get_generated_content(self):
        """生成されたコンテンツをコピーして返す"""
        self.edge_handler.activate_edge()
        self.move_to_copy_button()
        self.press_hotkey(["space"])
        generated_content = pyperclip.paste()
        logging.info("Generated content copied from clipboard")
        return generated_content

    def send_prompt(self, prompt, isFirst):
        """プロンプトを送信し、生成ボタンを押す処理を行う"""
        self.edge_handler.activate_edge()
        pyperclip.copy(prompt)
        if not isFirst:
            self.move_to_inout_box()
        self.paste_and_send_message()
        logging.info(f"Prompt sent")
        time.sleep(self.wait_time_after_prompt_long)
        logging.info(f"Waited for {self.wait_time_after_prompt_long} seconds")

    def get_content(self, prompt, isFirst):
        """プロンプトを送信し、生成されたコンテンツを返す"""
        self.send_prompt(prompt, isFirst)
        content = self.get_generated_content()
        logging.info("Content retrieved")
        return content
