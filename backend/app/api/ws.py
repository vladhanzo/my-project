from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, assembly_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(assembly_id, []).append(websocket)

    def disconnect(self, assembly_id: str, websocket: WebSocket):
        connections = self.active_connections.get(assembly_id)
        if connections:
            connections.remove(websocket)
            if not connections:
                del self.active_connections[assembly_id]

    async def broadcast(self, assembly_id: str, message: dict):
        for connection in self.active_connections.get(assembly_id, []):
            await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/{assembly_id}")
async def websocket_endpoint(websocket: WebSocket, assembly_id: str):
    await manager.connect(assembly_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(assembly_id, websocket)
