import logging
import colorama
import os

colorama.init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """カラー付きのフォーマッタクラス"""

    COLORS = {
        "DEBUG": colorama.Fore.BLUE,
        "INFO": colorama.Fore.GREEN,
        "WARNING": colorama.Fore.YELLOW,
        "ERROR": colorama.Fore.RED,
        "CRITICAL": colorama.Fore.RED + colorama.Back.WHITE,
    }

    def format(self, record):
        log_message = super().format(record)
        return f"{self.COLORS.get(record.levelname, '')}{log_message}{colorama.Style.RESET_ALL}"


def setup_logger(name, level=logging.INFO, log_folder="logs"):
    """
    ロガーをセットアップし、設定されたロガーを返す

    :param name: ロガーの名前
    :param level: ログレベル（デフォルトはINFO）
    :param log_folder: ログファイルを保存するフォルダ（デフォルトは'logs'）
    :return: 設定されたロガーオブジェクト
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(level)
    logger.propagate = False

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(
        ColoredFormatter(
            "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
    )
    logger.addHandler(console_handler)

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file_path = os.path.join(log_folder, f"{name}.log")
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(level)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
    )
    logger.addHandler(file_handler)

    def prominent_log(self, message, level=logging.INFO, box_width=60):
        border = "#" * box_width
        padded_message = f"## {message.center(box_width - 6)} ##"
        log_message = f"\n{border}\n{padded_message}\n{border}"
        self.log(level, log_message)

    logger.prominent_log = prominent_log.__get__(logger)

    return logger


logging.getLogger().handlers = []
