import datetime
from ..extensions import db
from ..models.tasks import Task
from ..models.users import User
from ..utils import detach
from sqlalchemy.dialects.postgresql import UUID

def CreateTask(title:str, description:str, admin_id:str|UUID):
    task = Task(title=title.strip(), description=description.strip(), admin_id=admin_id)
    db.session.add(task)
    db.session.commit()
    task = detach(task)
    return task, 500 if not task else 200

def FetchTasks(userid:str):
    tasks = (
        db.session.query(Task).filter(Task.admin_id==userid).all()
    )
    if not tasks: return [], 404
    tasks = detach(tasks)
    return tasks, 200 if len(tasks)>0 else 404

def FetchTask(id:UUID | str, userid:UUID | str):
    task = (
        db.session.query(Task).filter(Task.id==id and Task.admin_id==userid).first()
    )
    task = detach(task)
    return task, 404 if not task else 200
        

def UpdateTask(id:str | UUID, admin_id:str | UUID, title:str=None, description:str=None, completed:bool=None):
    task = (
        db.session.query(Task).filter(Task.id==id and Task.admin_id==admin_id).first()
    )
    if not task: return task, 404
    if(title): task.title=title
    if(description): task.description=description
    if(completed):
        task.completed=completed
    task.updated_at=datetime.datetime.now()
    db.session.commit()
    task = detach(task)
    return task, 200

def DeleteTask(id:str | UUID, admin_id:str | UUID):
    task = (
        db.session.query(Task).filter(Task.id==id and Task.admin_id==admin_id).first()
    )
    if not task: return False, 404
    db.session.delete(task)
    db.session.commit()
    return True, 200