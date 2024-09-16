from .file_handler import ExcelFileHandler
from .sheet_handler import ExcelSheetHandler
from .cell_handler import ExcelCellHandler
from .search_handler import ExcelSearchHandler
from .pandas_handler import PandasExcelHandler
from .data_processor import ExcelDataProcessor
from src.log_operations.log_handlers import setup_logger


class ExcelManager:
    """
    Excelファイルを管理するためのクラス。
    様々な操作を行うためのハンドラーを集約し、高レベルのインターフェースを提供する。
    """

    def __init__(self, file_path):
        """
        ExcelManagerの初期化
        :param file_path: 操作対象のExcelファイルのパス
        """
        self.logger = setup_logger(__name__)
        self.logger.info(f"Initializing ExcelManager for file: {file_path}")
        self.file_handler = ExcelFileHandler(file_path)
        self.sheet_handler = ExcelSheetHandler()
        self.cell_handler = ExcelCellHandler()
        self.search_handler = ExcelSearchHandler()
        self.pandas_handler = PandasExcelHandler(file_path)
        self.data_processor = ExcelDataProcessor()
        self.workbook = None
        self.current_sheet = None

    def load_workbook(self):
        """ワークブックを読み込む"""
        self.logger.info("Loading workbook")
        self.workbook = self.file_handler.load()
        if self.workbook:
            self.logger.info("Workbook loaded successfully")
        else:
            self.logger.error("Failed to load workbook")
        return self.workbook is not None

    def save_workbook(self):
        """ワークブックを保存する"""
        self.logger.info("Saving workbook")
        result = self.file_handler.save(self.workbook)
        if result:
            self.logger.info("Workbook saved successfully")
        else:
            self.logger.error("Failed to save workbook")
        return result

    def get_sheet_names(self):
        """ワークブック内のすべてのシート名を取得する"""
        self.logger.info("Getting sheet names")
        return self.sheet_handler.get_sheet_names(self.workbook)

    def set_active_sheet(self, sheet_name):
        """
        指定されたシートをアクティブにする
        :param sheet_name: アクティブにするシートの名前
        """
        self.logger.info(f"Setting active sheet: {sheet_name}")
        self.current_sheet = self.sheet_handler.set_active_sheet(
            self.workbook, sheet_name
        )
        if self.current_sheet:
            self.logger.info(f"Sheet '{sheet_name}' set as active")
        else:
            self.logger.error(f"Failed to set sheet '{sheet_name}' as active")
        return self.current_sheet is not None

    def update_cell(self, row, column, value):
        """
        指定されたセルの値を更新する
        :param row: 更新するセルの行
        :param column: 更新するセルの列
        :param value: セットする新しい値
        """
        self.logger.info(
            f"Updating cell at row {row}, column {column} with value: {value}"
        )
        return self.cell_handler.update_cell(self.current_sheet, row, column, value)

    def is_cell_empty_or_match(self, row, column, expected_value=None):
        """
        指定されたセルが空かどうか、または期待値と一致するかをチェックする
        :param row: チェックするセルの行
        :param column: チェックするセルの列
        :param expected_value: 期待される値（オプション）
        """
        self.logger.info(f"Checking cell at row {row}, column {column}")
        return self.cell_handler.is_cell_empty_or_match(
            self.current_sheet, row, column, expected_value
        )

    def find_matching_index(self, index, search_string, is_row_flag):
        """
        指定された文字列に一致する行または列のインデックスを検索する
        :param index: 検索を開始するインデックス
        :param search_string: 検索する文字列
        :param is_row_flag: Trueの場合は行を検索、Falseの場合は列を検索
        :return: 見つかった場合はインデックス、見つからなかった場合はNone
        """
        search_type = "rows" if is_row_flag else "columns"
        self.logger.info(f"Searching for '{search_string}' in {search_type}")

        result = self.search_handler.find_matching_index(
            self.current_sheet, index, search_string, is_row_flag
        )
        if result is None:
            self.logger.error(f"No match found for '{search_string}' in {search_type}")
        else:
            self.logger.info(f"Match found for '{search_string}' at index {result}")
        return result

    def load_pandas(self, sheet_name=None):
        """
        ExcelファイルをPandasデータフレームとして読み込む
        :param sheet_name: 読み込むシート名（オプション）
        """
        self.logger.info(
            f"Loading Excel file into Pandas DataFrame, sheet: {sheet_name or 'default'}"
        )
        return self.pandas_handler.load_pandas(sheet_name)

    def get_pandas_column_data(self, column_name):
        """
        指定された列名のデータをPandasデータフレームから取得する
        :param column_name: 取得するデータの列名
        """
        self.logger.info(f"Getting data from column: {column_name}")
        return self.pandas_handler.get_pandas_column_data(column_name)

    def remove_nan_from_list(self, text_list):
        """
        リストからNaN値を除去する
        :param text_list: 処理するテキストのリスト
        :return: NaN値が除去されたリストと、除去された要素数
        """
        self.logger.info("Starting to remove NaN values from list")

        original_length = len(text_list)
        cleaned_list = self.data_processor.remove_nan_from_list(text_list)
        removed_count = original_length - len(cleaned_list)
        self.logger.info(f"Removed {removed_count} NaN values from list")
        self.logger.info(
            f"Original list length: {original_length}, New list length: {len(cleaned_list)}"
        )
        if removed_count > 0:
            self.logger.warning(f"Removed {removed_count} NaN values from the list")
        else:
            self.logger.info("No NaN values were found in the list")

        return cleaned_list, removed_count
