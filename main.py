from fastapi import FastAPI, Body, Depends
import schemas
import models

from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

def get_session():
    Session = SessionLocal()
    try:
        yield Session

    finally:
        Session.close()


app = FastAPI()

fakeDatabase = {
    1:{"task":"Limpar Carro"},
    2:{"task":"Limpar Casa"},
    3:{"task":"Desenvolver Jobs"},
    4:{"task":"Passear com o Cachorro"},
    5:{"task":"Treinar Musculação"},
    6:{"task":"Buscar esposa no trabalho"},
}

# Endpoint Fake Database
# @app.get("/")
# def getItems():
#     return fakeDatabase

@app.get("/")
def getItems(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items

# option #1
# @app.post("/")
# def addItens(task:str):
#     newId = len(fakeDatabase.keys()) + 1
#     fakeDatabase[newId] = {"task":task}
#     return fakeDatabase

# option #2 - Usando schema e FakeDatabase
# @app.post("/")
# def addItens(item:schemas.Item):
#     newId = len(fakeDatabase.keys()) + 1
#     fakeDatabase[newId] = {"task":item.task}
#     return fakeDatabase

@app.post("/")
def addItens(item:schemas.Item, session: Session = Depends(get_session)):
    item = models.Item(task = item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

# option #3
# @app.post("/")
# def addItens(body = Body()):
#     newId = len(fakeDatabase.keys()) + 1
#     fakeDatabase[newId] = {"task":body['task']}
#     return fakeDatabase

# usando fakeDatabase
# @app.get("/{id}")
# def getItems(id:int):
#     return fakeDatabase [id]

@app.get("/{id}")
def getItems(id:int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item

# usando FakeDatabase
# @app.put("/{id}")
# def updateItem(id:int, item:schemas.Item):
#     fakeDatabase[id]['task'] = item.task
#     return fakeDatabase

@app.put("/{id}")
def updateItem(id:int, item:schemas.Item ,session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    session.close()
    return itemObject

# usando FakeDatabase
# @app.delete("/{id}")
# def deleteItem(id:int):
#     del fakeDatabase[id]
#     return fakeDatabase

@app.delete("/{id}")
def deleteItem(id:int, session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'Item ' + str(id) + ' - Deletado com Sucesso!'