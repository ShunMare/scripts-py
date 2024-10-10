from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)
from typing import List


class ArrayCombiner:
    @staticmethod
    def merge_elements(arr: List[str], merge_count: int, suffix: str = '') -> List[str]:
        """
        配列の要素を指定された数だけ結合し、各グループの末尾に指定された文字列を追加して新しい配列を返します。

        :param arr: 入力配列
        :param merge_count: 結合する要素の数
        :param suffix: 各グループの末尾に追加する文字列 (デフォルトは空文字列)
        :return: 結合された要素を含む新しい配列
        """
        if merge_count <= 0:
            logger.error("merge_count must be a positive integer")
            return []

        if not arr:
            logger.warning("Input array is empty")
            return []

        result = []
        temp = []
        for item in arr:
            if item is not None:
                temp.append(str(item))
            if len(temp) == merge_count:
                result.append("".join(temp) + suffix)
                temp = []

        if temp:
            result.append("".join(temp) + suffix)

        logger.info(f"Merged {len(arr)} elements into {len(result)} groups with suffix '{suffix}'")
        return result

class ArrayRemover:
    @staticmethod
    def remove_elements(main_array: List[str], elements_to_remove: List[str]) -> List[str]:
        """
        main_arrayから、elements_to_removeに含まれる文字列を部分一致で含む要素を削除した新しい配列を返します。

        :param main_array: 元の配列
        :param elements_to_remove: 削除する部分文字列を含む配列
        :return: フィルタリングされた新しい配列
        """
        if not main_array:
            logger.warning("main_array is empty")
            return []

        if not elements_to_remove:
            logger.info("elements_to_remove is empty, returning original array")
            return main_array.copy()

        filtered_array = []
        removed_count = 0

        for item in main_array:
            if not any(remove_str in item for remove_str in elements_to_remove):
                filtered_array.append(item)
            else:
                removed_count += 1

        logger.info(f"Removed {removed_count} elements from the array")
        return filtered_array

class ArrayKeeper:
    @staticmethod
    def keep_elements(main_array: List[str], elements_to_keep: List[str]) -> List[str]:
        """
        main_arrayから、elements_to_keepに含まれる文字列を部分一致で含む要素のみを残した新しい配列を返します。

        :param main_array: 元の配列
        :param elements_to_keep: 保持する部分文字列を含む配列
        :return: フィルタリングされた新しい配列
        """
        if not main_array:
            logger.warning("main_array is empty")
            return []

        if not elements_to_keep:
            logger.warning("elements_to_keep is empty, returning empty array")
            return []

        filtered_array = []
        kept_count = 0

        for item in main_array:
            if any(keep_str in item for keep_str in elements_to_keep):
                filtered_array.append(item)
                kept_count += 1

        logger.info(f"Kept {kept_count} elements in the array")
        return filtered_array