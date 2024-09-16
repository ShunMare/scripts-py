import json

class JSONProcessor:
    @staticmethod
    def sanitize_for_json(obj):
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, list):
            return [JSONProcessor.sanitize_for_json(item) for item in obj]
        elif isinstance(obj, dict):
            return {str(key): JSONProcessor.sanitize_for_json(value) for key, value in obj.items()}
        else:
            return str(obj)

    @staticmethod
    def to_json(data):
        sanitized_data = JSONProcessor.sanitize_for_json(data)
        try:
            return json.dumps(sanitized_data, ensure_ascii=False)
        except Exception as e:
            print(f"Error serializing to JSON: {e}")
            return str(sanitized_data)

    @staticmethod
    def from_json(json_str):
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Error deserializing JSON: {e}")
            return None
