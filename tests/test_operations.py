from httpx import AsyncClient


async def test_add_specific_operation(ac: AsyncClient):
    response = await ac.post("/operations", json = {
        "quantity": "25.5",
        "figi": "figi_CODE",
        "instriment_type": "bond",
        "date": None,
        "operation_type": "Выплата купонов"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
async def test_get_specific_operation(ac: AsyncClient):
    response = await ac.get("/operations", params={
        "operation_id": 1,
    }, follow_redirects=True)
    
    
    assert response.status_code == 200
    assert response.json()['status'] == "success"
    assert len(response.json()['data']) == 1
    