from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

import schemas
from database import get_db
from sqlalchemy.orm import Session
from crud import (
    create_group, get_groups, get_group, update_group, delete_group,
    create_user, get_users, get_user, update_user, delete_user
)

router_websocket = APIRouter()
router_groups = APIRouter(prefix='/groups', tags=['group'])
router_users = APIRouter(prefix='/users', tags=['user'])


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


async def notify_clients(message: str):
    for connection in manager.active_connections:
        await connection.send_text(message)


@router_websocket.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"Client id:{client_id} joined the chat")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You message: {data}", websocket)
            await manager.broadcast(f"Client id:{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client id:{client_id} left the chat")


@router_groups.post("/", response_model=schemas.Group)
async def create_group_route(group_data: schemas.GroupCreate, db: Session = Depends(get_db)):
    group = create_group(db, group_data)
    await notify_clients(f"group added: {group.name}")
    return group


@router_groups.get("/", response_model=List[schemas.Group])
async def read_groups(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    groups = get_groups(db, skip=skip, limit=limit)
    return groups


@router_groups.get("/{group_id}", response_model=schemas.Group)
async def read_group(group_id: int, db: Session = Depends(get_db)):
    group = get_group(db, group_id)
    return group


@router_groups.patch("/{group_id}", response_model=schemas.Group)
async def update_group_route(group_id: int, group_data: schemas.GroupUpdate, db: Session = Depends(get_db)):
    updated_group = update_group(db, group_id, group_data)
    if updated_group:
        await notify_clients(f"group updated: {updated_group.name}")
        return updated_group
    return {"message": "group not found"}


@router_groups.delete("/{group_id}")
async def delete_group_route(group_id: int, db: Session = Depends(get_db)):
    deleted = delete_group(db, group_id)
    if deleted:
        await notify_clients(f"group deleted: ID {group_id}")
        return {"message": "group deleted"}
    return {"message": "group not found"}


# Товары
@router_users.post("/", response_model=schemas.User)
async def create_user_route(schema: schemas.UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, schema)
    await notify_clients(f"user added: {user.name}")
    return user


@router_users.get("/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router_users.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    return user


@router_users.patch("/{user_id}")
async def update_user_route(user_id: int, schema: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, schema)
    if updated_user:
        await notify_clients(f"user updated: {updated_user.name}")
        return updated_user
    return {"message": "user not found"}


@router_users.delete("/{user_id}")
async def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    deleted = delete_user(db, user_id)
    if deleted:
        await notify_clients(f"user deleted: ID {user_id}")
        return {"message": "user deleted"}
    return {"message": "user not found"}
