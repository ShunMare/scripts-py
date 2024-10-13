import openpyxl
import time

from src.log_operations.log_handlers import CustomLogger


class ExcelFileHandler:
    def __init__(self):
        self.logger = CustomLogger(__name__)
        self.file_path = None
        self.workbook = None

    def set_file_path(self, file_path):
        self.file_path = file_path
        self.logger.debug("file_path has been set successfully.")

    def load(self):
        try:
            workbook = openpyxl.load_workbook(self.file_path)
            self.workbook = workbook
            self.logger.debug(f"Successfully loaded Excel file: {self.file_path}")
            return workbook
        except Exception as e:
            self.logger.error(f"Failed to load Excel file {self.file_path}: {str(e)}")
            return None

    def save(self, max_retries=3):
        for attempt in range(max_retries):
            try:
                self.workbook.save(self.file_path)
                self.logger.debug(f"Excel file {self.file_path} saved successfully.")
                return True
            except PermissionError:
                self.logger.debug(
                    f"PermissionError: Attempt {attempt + 1} of {max_retries} to save {self.file_path}. Retrying in 5 seconds..."
                )
                time.sleep(5)
        self.logger.error(
            f"Failed to save Excel file {self.file_path} after {max_retries} attempts."
        )
        return False
