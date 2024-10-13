from .file_handler import ExcelFileHandler
from .sheet_handler import ExcelSheetHandler
from .cell_handler import ExcelCellHandler
from .search_handler import ExcelSearchHandler
from .pandas_handler import ExcelPandasHandler
from .data_processor import ExcelDataProcessor
from src.log_operations.log_handlers import CustomLogger


class ExcelManager:
    """
    Excelファイルを管理するためのクラス。
    様々な操作を行うためのハンドラーを集約し、高レベルのインターフェースを提供する。
    """

    def __init__(self):
        """
        ExcelManagerの初期化
        """
        self.logger = CustomLogger(__name__)
        self.sheet_handler = ExcelSheetHandler()
        self.cell_handler = ExcelCellHandler()
        self.search_handler = ExcelSearchHandler()
        self.data_processor = ExcelDataProcessor()
        self.file_handler = ExcelFileHandler()
        self.pandas_handler = ExcelPandasHandler()
        self.workbook = None
        self.worksheet = None

    def set_workbook(self, file_path=None):
        """
        操作対象のExcelファイルのパスを設定し、ワークブックを読み込む
        :param file_path: (オプション) Excelファイルのパス
        """
        if file_path:
            self.file_handler.set_file_path(file_path)
            self.pandas_handler.set_file_path(file_path)
            self.logger.debug(f"Setting file path: {file_path}")

        if not self.file_handler:
            self.logger.error("File path not set. Please set a file path first.")
            return False

        self.logger.debug("Loading workbook")
        self.workbook = self.file_handler.load()
        if self.workbook:
            self.sheet_handler.set_workbook(self.workbook)
            self.logger.debug("Workbook loaded successfully")
        else:
            self.logger.error("Failed to load workbook")
        return self.workbook is not None

    def set_worksheet(self, sheet_name):
        """
        指定されたシートをアクティブにする
        :param sheet_name: アクティブにするシートの名前
        """
        self.logger.debug(f"Setting active sheet: {sheet_name}")
        self.worksheet = self.sheet_handler.set_active_sheet(sheet_name)
        self.search_handler.set_worksheet(self.worksheet)
        self.cell_handler.set_worksheet(self.worksheet)
        if self.worksheet:
            self.logger.debug(f"Sheet '{sheet_name}' set as active")
        else:
            self.logger.error(f"Failed to set sheet '{sheet_name}' as active")
        return self.worksheet is not None

    def set_info(self, file_path, sheet_name):
        if not self.set_workbook(file_path):
            self.logger.error("Failed to set workbook")
            return None

        if not self.set_worksheet(sheet_name):
            self.logger.error("Failed to set worksheet")
            return None

        return True