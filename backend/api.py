from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socket
import json

app = FastAPI(title="TimeTravel-Redis API Bridge")

# Corrected CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False, # This MUST be False when origins is ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

def query_tcp_server(cmd: str):
    """Sends a raw command to the TCP server and parses the JSON response."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 6379))
        
        resp = f"*1\r\n${len(cmd)}\r\n{cmd}\r\n"
        s.sendall(resp.encode('utf-8'))
        
        data = s.recv(4096).decode('utf-8')
        s.close()
        
        lines = data.split("\r\n")
        if len(lines) >= 2 and lines[0].startswith('$'):
            return json.loads(lines[1])
        return {"error": "Invalid response format"}
        
    except ConnectionRefusedError:
        return {"error": "TCP Server offline"}

@app.get("/api/health")
def health_check():
    return {"status": "Bridge Online"}

@app.get("/api/stats")
def get_database_stats():
    return query_tcp_server("STATS")

@app.get("/api/keys")
def get_all_keys():
    return query_tcp_server("KEYS")