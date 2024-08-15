
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.api.routes import agentroutes

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Received request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Returning response: Status {response.status_code}")
        return response
    except Exception as e:
        logger.exception("An error occurred while processing the request")
        return JSONResponse(status_code=500, content={"detail": str(e)})

app.include_router(agentroutes.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")