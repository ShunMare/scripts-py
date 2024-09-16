import pandas as pd

from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class ExcelDataProcessor:
    @staticmethod
    def remove_nan_from_list(text_list):
        original_length = len(text_list)
        processed_list = [text for text in text_list if pd.notna(text)]
        removed_count = original_length - len(processed_list)
        logger.info(
            f"Removed {removed_count} NaN values from list. Original length: {original_length}, New length: {len(processed_list)}"
        )
        return processed_list
