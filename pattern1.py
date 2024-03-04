import re
import json
import sys
import copy

if len(sys.argv) != 4:
    print("Usage: python script.py <path> <file>")
    sys.exit(1)

path_arg = sys.argv[1]
file_arg = sys.argv[2]
out_arg = sys.argv[3]




# Read the content from file.txt
with open(path_arg + '/' + file_arg, 'r') as file:
    data = file.read()



# Your pattern to match sequences of 14 digits
#pattern = r'\b\d{8,}\b'
pattern1 = r'\d{8,14}'

# Function to replace numeric portions with '?'
#def replace_numeric(match):
#    return '?' * len(match.group())

# Apply the replacement using re.sub to the content
#modified_content = json.loads(re.sub(pattern, replace_numeric, content))

data = json.loads(data)

for item in data:
    for i, filename in enumerate(item['files']):
        if re.search(pattern1, filename):
            new_filename = re.sub(pattern1, lambda match: '?' * len(match.group()), filename)
            item['files'][i] = new_filename
        else:
            pass

#print(type(modified_content))

#modified_content = json.loads(modified_content)
#print(type(modified_content ))
#print(json.load(modified_content))
#print(modified_content[0]['files'])

for i in range(len(data)):
  data[i]['files'] = list(set(data[i]['files']))




with open(path_arg + '/' + out_arg, 'w') as outfile:
    json.dump(data, outfile, indent=2)


