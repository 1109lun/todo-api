from pydantic import BaseModel
from typing import Optional
from datetime import date

class TaskBase (BaseModel) :
    title : str
    description : Optional[str] = ""
    due_date : Optional[date] = None
    priority : Optional[str] = "low"
    completed : Optional[bool] = False

class TaskCreate (TaskBase) :
    project_id : int

class TaskUpdate (TaskBase) :
    pass

class TaskInDB (TaskBase) :
    id : int
    project_id : int

    class Config :
        orm_mode = True

class ProjectBase (BaseModel) :
    name : str

class ProjectCreate (ProjectBase) : 
    pass

class ProjectInDB (ProjectBase) :
    id : int

    class Config :
        orm_mode = True