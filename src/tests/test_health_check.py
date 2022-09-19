def test_health_check(test_app):
    response = test_app.get("/api/v1/health-check/")
    assert response.status_code == 200
    assert response.json() == {"success": True}