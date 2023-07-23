import yaml

# 1. Dump dict to *.yaml file
my_dict = {
    'str_item': 'Im a string',
    'int_items': [1, 2, 3, 4, 5],
    'bool_items': {'true_item': True, 'false_item': False}
}

with open('my_yaml_dump.yml', 'w') as f:
    yaml.dump(my_dict, f)

# 2. Read *.yaml file content to dict
with open('my_yaml_dump.yml', 'r') as f:
    loaded_from_file_dict = yaml.safe_load(f)
