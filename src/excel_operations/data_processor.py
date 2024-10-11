import pandas as pd
from src.log_operations.log_handlers import setup_logger


class ExcelDataProcessor:
    def __init__(self):
        """
        ExcelDataProcessorの初期化
        """
        self.logger = setup_logger(__name__)

    def remove_nan_from_list(self, text_list):
        original_length = len(text_list)
        processed_list = [text for text in text_list if pd.notna(text)]
        removed_count = original_length - len(processed_list)
        self.logger.info(
            f"Removed {removed_count} NaN values from list. Original length: {original_length}, New length: {len(processed_list)}"
        )
        return processed_list
