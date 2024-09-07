import time
import pyautogui
import time
import pyperclip
import logging


class ChatGPTHandler:
    def __init__(
        self,
        edge_handler,
        keyboard_handler,
        wait_time_after_reload,
        wait_time_after_prompt_short,
        wait_time_after_prompt_long,
        model_type="4o",
        short_wait_time=0.5,
    ):
        self.edge_handler = edge_handler
        self.keyboard_handler = keyboard_handler
        self.wait_time_after_reload = wait_time_after_reload
        self.wait_time_after_prompt_short = wait_time_after_prompt_short
        self.wait_time_after_prompt_long = wait_time_after_prompt_long
        self.model_type = model_type
        self.short_wait_time = short_wait_time

    def press_hotkey(self, key_combination):
        """指定されたキー操作を実行し、待機時間を設ける"""
        pyautogui.hotkey(*key_combination)
        time.sleep(self.short_wait_time)

    def move_to_generate_button(self):
        """プロンプトの生成ボタンに移動する"""
        for _ in range(3):
            self.press_hotkey(["shift", "tab"])
        print("Moved to generate button")

    def move_to_copy_button(self):
        """プロンプトのコピーボタンに移動する"""
        if self.model_type == "4o":
            repeat_count = 7
        elif self.model_type == "4omini":
            repeat_count = 5
        else:
            raise ValueError(f"Invalid ChatGPT model type: {self.model_type}")

        for _ in range(repeat_count):
            self.press_hotkey(["shift", "tab"])
        print("Moved to copy button")

    def paste_and_send_message(self):
        """クリップボードの内容を貼り付け、送信する"""
        pyautogui.hotkey("ctrl", "v")
        time.sleep(self.short_wait_time)
        pyautogui.press("tab")
        time.sleep(self.short_wait_time)
        pyautogui.press("enter")

    def get_generated_content(self):
        """生成されたコンテンツをコピーして返す"""
        self.edge_handler.activate_edge()
        self.keyboard_handler.reload_page(self.wait_time_after_reload)
        self.move_to_copy_button()
        self.press_hotkey(["space"])
        generated_content = pyperclip.paste()
        logging.info("Generated content copied from clipboard")
        return generated_content

    def send_prompt_and_generate_content(self, prompt, repeat_count):
        """プロンプトを送信し、生成ボタンを押す処理を行う"""
        self.edge_handler.activate_edge()
        self.keyboard_handler.reload_page(self.wait_time_after_reload)
        pyperclip.copy(prompt)
        self.paste_and_send_message()
        logging.info("Prompt sent and message generation initiated")
        time.sleep(self.wait_time_after_prompt_long)

        for _ in range(repeat_count):
            self.edge_handler.activate_edge()
            self.keyboard_handler.reload_page(self.wait_time_after_reload)
            self.move_to_generate_button()
            self.press_hotkey(["space"])
            logging.info("Generation button pressed")
            time.sleep(self.wait_time_after_prompt_short)

    def get_content(self, prompt, repeat_count):
        """プロンプトを送信し、生成されたコンテンツを返す"""
        self.send_prompt_and_generate_content(prompt, repeat_count)
        content = self.get_generated_content()
        logging.info("Content retrieved")
        return content
