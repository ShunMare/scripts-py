import openpyxl
import time

from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class ExcelFileHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        logger.info(f"ExcelFileHandler initialized with file path: {file_path}")

    def load(self):
        try:
            workbook = openpyxl.load_workbook(self.file_path)
            logger.info(f"Successfully loaded Excel file: {self.file_path}")
            return workbook
        except Exception as e:
            logger.error(f"Failed to load Excel file {self.file_path}: {str(e)}")
            return None

    def save(self, workbook, max_retries=3):
        for attempt in range(max_retries):
            try:
                workbook.save(self.file_path)
                logger.info(f"Excel file {self.file_path} saved successfully.")
                return True
            except PermissionError:
                logger.warning(
                    f"PermissionError: Attempt {attempt + 1} of {max_retries} to save {self.file_path}. Retrying in 5 seconds..."
                )
                time.sleep(5)
        logger.error(
            f"Failed to save Excel file {self.file_path} after {max_retries} attempts."
        )
        return False
