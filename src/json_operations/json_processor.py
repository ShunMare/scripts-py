import json
from typing import Any, Dict, Union
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class JSONProcessor:
    @staticmethod
    def sanitize_for_json(obj):
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, list):
            return [JSONProcessor.sanitize_for_json(item) for item in obj]
        elif isinstance(obj, dict):
            return {
                str(key): JSONProcessor.sanitize_for_json(value)
                for key, value in obj.items()
            }
        else:
            return str(obj)

    @staticmethod
    def to_json(data):
        sanitized_data = JSONProcessor.sanitize_for_json(data)
        try:
            return json.dumps(sanitized_data, ensure_ascii=False)
        except Exception as e:
            logger.debug(f"Error serializing to JSON: {e}")
            return str(sanitized_data)

    @staticmethod
    def from_json(json_str):
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.debug(f"Error deserializing JSON: {e}")
            return None


class JSONParser:
    @staticmethod
    def get_value(data: Any, *keys: str, default: Any = None) -> Any:
        """
        Get a value from nested dictionaries.

        :param data: The dictionary containing the data.
        :param keys: A variable number of string keys to navigate the nested structure.
        :param default: Default value to return if the key is not found.
        :return: The value at the specified location, or the default value if not found.
        """
        current = data
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key, default)
                if current == default:
                    return default
            else:
                return default
        return current

    @staticmethod
    def get_all_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get all data as a flat dictionary.

        :param data: The dictionary containing the data.
        :return: A dictionary with dot-notated keys for all nested data.
        """

        def flatten(d: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
            result = {}
            for key, value in d.items():
                new_key = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    result.update(flatten(value, new_key))
                else:
                    result[new_key] = value
            return result

        return flatten(data)

    @staticmethod
    def load(config_path: str) -> Union[Dict[str, Any], None]:
        """
        Load and parse a JSON configuration file.

        :param config_path: The path to the JSON configuration file.
        :return: A dictionary containing the parsed JSON data, or None if an error occurs.
        """
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.debug(f"設定ファイルの読み込みに失敗しました: {e}")
            return None
