import copy
import re
import json
import sys

if len(sys.argv) != 4:
    print("Usage: python script.py <path> <file>")
    sys.exit(1)

path_arg = sys.argv[1]
file_arg = sys.argv[2]
out_arg = sys.argv[3]
# Read the content from file.txt
#with open(path_arg + '/' + file_arg, 'r') as file:
#    data = eval(file.read())  # Assuming the content is a valid Python list
data =[
    {
        "dir": "/disk1/data/cip/admin/abinitio/cip/private_internal/log/abinitio",
        "files": [
            "write_campaign_criteria_package_2024-02-12-12-17-43_2589812291",
            "apply_field_dependencies_to_a360_2024-02-13-03-09-02_4053465700",
            "apply_field_dependencies_to_a360_2024-02-13-03-09-19_4053460339",
            "apply_field_dependencies_to_a360_2024-02-13-10-53-23_4053464726",
            "apply_field_dependencies_to_a360_2024-02-13-10-53-43_4053462649",
            "apply_field_dependencies_to_a360_2024-02-13-10-57-09_4053465648",
            "apply_field_dependencies_to_a360_2024-02-13-10-57-29_4053465192",
            "apply_field_dependencies_to_a360_2024-02-13-10-58-43_4053463485",
            "apply_field_dependencies_to_a360_2024-02-13-10-59-03_4053469344"
        ]
    }
]

file_list = copy.deepcopy(data)

print(type(file_list))

# Iterate over the data and replace numeric portions in filenames
for item in data:
    for i, filename in enumerate(item['files']):
        pattern = r"[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}_[0-9.a-zA-Z]+"

        if re.search(pattern,filename):
           new_filename = re.sub(pattern, lambda match: re.sub(r"\d", ".", match.group()), filename)
           item['files'][i] = new_filename

#        print( re.match(pattern, item['files'][i]))
#        new_filename = re.sub(pattern, lambda match: re.sub(r"\d", "?", match.group()), filename)
#        item['files'][i] = new_filename


#to remove duplicate file pattern
for i in range(len(data)):
  data[i]['files'] = list(set(data[i]['files']))


result_list = []

for pattern in data:
    pattern_dir = pattern["dir"]
    pattern_files = pattern["files"]

    matching_directory = next((directory for directory in file_list if directory["dir"] == pattern_dir), None)

    if matching_directory:
        # Filter and get the latest file for each directory based on the pattern
        for file_pattern in pattern_files:
            filtered_files = [file for file in matching_directory["files"] if re.match(file_pattern, file)]
            latest_file = sorted(filtered_files) if filtered_files else None
            result_list.append({"dir": matching_directory["dir"], "latest_file":  latest_file })

new_result_list = []

for entry in result_list:
    # Get the 'latest_file' list
    latest_files = entry['latest_file']

    # Use slicing to get the last two files
    sorted_list = sorted(latest_files, reverse=True)

    last_n_files = sorted_list[:2]
    # Create a new entry with the same structure but only the last two files
    new_entry = {'dir': entry['dir'], 'latest_file': last_n_files}

    # Add the new entry to the new result list
    new_result_list.append(new_entry)



# Write the modified data back to a file
with open(path_arg + '/' + out_arg , 'w') as output_file:
    json.dump(data, output_file, indent=2)

with open(path_arg + '/' + out_arg + 'new', 'w') as output_file:
    json.dump(new_result_list, output_file, indent=2)
