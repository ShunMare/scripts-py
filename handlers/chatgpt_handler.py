import time
import pyautogui


class ChatGPTHandler:
    def __init__(self, model_type="4o", short_wait_time=0.5):
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
