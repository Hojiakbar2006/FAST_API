from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id:Optional[int]
    username:str
    email:str
    password:str
    is_staff:Optional[bool]
    is_active:Optional[bool]


    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                "username":"johndoe",
                "email":"johndoe@gmail.com",
                "password":"password",
                "is_staff":False,
                "is_active":True
            }
        }



class Settings(BaseModel):
    authjwt_secret_key:str='b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02d5c45b2fa7b86341fa405'


class LoginModel(BaseModel):
    username:str
    password:str



class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_status:Optional[str]="PENDING"
    pizza_size:Optional[str]="SMALL"
    user_id:Optional[int]


    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "quantity":2,
                "pizza_size":"LARGE"
            }
        }


class OrderStatusModel(BaseModel):
    order_status:Optional[str]="PENDING"

    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "order_status":"PENDING"
            }
        }

class PrductModel(BaseModel):
    id:Optional[int]
    name:str
    price:float
    description:Optional[str]
    image_url:Optional[str]
    category_id:Optional[int]


    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "name":"Pizza",
                "price":10.0,
                "description":"Pizza",
                "image_url":None,
                "category_id":None
            }}
        
class CategoryModel(BaseModel):
    id:Optional[int]
    name:str

    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "name":"Pizza"
            }
        }

