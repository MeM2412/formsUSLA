from db_logic import get_db_connection, insert_submission

def run_tests():
    # Test 1: Check the raw connection
    print("Testing database connection...")
    try:
        conn = get_db_connection()
        print("✅ Database connection successful!")
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return  # Stop here if we can't connect

    # Test 2: Attempt to insert a test record
    print("\nAttempting to insert a test record...")
    result = insert_submission(
        first_name="Matteo",
        middle_name="",
        last_name="Morais",
        phone="555-0100",
        email="test@example.com",
        privacy_accepted=True
    )
    
    if result["success"]:
        print(f"✅ Insert Test Passed: {result['message']} (ID: {result.get('id')})")
    else:
        print(f"⚠️ Insert Test Failed/Rejected: {result['message']}")

    # Test 3: Attempt to insert the exact same record again to test the duplicate block
    print("\nAttempting to insert a duplicate record...")
    duplicate_result = insert_submission(
        first_name="Matteo",
        middle_name="",
        last_name="Morais",
        phone="555-0100",
        email="test@example.com",
        privacy_accepted=True
    )

    if not duplicate_result["success"]:
        print(f"✅ Duplicate Block Passed: {duplicate_result['message']}")
    else:
        print(f"❌ Duplicate Block Failed: The database allowed a duplicate submission!")

if __name__ == "__main__":
    run_tests()