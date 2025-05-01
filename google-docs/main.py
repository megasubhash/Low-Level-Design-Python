from models.DocumentManager import DocumentManager
from services.DocumentService import DocumentService
from enums.DocumentPermission import DocumentPermission
from enums.OperationType import OperationType
import time

def print_document_info(document):
    """Print document information."""
    print(f"Document ID: {document.id}")
    print(f"Title: {document.title}")
    print(f"Owner: {document.owner_id}")
    print(f"Version: {document.version}")
    print(f"Content: {document.content}")
    print(f"Last Updated: {document.updated_at}")
    print(f"Permissions: {len(document.permissions)} users")
    print(f"Active Users: {len(document.active_users)} users")
    print("-" * 50)

def test_basic_functionality():
    """Test basic document creation and editing."""
    print("\n=== Testing Basic Functionality ===")
    
    # Create service and manager
    service = DocumentService()
    manager = DocumentManager(service)
    
    # Create users
    user1_id = manager.create_user("Alice", "alice@example.com")
    user2_id = manager.create_user("Bob", "bob@example.com")
    
    print(f"Created users: Alice ({user1_id}), Bob ({user2_id})")
    
    # Create a document
    doc_id = manager.create_document("Meeting Notes", "# Meeting Agenda", user1_id)
    document = manager.get_document(doc_id)
    
    print(f"Created document: {document.title} ({doc_id})")
    print_document_info(document)
    
    # Add Bob as an editor
    manager.add_user_to_document(doc_id, user2_id, DocumentPermission.EDITOR)
    print(f"Added Bob as an editor to the document")
    
    # Alice adds content
    manager.update_document(doc_id, user1_id, OperationType.INSERT, 
                           len(document.content), "\n\n1. Review last week's action items")
    document = manager.get_document(doc_id)
    print(f"Alice added content. New version: {document.version}")
    print(f"Content: {document.content}")
    
    # Bob adds content
    manager.update_document(doc_id, user2_id, OperationType.INSERT, 
                           len(document.content), "\n2. Discuss new project timeline")
    document = manager.get_document(doc_id)
    print(f"Bob added content. New version: {document.version}")
    print(f"Content: {document.content}")
    
    return service, manager, doc_id, user1_id, user2_id

def test_conflict_resolution():
    """Test conflict resolution with LastWriteWinsStrategy."""
    print("\n=== Testing Conflict Resolution (LastWriteWins) ===")
    
    # Create service and manager
    service = DocumentService()
    manager = DocumentManager(service)
    
    # Create users
    user1_id = manager.create_user("Alice", "alice@example.com")
    user2_id = manager.create_user("Bob", "bob@example.com")
    
    # Create a document
    doc_id = manager.create_document("Shared Document", "Initial content", user1_id)
    document = manager.get_document(doc_id)
    
    # Add Bob as an editor
    manager.add_user_to_document(doc_id, user2_id, DocumentPermission.EDITOR)
    
    print(f"Initial document content: '{document.content}'")
    
    # Simulate Alice and Bob editing the same part of the document at nearly the same time
    # Alice's change
    print("\nAlice is editing position 8...")
    manager.update_document(doc_id, user1_id, OperationType.DELETE, 8, "content")
    manager.update_document(doc_id, user1_id, OperationType.INSERT, 8, "text")
    
    # Get the updated document
    document = manager.get_document(doc_id)
    print(f"After Alice's edits: '{document.content}'")
    
    # Small delay to ensure Bob's change has a later timestamp
    time.sleep(0.1)
    
    # Bob's change (conflicts with Alice's)
    print("\nBob is editing position 8...")
    manager.update_document(doc_id, user2_id, OperationType.DELETE, 8, "text")
    manager.update_document(doc_id, user2_id, OperationType.INSERT, 8, "data")
    
    # Get the updated document
    document = manager.get_document(doc_id)
    print(f"After Bob's edits: '{document.content}'")
    
    # Get all changes for the document
    changes = manager.get_document_changes(doc_id)
    
    # Print change history
    print("\nChange history:")
    for i, change in enumerate(sorted(changes, key=lambda c: c.timestamp)):
        print(f"{i+1}. {change.timestamp}: User {change.user_id} - {change.operation_type.value} - Status: {change.status.value}")
    
    # Explain the conflict resolution
    print("\nConflict Resolution Explanation:")
    print("The LastWriteWinsStrategy resolves conflicts by prioritizing the most recent changes.")
    print("Since Bob's changes came after Alice's, Bob's edits were applied and any conflicting")
    print("changes from Alice were marked as conflicted and not applied.")
    
    return service, manager, doc_id, user1_id, user2_id

def test_multiple_users():
    """Test multiple users editing a document."""
    print("\n=== Testing Multiple Users ===")
    
    # Create service and manager
    service = DocumentService()
    manager = DocumentManager(service)
    
    # Create users
    users = []
    for i, name in enumerate(["Alice", "Bob", "Charlie", "Diana"]):
        user_id = manager.create_user(name, f"{name.lower()}@example.com")
        users.append(user_id)
        print(f"Created user: {name} ({user_id})")
    
    # Create a document owned by Alice
    doc_id = manager.create_document("Team Document", "# Team Project Plan", users[0])
    document = manager.get_document(doc_id)
    
    print(f"Created document: {document.title} ({doc_id})")
    
    # Add other users with different permissions
    manager.add_user_to_document(doc_id, users[1], DocumentPermission.EDITOR)
    manager.add_user_to_document(doc_id, users[2], DocumentPermission.COMMENTER)
    manager.add_user_to_document(doc_id, users[3], DocumentPermission.VIEWER)
    
    print("Added users with different permissions:")
    print(f"- Alice (Owner): {users[0]}")
    print(f"- Bob (Editor): {users[1]}")
    print(f"- Charlie (Commenter): {users[2]}")
    print(f"- Diana (Viewer): {users[3]}")
    
    # Users make non-conflicting changes
    manager.update_document(doc_id, users[0], OperationType.INSERT, 
                           len(document.content), "\n\n## Project Timeline")
    
    document = manager.get_document(doc_id)
    manager.update_document(doc_id, users[1], OperationType.INSERT, 
                           len(document.content), "\n- Phase 1: Planning (Week 1-2)")
    
    # Charlie tries to edit but can only comment
    try:
        manager.update_document(doc_id, users[2], OperationType.INSERT, 
                               len(document.content), "\n- Phase 2: Implementation")
        print("ERROR: Charlie should not be able to edit!")
    except:
        print("Charlie can't edit (as expected)")
    
    # Diana tries to edit but can only view
    try:
        manager.update_document(doc_id, users[3], OperationType.INSERT, 
                               len(document.content), "\n- Phase 3: Testing")
        print("ERROR: Diana should not be able to edit!")
    except:
        print("Diana can't edit (as expected)")
    
    # Get the final document
    document = manager.get_document(doc_id)
    print(f"\nFinal document content:")
    print(document.content)
    
    return service, manager, doc_id, users

def main():
    print("Google Docs-like System Demo")
    print("===========================\n")
    
    # Run test cases
    test_basic_functionality()
    test_conflict_resolution()
    test_multiple_users()

if __name__ == "__main__":
    main()
