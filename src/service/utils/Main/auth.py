import requests
from fastapi import HTTPException


async def check_permissions(token: str, role_access: list) -> bool:
    r_uri = 'https://id.vchern.me/id/users/me'
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(r_uri, headers=headers)
    if res.status_code == 200:
        res = res.json()
        if res['role'] in role_access:
            return True
        else:
            return False
    else:
        return res
