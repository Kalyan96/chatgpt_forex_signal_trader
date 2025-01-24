def read_nth_line_from_file(file_path, n):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if 1 <= n <= len(lines):
                return lines[n - 1].strip()
            else:
                print(f"Error: Line {n} does not exist in the file.")
                return None
    except FileNotFoundError:
        print("Error: File not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage:
file_path = "forex_gpt_prompt.txt"  # Replace 'example.txt' with the path to your text file.
line_number = 2  # Replace this with the line number you want to retrieve.
nth_line = read_nth_line_from_file(file_path, line_number)
if nth_line:
    # print(f"Line {line_number}: {nth_line}")
    print(nth_line)
