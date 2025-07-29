from fastapi import FastAPI
from mcp_infrastructure.mcp_server.handlers import pattern_detection_handler

app = FastAPI(title="Pattern Detection API")

# Inclure le router du handler de détection de patterns
app.include_router(pattern_detection_handler.router)

@app.get("/")
def root():
    return {"message": "Pattern Detection API is running."} 