import pandas as pd
from src.log_operations.log_handlers import setup_logger


class ExcelPandasHandler:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.file_path = None
        self.df = None

    def set_file_path(self, file_path):
        """
        ファイルパスを設定します。
        :param file_path: 対象のワークシート
        """
        self.file_path = file_path
        self.logger.debug("file_path has been set successfully.")

    def load_pandas(self, sheet_name=None):
        try:
            self.df = pd.read_excel(
                self.file_path,
                sheet_name=sheet_name,
                keep_default_na=False,
                na_values=[""],
            )
            self.logger.debug(f"Successfully loaded Excel file: {self.file_path}")
            self.logger.debug(f"Pandas DataFrame shape: {self.df.shape}")
            self.logger.debug(f"Pandas DataFrame columns: {self.df.columns.tolist()}")
            return self.df
        except Exception as e:
            self.logger.error(
                f"Failed to load Excel file {self.file_path} with pandas: {str(e)}"
            )
            return None

    def get_pandas_column_data(self, column_name):
        if self.df is not None and column_name in self.df.columns:
            data = self.df[column_name].tolist()
            self.logger.debug(f"Retrieved {len(data)} items from column '{column_name}'")
            return data
        else:
            if self.df is None:
                self.logger.debug("DataFrame is not loaded. Call load_pandas() first.")
            else:
                self.logger.debug(f"Column '{column_name}' not found in DataFrame.")
            return []
