input_file = "results.trf"
output_file = "results2.trf"

with open(input_file, "r") as f:
    lines = f.readlines()

# Modify lines 25 to 59 (index 24 to 58)
for i in range(24, 59):  # Python uses 0-based indexing
    if i < len(lines):
        line = lines[i]
        # Remove characters 92 to 232 (index 91 to 231)
        lines[i] = line[:91] + line[231:] if len(line) > 231 else line[:91]

# Save the modified lines to a new file
with open(output_file, "w") as f:
    f.writelines(lines)
