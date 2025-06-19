from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str = Field(..., min_length=3)
    price: float = Field(..., gt=0)
    description: Optional[str] = None
    in_stock: bool = True


class ProductCreate(ProductBase):
    price: float = Field(..., gt=0)
    in_stock: bool = True
    category_id: int = Field(..., gt=0)


class ProductUpdate(ProductBase):
    product_id: int
    category_id: int


class ProductResponse(ProductBase):
    product_id: int
    category_id: int

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=3)
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    category_id: int


class CategoryResponse(CategoryBase):
    category_id: int

    class Config:
        from_attributes = True


class AddressBase(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)


class AddressCreate(AddressBase):
    pass


class AddressResponse(AddressBase):
    address_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str = Field(..., min_length=3)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=120)
    is_employed: Optional[bool] = False


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    address: Optional[AddressCreate] = None


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=120)
    is_employed: Optional[bool] = None
    address: Optional[AddressCreate] = None

    # @model_validator(mode='after')
    # def validate_age(cls, values):
    #     age = values.age
    #     is_employed = values.is_employed
    #     if is_employed and age is not None:
    #         if age < 18 or age > 65:
    #             raise ValueError('Employed users must be between 18 and 65 years old')
    #     return values


class UserResponse(UserBase):
    user_uuid: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    status: int
    is_admin: bool
    address: Optional[AddressResponse] = None

    class Config:
        from_attributes = True
