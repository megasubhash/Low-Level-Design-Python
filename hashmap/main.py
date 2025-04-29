from factory.HashMapFactory import HashMapFactory
from services.HashMapService import HashMapService
from enums.HashMapType import HashMapType

def main():
    # Create a HashMap with the DJB2 hashing strategy using the factory
    hash_map = HashMapFactory.create_hash_map(HashMapType.SIMPLE, 16)
    
    # Add some key-value pairs
    hash_map.put("name", "John")
    hash_map.put("age", 30)
    hash_map.put("city", "New York")
    
    # Retrieve values
    print(f"Name: {hash_map.get('name')}")
    print(f"Age: {hash_map.get('age')}")
    print(f"City: {hash_map.get('city')}")
    
    # Check if a key exists
    print(f"Contains 'country': {hash_map.contains_key('country')}")
    
    # Remove a key
    hash_map.remove("age")
    print(f"After removing 'age', contains 'age': {hash_map.contains_key('age')}")
    
    # Add more entries to trigger resize
    for i in range(20):
        hash_map.put(f"key{i}", f"value{i}")
    
    # Use service for operations like resizing
    HashMapService.resize_if_needed(hash_map)
    
    print(f"HashMap size: {hash_map.get_size()}")
    print(f"HashMap capacity: {hash_map.capacity}")

if __name__ == "__main__":
    main()
