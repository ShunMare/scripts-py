import pandas as pd
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class PandasExcelHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        logger.info(f"PandasExcelHandler initialized with file path: {file_path}")

    def load_pandas(self, sheet_name=None):
        try:
            self.df = pd.read_excel(
                self.file_path,
                sheet_name=sheet_name,
                keep_default_na=False,
                na_values=[""],
            )
            logger.info(f"Successfully loaded Excel file: {self.file_path}")
            logger.info(f"Pandas DataFrame shape: {self.df.shape}")
            logger.info(f"Pandas DataFrame columns: {self.df.columns.tolist()}")
            return self.df
        except Exception as e:
            logger.error(
                f"Failed to load Excel file {self.file_path} with pandas: {str(e)}"
            )
            return None

    def get_pandas_column_data(self, column_name):
        if self.df is not None and column_name in self.df.columns:
            data = self.df[column_name].tolist()
            logger.info(f"Retrieved {len(data)} items from column '{column_name}'")
            return data
        else:
            if self.df is None:
                logger.warning("DataFrame is not loaded. Call load_pandas() first.")
            else:
                logger.warning(f"Column '{column_name}' not found in DataFrame.")
            return []
