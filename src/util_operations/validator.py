from typing import List, Any, Union, Dict, Callable
from src.log_operations.log_handlers import setup_logger
from src.text_operations.text_replacer import TextReplacer
from src.text_operations.text_handler import TextHandler

logger = setup_logger(__name__)
text_replacer = TextReplacer()
text_handler = TextHandler()


class ValueValidator:
    """
    単一の値または配列の要素を検証し、指定された条件に基づいて値の有効性をチェックするクラス。
    """

    @staticmethod
    def is_valid(
        value: Any,
        invalid_values: List[Any] = [None, "", False],
        custom_check: Callable[[Any], bool] = None,
    ) -> bool:
        """
        単一の値が有効（指定された無効値リストに含まれていない）かどうかをチェックします。

        :param value: チェックする値
        :param invalid_values: 無効とみなす値のリスト（デフォルトは [None, "", False]）
        :param custom_check: カスタム検証関数（オプション）。値を受け取り、Falseを返せば無効と判断
        :return: 値が有効な場合はTrue、そうでない場合はFalse
        """
        display_value = text_handler.generate_display_value(value, 10)
        if value in invalid_values or (custom_check and not custom_check(value)):
            logger.warning(f"Invalid value found: {display_value}")
            return False
        logger.info(f"Value is valid: {display_value}")
        return True

    @staticmethod
    def all_valid(
        array: List[Any],
        invalid_values: List[Any] = [None, "", False],
        custom_check: Callable[[Any], bool] = None,
    ) -> bool:
        """
        配列内の全ての要素が有効かどうかをチェックします。

        :param array: チェックする配列
        :param invalid_values: 無効とみなす値のリスト（デフォルトは [None, "", False]）
        :param custom_check: カスタム検証関数（オプション）。要素を受け取り、Falseを返せば無効と判断
        :return: 全ての要素が有効な場合はTrue、そうでない場合はFalse
        """
        if not array:
            logger.warning("Empty array was passed")
            return False

        for index, item in enumerate(array):
            if not ValueValidator.is_valid(item, invalid_values, custom_check):
                logger.warning(f"Invalid element found: index {index}, value {item}")
                return False
        logger.info("All elements are valid")
        return True

    @staticmethod
    def any_valid(
        array: List[Any],
        invalid_values: List[Any] = [None, "", False],
        custom_check: Callable[[Any], bool] = None,
    ) -> bool:
        """
        配列に1つでも有効な値が含まれているかをチェックします。

        :param array: チェックする配列
        :param invalid_values: 無効とみなす値のリスト（デフォルトは [None, "", False]）
        :param custom_check: カスタム検証関数（オプション）。要素を受け取り、Falseを返せば無効と判断
        :return: 1つでも有効な値があればTrue、すべて無効ならFalse
        """
        return any(
            ValueValidator.is_valid(item, invalid_values, custom_check)
            for item in array
        )

    @staticmethod
    def any_invalid(
        data: Any,
        invalid_values: List[Any] = [None, "", False],
        custom_check: Callable[[Any], bool] = None,
    ) -> bool:
        """
        配列またはディクショナリに1つでも無効な値が含まれているかをチェックします。

        :param data: チェックする配列またはディクショナリ
        :param invalid_values: 無効とみなす値のリスト（デフォルトは [None, "", False]）
        :param custom_check: カスタム検証関数（オプション）。要素を受け取り、Falseを返せば無効と判断
        :return: 1つでも無効な値があればTrue、すべて有効ならFalse
        """
        if isinstance(data, dict):
            values_to_check = data.values()
        elif isinstance(data, list):
            values_to_check = data
        else:
            raise ValueError("Input must be either a list or a dictionary")

        return any(
            not ValueValidator.is_valid(item, invalid_values, custom_check)
            for item in values_to_check
        )

    @staticmethod
    def find_invalid_indices(
        array: List[Any],
        invalid_values: List[Any] = [None, "", False],
        custom_check: Callable[[Any], bool] = None,
    ) -> List[int]:
        """
        配列内の無効な要素のインデックスのリストを返します。

        :param array: チェックする配列
        :param invalid_values: 無効とみなす値のリスト（デフォルトは [None, "", False]）
        :param custom_check: カスタム検証関数（オプション）。要素を受け取り、Falseを返せば無効と判断
        :return: 無効な要素のインデックスのリスト
        """
        invalid_indices = [
            index
            for index, item in enumerate(array)
            if not ValueValidator.is_valid(item, invalid_values, custom_check)
        ]

        if not invalid_indices:
            logger.info("No invalid elements found")
        else:
            logger.info(f"Found {len(invalid_indices)} invalid elements")

        return invalid_indices
