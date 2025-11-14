import json

def to_json(obj):

    def to_serializable(obj):
        if hasattr(obj, "__dict__"):
            return {key: to_serializable(value) for key, value in obj.__dict__.items()}
        elif isinstance(obj, list):
            return [to_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: to_serializable(value) for key, value in obj.items()}
        else:
            return str(obj)   

    return json.dumps(to_serializable(obj), ensure_ascii=False,)




