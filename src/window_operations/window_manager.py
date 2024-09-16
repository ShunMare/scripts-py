import win32gui
import pyautogui
import time


class WindowManager:
    """
    WindowManager クラスは、ウィンドウの操作に関する機能を提供します。
    特定のウィンドウを前面に表示したり、キー入力を送信したりする機能があります。
    """

    def __init__(self, wait_time=0.5):
        """
        WindowManager クラスのコンストラクタ

        :param wait_time: キー操作前の待機時間（秒）。デフォルトは0.5秒。
        """
        self.wait_time = wait_time

    def bring_window_to_foreground(self, window_title):
        """
        指定されたタイトルを持つウィンドウを前面に表示します。

        :param window_title: 検索するウィンドウのタイトル（部分一致）
        :return: ウィンドウが見つかり、前面に表示できた場合はTrue、そうでない場合はFalse
        """

        def callback(hwnd, windows):
            if (
                win32gui.IsWindowVisible(hwnd)
                and window_title.lower() in win32gui.GetWindowText(hwnd).lower()
            ):
                windows.append(hwnd)
            return True

        windows = []
        win32gui.EnumWindows(callback, windows)
        if windows:
            hwnd = windows[0]
            win32gui.SetForegroundWindow(hwnd)
            return True
        return False

    def send_keys_to_window(self, window_title, keys):
        """
        指定されたウィンドウにキー入力を送信します。

        :param window_title: 対象ウィンドウのタイトル（部分一致）
        :param keys: 送信するキー入力の文字列
        :return: キー入力の送信に成功した場合はTrue、そうでない場合はFalse
        """
        if self.bring_window_to_foreground(window_title):
            time.sleep(self.wait_time)
            pyautogui.write(keys)
            return True
        return False

    def send_hotkey_to_window(self, window_title, *keys):
        """
        指定されたウィンドウにホットキーを送信します。

        :param window_title: 対象ウィンドウのタイトル（部分一致）
        :param keys: 送信するホットキーの組み合わせ（例: 'ctrl', 'c'）
        :return: ホットキーの送信に成功した場合はTrue、そうでない場合はFalse
        """
        if self.bring_window_to_foreground(window_title):
            time.sleep(self.wait_time)
            pyautogui.hotkey(*keys)
            return True
        return False
