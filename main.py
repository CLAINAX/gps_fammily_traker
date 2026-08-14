from fastapi import FastAPI
from api.routes import router
from core.security import rotate_all_tokens
import asyncio
from contextlib import asynccontextmanager
from test_app import run_all_tests  # Importamos tu nuevo robot

async def refresh_tokens_loop():
    while True:
        rotate_all_tokens()
        await asyncio.sleep(30)


async def daily_test_loop():
    await asyncio.sleep(5)  
    while True:
        await asyncio.to_thread(run_all_tests)
        await asyncio.sleep(86400)  

@asynccontextmanager
async def lifespan(app: FastAPI):
    task1 = asyncio.create_task(refresh_tokens_loop())
    task2 = asyncio.create_task(daily_test_loop()) 
    yield
    task1.cancel()
    task2.cancel()
    try:
        await task1
        await task2
    except asyncio.CancelledError:
        pass

app = FastAPI(title="Live360 Clone Modular API", lifespan=lifespan)
app.include_router(router)