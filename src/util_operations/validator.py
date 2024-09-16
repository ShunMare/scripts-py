from typing import List, Any, Callable
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class ValueValidator:
    """
    単一の値または配列の要素を検証し、指定された条件に基づいて値の有効性をチェックするクラス。
    """

    @staticmethod
    def is_single_value_valid(
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
        if value in invalid_values or (custom_check and not custom_check(value)):
            logger.warning(f"無効な値が見つかりました: {value}")
            return False
        logger.info("値は有効です")
        return True

    @staticmethod
    def are_all_array_values_valid(
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
            logger.warning("空の配列が渡されました")
            return False

        for index, item in enumerate(array):
            if not ValueValidator.is_single_value_valid(
                item, invalid_values, custom_check
            ):
                logger.warning(
                    f"無効な要素が見つかりました: インデックス {index}, 値 {item}"
                )
                return False
        logger.info("全ての要素が有効です")
        return True

    @staticmethod
    def get_invalid_indices_in_array(
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
            if not ValueValidator.is_single_value_valid(
                item, invalid_values, custom_check
            )
        ]

        if not invalid_indices:
            logger.info("無効な要素は見つかりませんでした")
        else:
            logger.info(f"{len(invalid_indices)}個の無効な要素が見つかりました")

        return invalid_indices

    @staticmethod
    def has_any_valid_value_in_array(
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
            ValueValidator.is_single_value_valid(item, invalid_values, custom_check)
            for item in array
        )

    @staticmethod
    def has_any_invalid_value_in_array(
        array: List[Any],
        invalid_values: List[Any] = [None, "", False],
        custom_check: Callable[[Any], bool] = None,
    ) -> bool:
        """
        配列に1つでも無効な値が含まれているかをチェックします。

        :param array: チェックする配列
        :param invalid_values: 無効とみなす値のリスト（デフォルトは [None, "", False]）
        :param custom_check: カスタム検証関数（オプション）。要素を受け取り、Falseを返せば無効と判断
        :return: 1つでも無効な値があればTrue、すべて有効ならFalse
        """
        return any(
            not ValueValidator.is_single_value_valid(item, invalid_values, custom_check)
            for item in array
        )
