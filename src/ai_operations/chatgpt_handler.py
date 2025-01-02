import time
from typing import Optional
from enum import Enum
import pyautogui
import pyperclip

from src.input_operations.keyboard_handler import KeyboardHandler
from src.log_operations.log_handlers import CustomLogger
from src.web_operations.edge_handler import EdgeHandler

keyboard_handler = KeyboardHandler()
edge_handler = EdgeHandler()
logger = CustomLogger(__name__)


# model type
class ModelType(str, Enum):
    GPT_4O = "4o"
    GPT_4OMINI = "4omini"
    GPTS = "gpts"


# actions
class ShortcutAction(str, Enum):
    NEW_CHAT = "NEW_CHAT"
    CUSTOM_INSTRUCTION = "CUSTOM_INSTRUCTION"
    FOCUS_CHAT_INPUT = "FOCUS_CHAT_INPUT"
    TOGGLE_SIDEBAR = "TOGGLE_SIDEBAR"
    DELETE_CHAT = "DELETE_CHAT"
    COPY_LAST_CODE = "COPY_LAST_CODE"
    COPY_LAST_RESPONSE = "COPY_LAST_RESPONSE"
    SHOW_SHORTCUTS = "SHOW_SHORTCUTS"


class ChatGPTHandler:
    """
    ChatGPTとのインタラクションを自動化するためのハンドラークラス。
    Edgeブラウザ上でのChatGPTの操作を管理します。
    """

    def __init__(self):
        """
        ChatGPTHandlerの初期化
        :param wait_time_after_reload: ページリロード後の待機時間
        :param wait_time_after_prompt_medium: プロンプト送信後の短い待機時間
        :param wait_time_after_prompt_long: プロンプト送信後の長い待機時間
        :param model_type: 使用するChatGPTのモデルタイプ（'4o'または'4omini'）
        :param short_wait_time: 短い操作間の待機時間
        """
        self.wait_time_after_reload = 0
        self.wait_time_after_prompt_short = 0
        self.wait_time_after_prompt_medium = 0
        self.wait_time_after_prompt_long = 0
        self.model_type = ""
        self.short_wait_time = 0
        self.tab_count = 6

    def set_info(
        self,
        wait_time_after_reload,
        wait_time_after_prompt_short,
        wait_time_after_prompt_medium,
        wait_time_after_prompt_long,
        model_type,
        short_wait_time,
        tab_count_4o,
        tab_count_4omini,
        tab_count_gpts,
    ):
        self.wait_time_after_reload = wait_time_after_reload
        self.wait_time_after_prompt_short = wait_time_after_prompt_short
        self.wait_time_after_prompt_medium = wait_time_after_prompt_medium
        self.wait_time_after_prompt_long = wait_time_after_prompt_long
        self.model_type = model_type
        self.short_wait_time = short_wait_time
        match self.model_type:
            case ModelType.GPT_4O:
                self.tab_count = tab_count_4o
            case ModelType.GPT_4OMINI:
                self.tab_count = tab_count_4omini
            case ModelType.GPTS:
                self.tab_count = tab_count_gpts
            case _:
                logger.error(f"Invalid ChatGPT model type: {self.model_type}")
                raise ValueError(f"Invalid ChatGPT model type: {self.model_type}")

    def press_hotkey(self, key_combination, duration=0.5):
        """
        指定されたキー操作を実行し、待機時間を設ける
        :param key_combination: 押下するキーの組み合わせ
        :param duration: キーを押し続ける時間（秒）。Noneの場合はデフォルトの動作
        """
        pyautogui.hotkey(*key_combination, duration=duration)
        time.sleep(self.short_wait_time)
        logger.debug(
            f"Hotkey pressed: {key_combination}, Duration: {duration if duration is not None else 'default'}"
        )

    def execute_shortcut(self, action: ShortcutAction) -> None:
        """
        指定されたアクションに対応するショートカットを実行する
        :param action: 実行するショートカットアクション
        :raises ValueError: 不明なアクションが指定された場合
        """
        match action:
            case ShortcutAction.NEW_CHAT:
                self.press_hotkey(["ctrl", "shift", "o"])
            case ShortcutAction.CUSTOM_INSTRUCTION:
                self.press_hotkey(["ctrl", "shift", "i"])
            case ShortcutAction.FOCUS_CHAT_INPUT:
                self.press_hotkey(["shift", "esc"])
            case ShortcutAction.TOGGLE_SIDEBAR:
                self.press_hotkey(["ctrl", "shift", "s"])
            case ShortcutAction.DELETE_CHAT:
                self.press_hotkey(["ctrl", "shift", "backspace"])
            case ShortcutAction.COPY_LAST_CODE:
                self.press_hotkey(["ctrl", "shift", ";"])
            case ShortcutAction.COPY_LAST_RESPONSE:
                self.press_hotkey(["ctrl", "shift", "c"])
            case ShortcutAction.SHOW_SHORTCUTS:
                self.press_hotkey(["ctrl", "/"])
            case _:
                logger.error(f"Unknown action: {action}")
                raise ValueError(f"Unknown action: {action}")
        logger.debug(f"Executed shortcut for action: {action}")

    def focus_chat_input(self):
        """チャット入力欄にフォーカスを移動する"""
        self.execute_shortcut(ShortcutAction.FOCUS_CHAT_INPUT)

    def delete_chat(self):
        """チャットを削除する"""
        self.execute_shortcut(ShortcutAction.DELETE_CHAT)
        self.press_hotkey(["enter"])

    def move_to_generate_button(self):
        """プロンプトの生成ボタンに移動する"""
        for _ in range(self.tab_count - 2):
            self.press_hotkey(["shift", "tab"])
        logger.debug("Moved to generate button")

    def move_to_copy_button(self):
        """プロンプトのコピーボタンに移動する"""
        for _ in range(self.tab_count):
            self.press_hotkey(["shift", "tab"])
        logger.debug("Moved to copy button")

    def paste_and_send_message(self):
        """クリップボードの内容を貼り付け、送信する"""
        self.press_hotkey(["ctrl", "v"])
        for _ in range(self.tab_count):
            self.press_hotkey(["tab"])
        self.press_hotkey(["enter"])
        logger.debug("Message pasted and sent")

    def get_generated_content_copy_button(self):
        """
        生成されたコンテンツをコピーして返す
        :return: 生成されたコンテンツの文字列
        """
        edge_handler.activate_edge()
        keyboard_handler.reload_page(self.wait_time_after_reload)
        self.move_to_copy_button()
        self.press_hotkey(["enter"])
        generated_content = pyperclip.paste()
        logger.debug("Generated content copied from clipboard")
        return generated_content

    def get_generated_content(self):
        """
        生成されたコンテンツをコピーして返す
        :return: 生成されたコンテンツの文字列
        """
        edge_handler.activate_edge()
        self.execute_shortcut(ShortcutAction.COPY_LAST_RESPONSE)
        generated_content = pyperclip.paste()
        logger.debug("Generated content copied")
        return generated_content

    def send_prompt_and_generate_content(
        self, prompt: str, repeat_count: int = 0, is_reload: Optional[bool] = False
    ):
        """
        プロンプトを送信し、生成ボタンを押す処理を行う
        :param prompt: 送信するプロンプト
        :param repeat_count: 生成ボタンを押す回数
        :param is_reload: 最初の実行かどうか（デフォルトはTrue）
        """
        edge_handler.activate_edge()

        if is_reload:
            keyboard_handler.reload_page(self.wait_time_after_reload)

        self.focus_chat_input()
        pyperclip.copy(prompt)
        self.paste_and_send_message()
        logger.debug("Prompt sent and message generation initiated")
        time.sleep(self.wait_time_after_prompt_long)

        for i in range(repeat_count):
            edge_handler.activate_edge()
            self.focus_chat_input()
            self.move_to_generate_button()
            self.press_hotkey(["enter"])
            logger.debug(f"Generation button pressed (iteration {i+1}/{repeat_count})")
            time.sleep(self.wait_time_after_prompt_medium)
