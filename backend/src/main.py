import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import refresh_token
from src.db.database import get_async_session
from src.settings import settings

from src.auth.router import router as auth_router
from src.workspace.router import router as workspace_router
from src.project.router import router as project_router
from src.task.router import router as task_router
from src.task.color_router import router as color_router
from src.task.tag_router import router as tag_router


app = FastAPI(
    title='My Family Todo',
    description='My Family Todo App',
    version='0.2.0',
    debug=True,
)

app.include_router(auth_router)
app.include_router(workspace_router, prefix='/workspace', tags=['workspace'])
app.include_router(project_router, prefix='/project', tags=['project'])
app.include_router(task_router, prefix='/task', tags=['task'])
app.include_router(color_router, prefix='/color', tags=['color'])
app.include_router(tag_router, prefix='/tag', tags=['tag'])

origins = ["0.0.0.0:8000", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def index():
    return f'Приложение My Family TODO'


@app.post('/token/refresh', status_code=200)
async def refresh_token_endpoint(
    request: dict,
    session: AsyncSession = Depends(get_async_session),
):
    return await refresh_token(request.get('refresh_token'), session)



if __name__ == '__main__':

    uvicorn.run(
        'app:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )
