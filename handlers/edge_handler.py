import time
import pygetwindow as gw

class EdgeHandler:
    def __init__(self, wait_time_after_switch=2):
        self.wait_time_after_switch = wait_time_after_switch

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
