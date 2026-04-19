import re
import json
import pandas as pd


def json_to_dict(content):
    match = re.search(r'\{.*\}', content, re.DOTALL)
    if match:
        json_str = match.group()
        try:
            try:
                data_dict = json.loads(json_str)
            except json.JSONDecodeError:
                import ast
                data_dict = ast.literal_eval(json_str)
            return data_dict
        except:
            return json_str
    else:
        return None
