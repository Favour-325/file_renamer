import os
import string

def get_user_preferences():
    """
    Get user preferences for the renaming operation
    """
    print("=== File Renaming Automation ===")
    
    # Get the directory containing files to rename
    directory = input("Enter the directory path (or press Enter for current directory): ").strip()
    if not directory:
        directory = os.getcwd()  # Use current directory if none provided
    
    # Get common name for files
    common_name = input("Enter the common name for all files: ").strip()
    if not common_name:
        print("Error: Common name cannot be empty!")
        return None
    
    # Choose numbering style
    print("\nChoose numbering style:")
    print("1. Numbers (file_1, file_2, ...)")
    print("2. Letters (file_a, file_b, ...)")
    
    while True:
        try:
            choice = int(input("Enter your choice (1 or 2): "))
            if choice in [1, 2]:
                break
            else:
                print("Please enter 1 or 2")
        except ValueError:
            print("Please enter a valid number (1 or 2)")
    
    # Get starting index
    while True:
        try:
            start_index = int(input("Enter starting number/letter index (default is 1): ") or "1")
            if start_index >= 0:
                break
            else:
                print("Please enter a non-negative number")
        except ValueError:
            print("Please enter a valid number")
    
    # Get file extension filter
    extension_filter = input("Enter file extension to filter by (e.g., '.jpg', '.png', or press Enter for all files): ").strip().lower()
    
    return {
        'directory': directory,
        'common_name': common_name,
        'numbering_style': choice,
        'start_index': start_index,
        'extension_filter': extension_filter
    }

def get_files_to_rename(directory, extension_filter):
    """
    Get list of files to rename from the specified directory
    """
    try:
        # Get all files in the directory (excluding subdirectories)
        all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        # Filter by extension if specified
        if extension_filter:
            # Ensure the extension starts with a dot
            if not extension_filter.startswith('.'):
                extension_filter = '.' + extension_filter
            
            filtered_files = [f for f in all_files if f.lower().endswith(extension_filter)]
            print(f"Found {len(filtered_files)} files with extension '{extension_filter}'")
            return filtered_files
        else:
            print(f"Found {len(all_files)} files in directory")
            return all_files
    
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found!")
        return None
    except PermissionError:
        print(f"Error: Permission denied to access directory '{directory}'!")
        return None

def generate_suffix(index, numbering_style):
    """
    Generate the suffix based on numbering style and index
    """
    if numbering_style == 1:  # Numbers
        return str(index)
    else:  # Letters
        # Convert number to letters (1=a, 2=b, ..., 27=aa, 28=ab, etc.)
        result = ""
        while index > 0:
            index -= 1
            result = string.ascii_lowercase[index % 26] + result
            index //= 26
        return result

def rename_files(directory, files, common_name, numbering_style, start_index):
    """
    Perform the actual file renaming operation
    """
    renamed_count = 0
    
    print(f"\nRenaming {len(files)} files...")
    
    for i, filename in enumerate(files, start=start_index):
        # Get file extension
        file_extension = os.path.splitext(filename)[1]
        
        # Generate suffix
        suffix = generate_suffix(i, numbering_style)
        
        # Create new filename
        new_filename = f"{common_name}_{suffix}{file_extension}"
        new_filepath = os.path.join(directory, new_filename)
        old_filepath = os.path.join(directory, filename)
        
        # Check if new filename already exists
        if os.path.exists(new_filepath):
            print(f"Warning: {new_filename} already exists! Skipping {filename}")
            continue
        
        try:
            # Rename the file
            os.rename(old_filepath, new_filepath)
            print(f"Renamed: {filename} -> {new_filename}")
            renamed_count += 1
            
        except OSError as e:
            print(f"Error renaming {filename}: {e}")
    
    return renamed_count

def preview_changes(directory, files, common_name, numbering_style, start_index):
    """
    Show a preview of what the renaming will look like
    """
    print("\n=== PREVIEW OF CHANGES ===")
    print("Old names -> New names")
    print("-" * 40)
    
    for i, filename in enumerate(files[:5], start=start_index):  # Show first 5 files as preview
        file_extension = os.path.splitext(filename)[1]
        suffix = generate_suffix(i, numbering_style)
        new_filename = f"{common_name}_{suffix}{file_extension}"
        print(f"{filename} -> {new_filename}")
    
    if len(files) > 5:
        print(f"... and {len(files) - 5} more files")
    
    return input("\nProceed with renaming? (y/n): ").strip().lower() == 'y'

def main():
    """
    Main function to orchestrate the file renaming process
    """
    # Step 1: Get user preferences
    preferences = get_user_preferences()
    if not preferences:
        return
    
    # Step 2: Get list of files to rename
    files = get_files_to_rename(preferences['directory'], preferences['extension_filter'])
    if not files:
        print("No files found to rename!")
        return
    
    # Step 3: Show preview and get confirmation
    if not preview_changes(
        preferences['directory'],
        files,
        preferences['common_name'],
        preferences['numbering_style'],
        preferences['start_index']
    ):
        print("Renaming cancelled by user.")
        return
    
    # Step 4: Perform the renaming
    renamed_count = rename_files(
        preferences['directory'],
        files,
        preferences['common_name'],
        preferences['numbering_style'],
        preferences['start_index']
    )
    
    # Step 5: Show summary
    print(f"\n=== RENAMING COMPLETE ===")
    print(f"Successfully renamed {renamed_count} out of {len(files)} files")

# Run the script
if __name__ == "__main__":
    main()