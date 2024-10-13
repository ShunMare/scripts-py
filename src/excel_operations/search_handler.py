from typing import List, Dict, Optional
from src.log_operations.log_handlers import setup_logger


class ExcelSearchHandler:
    def __init__(self):
        """
        ExcelSearchHandlerの初期化
        """
        self.logger = setup_logger(__name__)
        self.worksheet = None

    def set_worksheet(self, worksheet):
        """
        ワークシートを設定します。
        :param worksheet: 対象のワークシート
        """
        self.worksheet = worksheet
        self.logger.debug("Worksheet has been set successfully.")

    def find_matching_index(self, index, search_string, is_row_flag):
        """
        指定された行または列の中から、指定された文字列に一致する最初のセルのインデックスを返す。

        :param index: 検索する行または列のインデックス（行の場合は row、列の場合は column）
        :param search_string: 検索する文字列
        :param is_row_flag: Trueの場合は行内で検索し、Falseの場合は列内で検索
        :return: 一致するセルが見つかった場合、その列または行のインデックスを返す。見つからない場合は None を返す。
        """
        search_type = "row" if is_row_flag else "column"
        self.logger.debug(f"Starting search: '{search_string}' in {search_type} {index}")

        if is_row_flag:
            max_range = self.worksheet.max_column
            self.logger.debug(f"Searching all {max_range} columns in row {index}")
            for col in range(1, max_range + 1):
                cell_value = self.worksheet.cell(row=index, column=col).value
                if cell_value is not None:
                    self.logger.debug(f"Cell ({index}, {col}) value: {cell_value}")
                    if str(cell_value).strip() == str(search_string).strip():
                        self.logger.debug(f"Match found: column {col}")
                        return col
        else:
            max_range = self.worksheet.max_row
            self.logger.debug(f"Searching all {max_range} rows in column {index}")
            for row in range(1, max_range + 1):
                cell_value = self.worksheet.cell(row=row, column=index).value
                if cell_value is not None:
                    self.logger.debug(f"Cell ({row}, {index}) value: {cell_value}")
                    if str(cell_value).strip() == str(search_string).strip():
                        self.logger.debug(f"Match found: row {row}")
                        return row

        self.logger.debug(
            f"No match found for '{search_string}' in {search_type} {index}"
        )
        return None

    def find_multiple_matching_indices(
        self, index: int, search_strings: List[str], is_row_flag: bool
    ) -> List[Optional[int]]:
        """
        指定された行または列の中から、複数の指定された文字列に一致するセルのインデックスを返す。

        :param index: 検索する行または列のインデックス
        :param search_strings: 検索する文字列のリスト
        :param is_row_flag: Trueの場合は行内で検索し、Falseの場合は列内で検索
        :return: 各検索文字列に対応するインデックスのリスト。見つからない場合はNoneが含まれる。
        """
        search_type = "row" if is_row_flag else "column"
        self.logger.debug(
            f"Starting multiple search: {len(search_strings)} strings in {search_type} {index}"
        )

        results = []
        for search_string in search_strings:
            result = self.find_matching_index(index, search_string, is_row_flag)
            results.append(result)
            if result is not None:
                self.logger.debug(
                    f"Match found for '{search_string}': {search_type} {result}"
                )
            else:
                self.logger.debug(f"No match found for '{search_string}'")

        self.logger.debug(f"Multiple search completed: results = {results}")
        return results

    def find_and_map_column_indices(
        self, index: int, search_strings: List[str], is_row_flag: bool = True
    ) -> Dict[str, Optional[int]]:
        """
        指定された行または列の中から、複数の指定された文字列に一致するセルのインデックスを
        検索し、検索文字列をキー、インデックスを値とする辞書を返す。

        :param index: 検索する行または列のインデックス
        :param search_strings: 検索する文字列のリスト
        :param is_row_flag: Trueの場合は行内で検索し、Falseの場合は列内で検索（デフォルトはTrue）
        :return: 各検索文字列をキー、対応するインデックスを値とする辞書。
                見つからない場合の値はNone。
        """
        self.logger.debug(
            f"Starting to find and map indices for {len(search_strings)} strings"
        )
        column_indices = self.find_multiple_matching_indices(
            index, search_strings, is_row_flag
        )
        result_dict = dict(zip(search_strings, column_indices))
        self.logger.debug(f"Mapping completed: {result_dict}")
        return result_dict
