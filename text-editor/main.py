from services.EditorService import EditorService
import os

def display_document(editor_service, start_line=0, num_lines=10):
    """
    Display a portion of the document with line numbers.
    
    Args:
        editor_service: The editor service
        start_line (int): Line to start displaying from
        num_lines (int): Number of lines to display
    """
    line_count = editor_service.get_line_count()
    end_line = min(start_line + num_lines, line_count)
    
    print("\nDocument Content:")
    print("----------------")
    
    if line_count == 0:
        print("[Empty document]")
    else:
        for i in range(start_line, end_line):
            print(f"{i+1:4d} | {editor_service.get_line(i)}")
    
    print("----------------")
    
    cursor_row, cursor_col = editor_service.get_cursor_position()
    print(f"Cursor position: Line {cursor_row+1}, Column {cursor_col+1}")
    
    if editor_service.is_modified():
        print("Document has been modified.")
    
    file_path = editor_service.get_file_path()
    if file_path:
        print(f"File: {file_path}")
    else:
        print("New document (not saved)")

def demo_text_editor():
    """Demonstrate the text editor functionality."""
    print("Text Editor Demo")
    print("===============\n")
    
    # Create editor service (Singleton)
    editor_service = EditorService.get_instance()
    
    # Create a new document
    editor_service.new_document()
    print("Created a new document.")
    
    # Display the empty document
    display_document(editor_service)
    
    # Insert some lines
    print("\nInserting lines...")
    editor_service.insert_line(0, "# Text Editor Demo")
    editor_service.insert_line(1, "")
    editor_service.insert_line(2, "This is a simple text editor implementation using clean architecture principles.")
    editor_service.insert_line(3, "It supports the following operations:")
    editor_service.insert_line(4, "- Insert, delete, and replace text")
    editor_service.insert_line(5, "- Undo and redo operations")
    editor_service.insert_line(6, "- Find and replace text")
    editor_service.insert_line(7, "- Save and load documents")
    
    # Display the document
    display_document(editor_service)
    
    # Save the document
    temp_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_document.txt")
    print(f"\nSaving document to {temp_file_path}...")
    if editor_service.save_document(temp_file_path):
        print("Document saved successfully.")
    else:
        print("Failed to save document.")
    
    # Modify the document
    print("\nModifying document...")
    editor_service.replace_line(0, "# Text Editor Demo - Modified")
    editor_service.delete_line(1)  # Delete the empty line
    editor_service.insert_text(2, 0, "* ")  # Add a bullet point
    
    # Display the modified document
    display_document(editor_service)
    
    # Undo operations
    print("\nUndoing operations...")
    editor_service.undo()  # Undo insert_text
    editor_service.undo()  # Undo delete_line
    editor_service.undo()  # Undo replace_line
    
    # Display the document after undo
    display_document(editor_service)
    
    # Redo operations
    print("\nRedoing operations...")
    editor_service.redo()  # Redo replace_line
    editor_service.redo()  # Redo delete_line
    editor_service.redo()  # Redo insert_text
    
    # Display the document after redo
    display_document(editor_service)
    
    # Find and replace text
    print("\nFinding and replacing text...")
    count = editor_service.find_and_replace("simple", "powerful")
    print(f"Replaced {count} occurrences of 'simple' with 'powerful'.")
    
    # Display the document after find and replace
    display_document(editor_service)
    
    # Open the saved document
    print("\nOpening the saved document...")
    if editor_service.open_document(temp_file_path):
        print("Document opened successfully.")
    else:
        print("Failed to open document.")
    
    # Display the opened document
    display_document(editor_service)
    
    # Clean up
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
        print(f"\nRemoved temporary file: {temp_file_path}")

def main():
    """Main function."""
    demo_text_editor()

if __name__ == "__main__":
    main()
