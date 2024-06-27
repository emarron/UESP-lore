# Function to load and sort the contents of a file
def load_and_sort(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        # Remove any trailing newline characters and sort in descending order
        sorted_lines = sorted([line.strip() for line in lines], reverse=False)
    return sorted_lines


# Load and sort titles_a.txt
titles_a = load_and_sort('titles_a.txt')
print("Sorted titles_a:")

# Load and sort titles_b.txt
titles_b = load_and_sort('titles_b.txt')
print("Sorted titles_b:")
