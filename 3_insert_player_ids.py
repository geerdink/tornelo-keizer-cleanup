source_file = "results_first_half.txt"
target_file = "results3.trf"
output_file = "merged_output.txt"

# Load lines
with open(source_file, "r") as f:
    source_lines = f.readlines()

with open(target_file, "r") as f:
    target_lines = f.readlines()

# Create a map from the first 47 chars to the substring 32–69
source_map = {}
for line in source_lines:
    if len(line) >= 69:
        key = line[:47]
        value = line[31:69]  # Python index 31 to 68 inclusive
        source_map[key] = value

# Modify target lines
modified_lines = []
for line in target_lines:
    key = line[:47]
    if key in source_map and len(line) >= 69:
        new_line = line[:37] + source_map[key] + line[69:]
        modified_lines.append(new_line)
    else:
        modified_lines.append(line)

# Write to output
with open(output_file, "w") as f:
    f.writelines(modified_lines)
