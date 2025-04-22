import yaml
import os

def load_event_definitions(path="config/event_definitions") -> dict:
    definitions = {}
    for file in os.listdir(path):
        if file.endswith(".yaml"):
            with open(os.path.join(path, file), "r") as f:
                data = yaml.safe_load(f)
                definitions.update(data)
    return definitions

def load_base_event_fields(path="config/base_event_fields.yaml") -> dict:
    with open(path, "r") as f:
        schema = yaml.safe_load(f)
    return {field: None for field in schema.keys()}

class BaseEventFields:
    def __init__(self, schema_path="config/base_event_fields.yaml"):
        self.schema = self._load_schema(schema_path)

    def _load_schema(self, path):
        with open(path, "r") as f:
            raw = yaml.safe_load(f)
        return list(raw.keys())

    def build(self, context):
        context_dict = context.to_dict()
        return {field: context_dict.get(field, None) for field in self.schema}
