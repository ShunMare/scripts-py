from .text_appender import TextAppender
from .text_finder import TextFinder
from .text_handler import TextHandler
from .text_remover import TextRemover
from .text_replacer import TextReplacer


class TextManager:
    """
    テキストを管理するためのクラス。
    様々なテキスト操作を行うためのハンドラーを集約し、高レベルのインターフェースを提供する。
    """

    def __init__(self):
        """
        TextManagerの初期化
        """
        self.text_handler = TextHandler()
        self.text_appender = TextAppender()
        self.text_finder = TextFinder()
        self.text_remover = TextRemover()
        self.text_replacer = TextReplacer()
