import pytest
from app import (create_app)

"""@pytest.fixture(scope = "session")
def client():
    app = create_app()
    app.config.update({"TESTING": True});
    app.run(debug=True, host='0.0.0.0', port=5000)
    client = app.test_client()
    yield client
"""
    
def test_flask1():
    app = create_app()
    app.config.update({"TESTING": True});
    client = app.test_client()
    response = client.get("http://127.0.0.1:5000/catalog")
    
    #check status code
    assert response.status_code == 200;
    
def test_flask2():
    app = create_app()
    app.config.update({"TESTING": True});
    client = app.test_client()
    response = client.get("http://127.0.0.1:5000/catalog")
    html = response.data
    
    #check basic table tags
    assert "<table>".encode() in html;
    assert "</table>".encode() in html;
    assert "<thead>".encode() in html;
    assert "</thead>".encode() in html;
    assert "<tbody>".encode() in html;
    assert "</tbody>".encode() in html;
    assert "<tr>".encode() in html;
    assert "</tr>".encode() in html;
    assert "<td>".encode() in html;
    assert "</td>".encode() in html;
    
def test_flask3():
    app = create_app()
    app.config.update({"TESTING": True});
    client = app.test_client()
    response = client.get("http://127.0.0.1:5000/catalog")
    html = response.data
    
    #check correct headers
    assert "<th>ID</th>".encode() in html;
    assert "<th>Title</th>".encode() in html;
    assert "<th>Author</th>".encode() in html;
    assert "<th>ISBN</th>".encode() in html;
    assert "<th>Availability</th>".encode() in html;
    assert "<th>Actions</th>".encode() in html;
