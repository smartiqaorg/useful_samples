import json

# 1. Dump dict to json str or file
my_dict = {
    'str_item': 'Im a string',
    'int_item': 100,
    'bool_item': True
}

# dict -> json str
my_str = json.dumps(my_dict)
my_str_with_indent = json.dumps(my_dict, indent=2)

print(my_str)
print(my_str_with_indent)

# dict -> json file
with open('my_json_dump.json', 'w') as f:
    json.dump(my_dict, f, indent=2)

# 2. Load json from string/file to dict
dict_loaded_from_str = json.loads(my_str)

with open('my_json_dump.json', 'r') as f:
    dict_loaded_from_file = json.load(f)

a = 0
