import os
import yaml

# List of data.yaml files to check for duplicate image filenames
data_yaml_files = ['/path/to/train/data.yaml', '/path/to/val/data.yaml']

# Set to keep track of image filenames
image_filenames = set()

# Iterate over each data YAML file and check for duplicate image filenames
for data_yaml_file in data_yaml_files:
    with open(data_yaml_file, 'r') as f:
        data = yaml.safe_load(f)
        images = data['train'] + data['val']
        for image in images:
            filename = os.path.basename(image['path'])
            if filename in image_filenames:
                print(f"WARNING: Duplicate filename '{filename}' found in '{data_yaml_file}'")
            else:
                image_filenames.add(filename)
