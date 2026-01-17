"""
Phase II API Test Suite
Tests all endpoints: health, auth, and task CRUD operations
"""

import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health():
    """Test the health check endpoint"""
    print_section("TEST 1: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_register(email, password, name):
    """Test user registration"""
    print_section(f"TEST 2: Register User ({email})")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json={"email": email, "password": password, "name": name},
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")

        if response.status_code in [200, 201]:
            token = data.get("access_token")
            user_id = data.get("user_id")
            print(f"\nToken obtained: {token[:20]}...")
            print(f"User ID: {user_id}")
            return token, user_id
        return None, None
    except Exception as e:
        print(f"ERROR: {e}")
        return None, None

def test_login(email, password):
    """Test user login"""
    print_section(f"TEST 3: Login User ({email})")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password},
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")

        if response.status_code == 200:
            token = data.get("access_token")
            user_id = data.get("user_id")
            print(f"\nToken obtained: {token[:20]}...")
            print(f"User ID: {user_id}")
            return token, user_id
        return None, None
    except Exception as e:
        print(f"ERROR: {e}")
        return None, None

def test_create_task(token, title, description=""):
    """Test creating a task"""
    print_section(f"TEST 4: Create Task - '{title}'")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{BASE_URL}/tasks/",
            headers=headers,
            json={"title": title, "description": description},
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")

        if response.status_code in [200, 201]:
            task_id = data.get("id")
            print(f"\nTask created with ID: {task_id}")
            return task_id
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def test_list_tasks(token):
    """Test listing all tasks"""
    print_section("TEST 5: List All Tasks")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/tasks/", headers=headers, timeout=5)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        print(f"\nTotal tasks: {len(data)}")
        return data
    except Exception as e:
        print(f"ERROR: {e}")
        return []

def test_get_task(token, task_id):
    """Test getting a specific task"""
    print_section(f"TEST 6: Get Task by ID ({task_id})")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/tasks/{task_id}", headers=headers, timeout=5)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        return data
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def test_update_task(token, task_id, title=None, description=None):
    """Test updating a task"""
    print_section(f"TEST 7: Update Task ({task_id})")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {}
        if title:
            payload["title"] = title
        if description is not None:
            payload["description"] = description

        response = requests.put(
            f"{BASE_URL}/tasks/{task_id}",
            headers=headers,
            json=payload,
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        return data
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def test_toggle_complete(token, task_id):
    """Test toggling task completion"""
    print_section(f"TEST 8: Toggle Task Completion ({task_id})")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.patch(
            f"{BASE_URL}/tasks/{task_id}/toggle",
            headers=headers,
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        print(f"\nTask completion status: {data.get('completed')}")
        return data
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def test_delete_task(token, task_id):
    """Test deleting a task"""
    print_section(f"TEST 9: Delete Task ({task_id})")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(
            f"{BASE_URL}/tasks/{task_id}",
            headers=headers,
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 204:
            print("Task deleted successfully (204 No Content)")
            return True
        else:
            print(f"Response: {response.text}")
        return response.status_code == 204
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_data_isolation(token1, token2):
    """Test that users can only see their own tasks"""
    print_section("TEST 10: Data Isolation Between Users")
    try:
        # Create task for user 1
        headers1 = {"Authorization": f"Bearer {token1}"}
        response1 = requests.post(
            f"{BASE_URL}/tasks/",
            headers=headers1,
            json={"title": "User 1 Task", "description": "Only visible to User 1"},
            timeout=5
        )
        task1_id = response1.json().get("id")
        print(f"User 1 created task ID: {task1_id}")

        # Create task for user 2
        headers2 = {"Authorization": f"Bearer {token2}"}
        response2 = requests.post(
            f"{BASE_URL}/tasks/",
            headers=headers2,
            json={"title": "User 2 Task", "description": "Only visible to User 2"},
            timeout=5
        )
        task2_id = response2.json().get("id")
        print(f"User 2 created task ID: {task2_id}")

        # User 1 lists tasks - should only see their task
        response = requests.get(f"{BASE_URL}/tasks/", headers=headers1, timeout=5)
        user1_tasks = response.json()
        print(f"\nUser 1 sees {len(user1_tasks)} task(s)")
        print(f"Task titles: {[t['title'] for t in user1_tasks]}")

        # User 2 lists tasks - should only see their task
        response = requests.get(f"{BASE_URL}/tasks/", headers=headers2, timeout=5)
        user2_tasks = response.json()
        print(f"\nUser 2 sees {len(user2_tasks)} task(s)")
        print(f"Task titles: {[t['title'] for t in user2_tasks]}")

        # Verify isolation
        user1_has_user2_task = any(t['id'] == task2_id for t in user1_tasks)
        user2_has_user1_task = any(t['id'] == task1_id for t in user2_tasks)

        if user1_has_user2_task or user2_has_user1_task:
            print("\nERROR: Data isolation FAILED - users can see each other's tasks!")
            return False
        else:
            print("\nSUCCESS: Data isolation working correctly!")
            return True

    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  PHASE II API TEST SUITE")
    print("  Testing Backend: http://127.0.0.1:8000")
    print("="*60)

    results = {
        "passed": 0,
        "failed": 0,
        "tests": []
    }

    # Wait for server to be ready
    print("\nWaiting for server to be ready...")
    time.sleep(2)

    # Test 1: Health check
    if test_health():
        results["passed"] += 1
        results["tests"].append(("Health Check", "PASS"))
    else:
        results["failed"] += 1
        results["tests"].append(("Health Check", "FAIL"))
        print("\nERROR: Server not responding. Is it running?")
        return

    # Test 2 & 3: Register and login user 1
    token1, user1_id = test_register("user1@test.com", "password123", "User One")
    if token1:
        results["passed"] += 1
        results["tests"].append(("Register User 1", "PASS"))
    else:
        results["failed"] += 1
        results["tests"].append(("Register User 1", "FAIL"))
        return

    # Test login
    token1_login, _ = test_login("user1@test.com", "password123")
    if token1_login:
        results["passed"] += 1
        results["tests"].append(("Login User 1", "PASS"))
        token1 = token1_login  # Use login token
    else:
        results["failed"] += 1
        results["tests"].append(("Login User 1", "FAIL"))

    # Test 4: Create tasks
    task1_id = test_create_task(token1, "Buy groceries", "Milk, eggs, bread")
    if task1_id:
        results["passed"] += 1
        results["tests"].append(("Create Task", "PASS"))
    else:
        results["failed"] += 1
        results["tests"].append(("Create Task", "FAIL"))

    task2_id = test_create_task(token1, "Call dentist", "Schedule appointment")
    task3_id = test_create_task(token1, "Finish project", "Complete Phase II testing")

    # Test 5: List tasks
    tasks = test_list_tasks(token1)
    if len(tasks) >= 3:
        results["passed"] += 1
        results["tests"].append(("List Tasks", "PASS"))
    else:
        results["failed"] += 1
        results["tests"].append(("List Tasks", "FAIL"))

    # Test 6: Get specific task
    if task1_id:
        task = test_get_task(token1, task1_id)
        if task and task.get("id") == task1_id:
            results["passed"] += 1
            results["tests"].append(("Get Task by ID", "PASS"))
        else:
            results["failed"] += 1
            results["tests"].append(("Get Task by ID", "FAIL"))

    # Test 7: Update task
    if task1_id:
        updated = test_update_task(token1, task1_id, title="Buy groceries and milk")
        if updated and "Buy groceries and milk" in updated.get("title", ""):
            results["passed"] += 1
            results["tests"].append(("Update Task", "PASS"))
        else:
            results["failed"] += 1
            results["tests"].append(("Update Task", "FAIL"))

    # Test 8: Toggle completion
    if task1_id:
        toggled = test_toggle_complete(token1, task1_id)
        if toggled and toggled.get("completed") is not None:
            results["passed"] += 1
            results["tests"].append(("Toggle Completion", "PASS"))
        else:
            results["failed"] += 1
            results["tests"].append(("Toggle Completion", "FAIL"))

    # Test 9: Delete task
    if task3_id:
        deleted = test_delete_task(token1, task3_id)
        if deleted:
            results["passed"] += 1
            results["tests"].append(("Delete Task", "PASS"))
        else:
            results["failed"] += 1
            results["tests"].append(("Delete Task", "FAIL"))

    # Test 10: Data isolation (register second user)
    token2, user2_id = test_register("user2@test.com", "password456", "User Two")
    if token2:
        isolated = test_data_isolation(token1, token2)
        if isolated:
            results["passed"] += 1
            results["tests"].append(("Data Isolation", "PASS"))
        else:
            results["failed"] += 1
            results["tests"].append(("Data Isolation", "FAIL"))

    # Print summary
    print_section("TEST SUMMARY")
    for test_name, status in results["tests"]:
        symbol = "✓" if status == "PASS" else "✗"
        print(f"{symbol} {test_name}: {status}")

    print(f"\nTotal Tests: {results['passed'] + results['failed']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")

    if results["failed"] == 0:
        print("\n" + "="*60)
        print("  ALL TESTS PASSED! Phase II Backend is WORKING!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print(f"  {results['failed']} TEST(S) FAILED - Review errors above")
        print("="*60)

if __name__ == "__main__":
    main()
