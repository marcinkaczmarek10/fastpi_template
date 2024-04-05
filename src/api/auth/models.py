from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=256, unique=True)
    password = fields.CharField(max_length=256, null=True)
    created = fields.DatetimeField(auto_now_add=True)


user_pydantic = pydantic_model_creator(User, name="UserPydantic")
user_exclude_read_only = pydantic_model_creator(
    User, name="UserExcludeReadOnly", exclude_readonly=True
)
user_login = pydantic_model_creator(User, name="UserLogin", exclude=("id", "created"))
