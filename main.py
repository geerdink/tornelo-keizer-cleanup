from datetime import datetime, timedelta
import re

# File path
export_file_path = "tornelo_export.trf"
results_file_path = "results.trf"

external_players_pattern = r"^001\s+(\d+)\s+(\d+), extern\s.*$"
external_player_ids = []

date_line_pattern = r"132\s+(24/09/09\s+).*"

# Read the file content
with open(export_file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

for line in lines:
    match = re.match(external_players_pattern, line)
    if match:
        # Extract the two numbers from the matched line
        player_id = match.group(1)  # The first number (e.g., 30)
        external_player_ids.append(player_id)

print(f"Found external player IDs: {external_player_ids}")

# Function to generate a list of increasing weekly dates
def generate_weekly_dates(start_date_str, count):
    start_date = datetime.strptime(start_date_str, "%y/%m/%d")
    dates = [(start_date + timedelta(days=7 * i)).strftime("%y/%m/%d") for i in range(count)]
    return dates

updated_lines = []
for line in lines:
    # Check if the line contains "132" and subsequent long date sequence
    match = re.match(r"(132\s+)(.*?24/09/09.*?)(\s+)", line)
    if match:
        prefix, extracted_dates, spaces = match.groups()

        first_date = re.search(r"(24/09/09)", extracted_dates).group(0)
        weekly_dates = generate_weekly_dates(first_date, 25)  # Create weekly increments for 25 slots

        formatted_correct_dates = "  ".join(map(str, weekly_dates))

        corrected_line = prefix + formatted_correct_dates + spaces
        updated_lines.append(corrected_line + "\n")

    # Filter out lines that start with "001   30      1, extern"
    elif not re.match(r"^001\s+\d+\s+\d+, extern\s", line):
        updated_lines.append(line)

for external_player_id in external_player_ids:
    # Pattern to match lines with "{player_id} b 0  " where b and 0 can be any character
    # matches any line where the external_player_id is followed by two single characters separated by spaces
    external_matches_pattern = fr"\s{external_player_id}\s+[bw]\s+\d+"
    print(f"Removing matches for external player {external_player_id} with pattern {external_matches_pattern}...")

    # Replace matches in each line
    updated_lines = [
        re.sub(
            external_matches_pattern,
            lambda m: " " * len(m.group(0)),  # Replace with spaces of the same length as the match
            line
        )
        for line in updated_lines
    ]


# Write the updated content back to the file
with open(results_file_path, "w", encoding="utf-8") as file:
    file.writelines(updated_lines)

print("Done!")
