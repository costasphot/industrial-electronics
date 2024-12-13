import os
import sys
from collections import Counter
from typing import List

DEBUG_MODE = True
debug_mode_checked = False # Global flag to track if debug mode check has run

OUTPUT_DIR = "../outputs"  # Directory for outputs

def ensure_output_dir_exists() -> None:
    """Ensure the output directory exists."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def check_debug_mode() -> None:
    global debug_mode_checked
    if not debug_mode_checked:
        if DEBUG_MODE:
            print("[DEBUG]: Debug mode is enabled.")
        debug_mode_checked = True # Set the flag to True after the first run

def list_files_in_directory() -> List[str]:
    """List all files in the output directory."""
    files = [f for f in os.listdir(OUTPUT_DIR) if os.path.isfile(os.path.join(OUTPUT_DIR, f))]
    return files

def delete_file() -> None:
    """Delete a file selected by the user from the output directory."""
    files = list_files_in_directory()
    if not files:
        print("No files in the 'outputs' directory.")
        return

    print("Files in the current directory:")
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file}")

    try:
        choice = int(input("Enter the number of the file you want to delete: "))
        if 1 <= choice <= len(files):
            file_to_delete = os.path.join(OUTPUT_DIR, files[choice - 1])
            os.remove(file_to_delete)
            print(f"File '{files[choice - 1]}' has been deleted.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")

def create_file() -> None:
    """Create a new file in the output directory after checking for duplicates."""
    ensure_output_dir_exists()

    while True:
        file_name = input("Enter the name of the new file (with or without desired extension): ").strip()

        # Extract the name and extension parts
        base_name, ext = os.path.splitext(file_name)

        # If no extension provided, suggest ".txt" and ask for confirmation
        if not ext:
            default_extension = ".txt"
            print(f"No extension provided. Defaulting to '{base_name}{default_extension}'.")
            confirm = input(f"Do you want to save it as '{base_name}{default_extension}'? (y/n): ").strip().lower()
            if confirm == "y":
                ext = default_extension
            else:
                new_extension = input("Enter the desired extension (e.g., '.log', '.csv'): ").strip()
                if not new_extension.startswith("."):
                    new_extension = "." + new_extension
                ext = new_extension

        # Reconstruct the file name with the confirmed or updated extension
        file_name = base_name + ext
        file_path = os.path.join(OUTPUT_DIR, file_name)

        if os.path.exists(file_path):
            print(f"A file with the name '{file_name}' already exists. Please choose another name.")
        else:
            with open(file_name, "w") as file:
                print(f"File '{file_name}' has been created.")
                file.write("") # Create an empty file.
            break # Exit the loop once the file is created

def main() -> int:
    """Perform the main functionality of managing lists."""
    ensure_output_dir_exists()
    numbers: List[float] = []

    check_debug_mode()

    results_file_path = os.path.join(OUTPUT_DIR, "results.txt")
    # Open the file in append mode so new data is added without overwriting previous entries
    with open(results_file_path, "a") as file:
        length = int(input("How many numbers: "))
        for i in range(0, length):
            numbers.append(float(input(f"Give me number #{i + 1}: ")))

        # Write the initial list
        file.write("Initial list: " + str(numbers) + "\n")

        # Check for duplicates
        counter = Counter(numbers)
        duplicates = {num: count for num, count in counter.items() if count > 1}

        if duplicates:
            warning_message = "[WARNING]: There are duplicates in the list."
            if DEBUG_MODE:
                print(warning_message)
            file.write(warning_message + "\n")

            duplicate_summary = f"Duplicate numbers: {', '.join([str(num) for num in duplicates.keys()])}"
            duplicate_count_summary = f"Number of duplicates: {sum(count - 1 for count in duplicates.values())}\n"

            if DEBUG_MODE:
                print(duplicate_summary)
                print(duplicate_count_summary)

            file.write(duplicate_summary)
            file.write(duplicate_count_summary)

        # Sort the list
        numbers.sort()
        print(numbers)

        # Write the final sorted list
        file.write("Sorted numbers: " + str(numbers) + "\n")

        # Add a separator for clarity between sessions
        file.write("\n")

    return 0

def menu() -> None:
    """Display the menu and handle user input."""
    while True:
        print("\nMenu:")
        print("1. Delete a file")
        print("2. Create a new file")
        print("3. Perform list operations")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            delete_file()
        elif choice == "2":
            create_file()
        elif choice == "3":
            main()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
