from pydantic import BaseModel



#資料驗證
class TodoBase(BaseModel):
    title:str
    description:str | None=None #None=None 代表可以填空白值
    complete: bool=False

#建立的格式
class TodoCreate(TodoBase):
    pass

#回傳的格式
class TodoResponse(TodoBase):
    id:int

    class Config:
        from_attributes=True