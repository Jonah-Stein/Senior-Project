# Define the file path
file_path = 'data.csv'

# Read the file and filter out empty lines
with open(file_path, 'r') as file:
    lines = file.readlines()
    non_empty_lines = [line for line in lines if line.strip()]

# Write the non-empty lines back to the file
with open(file_path, 'w') as file:
    file.writelines(non_empty_lines)

print("Skipped lines have been removed.")