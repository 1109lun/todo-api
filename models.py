from sqlalchemy import Column , Integer , String , Boolean , ForeignKey , Date
from sqlalchemy.orm import relationship , declarative_base

Base = declarative_base()

class Project(Base) :
    __tablename__ = "projects"

    id = Column(Integer , primary_key = True)
    name = Column(String , nullable = False)

    tasks = relationship("Task" , back_populates="project" , cascade = "all , delete-orphan" )

class Task(Base) :
    __tablename__ = "tasks"

    id = Column(Integer , primary_key = True)
    title = Column(String , nullable = False)
    description = Column(String)
    due_date = Column(Date)
    priority = Column(String , default = "low")
    completed = Column(Boolean , default = False)

    project_id = Column(Integer , ForeignKey("projects.id"))
    project = relationship("Project" ,  back_populates = "tasks")