import pytest
from time import sleep

from sqlalchemy import insert, select

from src.auth.database import Role
from conftest import client, async_session_maker

# @pytest.mark.asyncio - labels like this are copmmented, bcs look last row at pyproject.toml
async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(Role).values(name="slave", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(Role)
        result = await session.execute(query)
        roles = result.scalars().all()
        # print(roles[0].name)
        assert len(roles)==1
        assert roles[0].name == 'slave', "Шото не так"
        

# @pytest.mark.asyncio
def test_register():
    response = client.post("/auth/register", json = {
        "email": "artur@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "artur",
        "role_id": 1
    })
    
    assert response.status_code == 201