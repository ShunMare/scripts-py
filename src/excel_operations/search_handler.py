from typing import List, Optional
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class ExcelSearchHandler:
    @staticmethod
    def find_matching_index(worksheet, index, search_string, is_row_flag):
        """
        指定された行または列の中から、指定された文字列に一致する最初のセルのインデックスを返す。

        :param worksheet: 検索対象のExcelワークシート
        :param index: 検索する行または列のインデックス（行の場合は row、列の場合は column）
        :param search_string: 検索する文字列
        :param is_row_flag: Trueの場合は行内で検索し、Falseの場合は列内で検索
        :return: 一致するセルが見つかった場合、その列または行のインデックスを返す。見つからない場合は None を返す。
        """
        search_type = "row" if is_row_flag else "column"
        logger.info(f"Starting search: '{search_string}' in {search_type} {index}")

        if is_row_flag:
            max_range = worksheet.max_column
            logger.debug(f"Searching all {max_range} columns in row {index}")
            for col in range(1, max_range + 1):
                cell_value = worksheet.cell(row=index, column=col).value
                if cell_value is not None:
                    logger.debug(f"Cell ({index}, {col}) value: {cell_value}")
                    if str(cell_value).strip() == str(search_string).strip():
                        logger.info(f"Match found: column {col}")
                        return col
        else:
            max_range = worksheet.max_row
            logger.debug(f"Searching all {max_range} rows in column {index}")
            for row in range(1, max_range + 1):
                cell_value = worksheet.cell(row=row, column=index).value
                if cell_value is not None:
                    logger.debug(f"Cell ({row}, {index}) value: {cell_value}")
                    if str(cell_value).strip() == str(search_string).strip():
                        logger.info(f"Match found: row {row}")
                        return row

        logger.warning(f"No match found for '{search_string}' in {search_type} {index}")
        return None

    @staticmethod
    def find_multiple_matching_indices(
        worksheet, index: int, search_strings: List[str], is_row_flag: bool
    ) -> List[Optional[int]]:
        """
        指定された行または列の中から、複数の指定された文字列に一致するセルのインデックスを返す。

        :param worksheet: 検索対象のExcelワークシート
        :param index: 検索する行または列のインデックス
        :param search_strings: 検索する文字列のリスト
        :param is_row_flag: Trueの場合は行内で検索し、Falseの場合は列内で検索
        :return: 各検索文字列に対応するインデックスのリスト。見つからない場合はNoneが含まれる。
        """
        search_type = "row" if is_row_flag else "column"
        logger.info(f"Starting multiple search: {len(search_strings)} strings in {search_type} {index}")

        results = []
        for search_string in search_strings:
            result = ExcelSearchHandler.find_matching_index(
                worksheet, index, search_string, is_row_flag
            )
            results.append(result)
            if result is not None:
                logger.info(f"Match found for '{search_string}': {search_type} {result}")
            else:
                logger.warning(f"No match found for '{search_string}'")

        logger.info(f"Multiple search completed: results = {results}")
        return results
