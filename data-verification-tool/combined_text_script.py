import os

def combine_text_files(folder_path, output_file):
    with open(output_file, 'w', encoding='utf-8') as combined_file:
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8-sig') as file:
                    content = file.read().replace('\n', '').strip()  # Read content, remove newlines, and strip whitespace
                    if content:  # Check if content is not empty
                        combined_file.write(content + '\n')  # Write content to combined file with a newline

    print(f"Combined all text files in {folder_path} into {output_file}")

# Example usage:
folder_path = 'C:/Users/PMLS/Desktop/LE Work/incorrect_data H/incorrect_data/texts'  # Replace with the path to your folder containing .txt files
output_file = 'C:/Users/PMLS/Desktop/LE Work/incorrect_data H/incorrect_data/combined_text.txt'  # Name of the output combined file

combine_text_files(folder_path, output_file)
