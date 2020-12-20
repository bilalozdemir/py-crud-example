import os
from typing import Optional, Union, List

from tortoise import Tortoise, models, fields
from tortoise.exceptions import DoesNotExist

from util import check_password

class User(models.Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=20, required=True)
    last_name = fields.CharField(max_length=20, required=True)
    email = fields.CharField(min_length=5, max_length=20, unique=True, required=True)
    username = fields.CharField(min_length=5, max_length=15, unique=True, required=True)
    password = fields.CharField(max_length=255, indexable=False, required=True)

async def create_user(data) -> bool:
    await User.create(data)
    return True

async def delete_user(id: int) -> bool:
    count = await User.filter(id=id).delete()
    if count:
        return True
    return False

async def get_user_s(id: Optional[int] = None) -> Union[dict, List[dict]]:
    try:
        if id:
            data = await User.filter(id=id).values("id", "first_name", "last_name", "email", "username")
        else:
            data = await User.all().values("id", "first_name", "last_name", "email", "username")
        return data
    except DoesNotExist:
        return {"err": "Does Not Exists", "msg": f"Couldn't find a user with ID <{id}>"}

async def check_password(username: str, password: str) -> bool:
    return await check_password(password, User.filter(username=username).value("password"))

async def change_password(username: str, new_hashed_password: str) -> bool:
    await User.filter(username=username).update(password=new_hashed_password)
    return True

async def init():
    await Tortoise.init(
        db_url = f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@maria_db:3306/{os.getenv('MYSQL_DATABASE')}",
        modules={'models': [__name__]}
    )
    await Tortoise.generate_schemas()
