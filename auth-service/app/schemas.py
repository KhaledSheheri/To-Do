from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username:str
    passward:str

class LoginRequest(BaseModel):
    username:str
    password:str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str | str= "bearer"

class RegisterResponse(BaseModel):
    statusCode:int
    message:str

class TokenData(BaseModel):
    token: str
    
class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool

    class Config:
        from_attributes = True