import pytest
from unittest.mock import Mock, patch, call
from app.main import app, process_expression
from app.calculator import evaluate_rpn

def test_calculate_add(client):
    resp = client.post("/calculate", json={"expression": "2 3 +"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["result"] == 5
    assert data["expression"] == "2 3 +"

def test_calculate_invalid(client):
    resp = client.post("/calculate", json={"expression": "2 +"})
    assert resp.status_code == 400

def test_history(client):
    resp = client.get("/history")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_batch_calculate_valid(client):
    expressions = [
        "2 3 +",      # 5
        "5 3 2 + *",  # 25
        "3 4 5 * +"   # 23
    ]
    resp = client.post("/calculate_batch", json={"expressions": expressions})
    assert resp.status_code == 200
    data = resp.json()
    assert "Processing 3 expressions" in data["message"]

    # Wait a bit for background processing
    import time
    time.sleep(1)

    # Check history after batch processing
    resp = client.get("/history")
    assert resp.status_code == 200
    history = resp.json()
    
    # Find our batch calculations in history
    results = {h["expression"]: h["result"] for h in history}
    assert results.get("2 3 +") == 5
    assert results.get("5 3 2 + *") == 25
    assert results.get("3 4 5 * +") == 23

def test_batch_calculate_invalid_expression(client):
    expressions = [
        "2 3 +",  # valid
        "2 +",    # invalid
        "3 4 *"   # valid
    ]
    resp = client.post("/calculate_batch", json={"expressions": expressions})
    assert resp.status_code == 400
    assert "Invalid expression" in resp.json()["detail"]

def test_batch_calculate_empty(client):
    resp = client.post("/calculate_batch", json={"expressions": []})
    assert resp.status_code == 200
    assert "Processing 0 expressions" in resp.json()["message"]

@pytest.mark.asyncio
async def test_process_expression(client):
    # Mock database operations
    mock_db = Mock()
    mock_db.add = Mock()
    mock_db.commit = Mock()
    mock_db.refresh = Mock()
    
    test_expr = "2 3 +"
    expected_result = evaluate_rpn(test_expr)
    
    await process_expression(test_expr, mock_db)
    
    # Verify database operations were called
    assert mock_db.add.called
    assert mock_db.commit.called

def test_complex_rpn_expressions(client):
    test_cases = [
        ("2 3 4 + *", 14),      # 2 * (3 + 4)
        ("5 1 2 + 4 * + 3 -", 14),  # 5 + (1 + 2) * 4 - 3
        ("3 4 2 * 1 5 - 2 3 + * + +", -9),  # 3 + (4 * 2 + (1 - 5) * (2 + 3))
    ]
    
    # First verify direct calculator results
    for expr, expected in test_cases:
        print(f"\nTesting expression: {expr}")
        print(f"Expected result: {expected}")
        result = evaluate_rpn(expr, debug=True)
        assert result == expected, f"Calculator gave wrong result for {expr}: got {result}, expected {expected}"
    
    # Then test through API
    for expr, expected in test_cases:
        resp = client.post("/calculate", json={"expression": expr})
        assert resp.status_code == 200
        result = resp.json()["result"]
        assert result == expected, f"API gave wrong result for {expr}: got {result}, expected {expected}"

def test_batch_calculate_concurrent(client):
    # Test concurrent processing of multiple expressions
    expressions = [f"{i} {i} +" for i in range(1, 11)]  # Creates 10 expressions: "1 1 +", "2 2 +", etc.
    
    resp = client.post("/calculate_batch", json={"expressions": expressions})
    assert resp.status_code == 200
    
    # Wait a bit for background processing
    import time
    time.sleep(1)
    
    # Check history
    resp = client.get("/history")
    history = resp.json()
    
    # Verify results
    results = {h["expression"]: h["result"] for h in history}
    for i in range(1, 11):
        expr = f"{i} {i} +"
        assert expr in results
        assert results[expr] == i + i  # Each expression should sum to 2*i 