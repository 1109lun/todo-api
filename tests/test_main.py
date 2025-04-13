from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_projects():
    response = client.get("/projects")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_project():
    response = client.post("/projects", json={"name": "Test Project"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Project"

def test_get_single_project():
    create_res = client.post("/projects", json={"name": "Single Project"})
    project_id = create_res.json()["id"]

    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["id"] == project_id

def test_update_project():
    create_res = client.post("/projects", json={"name": "Old Project"})
    project_id = create_res.json()["id"]

    response = client.put(f"/projects/{project_id}", json={"name": "Updated Project"})
    assert response.status_code == 200

def test_delete_project():
    create_res = client.post("/projects", json={"name": "To be deleted"})
    project_id = create_res.json()["id"]

    response = client.delete(f"/projects/{project_id}")
    assert response.status_code == 204

def test_create_task():
    # 先建立一個 project
    project_res = client.post("/projects", json={"name": "Task Project"})
    project_id = project_res.json()["id"]

    task_data = {
        "title": "Test Task",
        "description": "Details",
        "due_date": "2025-05-01",
        "priority": "High",
        "completed": False,
        "project_id": project_id
    }

    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"

def test_get_tasks_by_project():
    project_res = client.post("/projects", json={"name": "Project With Tasks"})
    project_id = project_res.json()["id"]

    task_data = {
        "title": "Task 1",
        "description": "abc",
        "due_date": "2025-05-02",
        "priority": "Medium",
        "completed": False,
        "project_id": project_id
    }
    client.post("/tasks", json=task_data)

    response = client.get(f"/projects/{project_id}/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_task():
    project_res = client.post("/projects", json={"name": "Project for Update"})
    project_id = project_res.json()["id"]

    task_res = client.post("/tasks", json={
        "title": "Original",
        "description": "",
        "due_date": "2025-06-01",
        "priority": "Low",
        "completed": False,
        "project_id": project_id
    })
    task_id = task_res.json()["id"]

    update_data = {
        "title": "Updated Title",
        "completed": True
    }

    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200

def test_delete_task():
    project_res = client.post("/projects", json={"name": "To Delete Task"})
    project_id = project_res.json()["id"]

    task_res = client.post("/tasks", json={
        "title": "To Be Deleted",
        "description": "",
        "due_date": "2025-06-01",
        "priority": "Low",
        "completed": False,
        "project_id": project_id
    })
    task_id = task_res.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

