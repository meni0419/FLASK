from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime

# Схемы для категорий вопросов
class QuestionCategoryBase(BaseModel):
    name: str = Field(..., min_length=3)
    description: Optional[str] = None


class QuestionCategoryCreate(QuestionCategoryBase):
    pass


class QuestionCategoryUpdate(QuestionCategoryBase):
    pass


class QuestionCategoryResponse(QuestionCategoryBase):
    question_category_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Схемы для вопросов
class QuestionBase(BaseModel):
    question: str = Field(..., min_length=5)


class QuestionCreate(QuestionBase):
    question_category_id: int = Field(..., gt=0)


class QuestionUpdate(QuestionBase):
    question_category_id: Optional[int] = Field(None, gt=0)


class QuestionResponse(QuestionBase):
    question_id: int
    question_category_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # Интеграция данных о категории
    category: Optional[QuestionCategoryResponse] = None

    class Config:
        from_attributes = True

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
    full_name: Optional[str] = Field(None, pattern=r'^[a-zA-Z\s]*$')
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

    # @field_validator('username')
    # def username_validator(cls, v):
    #     if v.lower() in ['admin', 'administrator']:
    #         raise ValueError('Username cannot be "admin" or "administrator"')
    #     return v

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
