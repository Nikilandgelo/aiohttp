from aiohttp import web
from User.views import user_routes
from Advertisement.views import adverts_routes
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
import os
from sqlmodel import SQLModel
from models import *
from dotenv import find_dotenv, load_dotenv


@web.middleware
async def add_db_session(request: web.Request, handler):
    setattr(request, 'db_session', getattr(app, 'db_session'))
    response = await handler(request)
    return response

app = web.Application(middlewares=[add_db_session])
app.add_routes(user_routes)
app.add_routes(adverts_routes)

async def init_orm(app):
    database: AsyncEngine = create_async_engine(f'postgresql+asyncpg://'
                                                f'{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@'
                                                f'{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/'
                                                f'{os.getenv("POSTGRES_DB")}')
    async with database.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
    
    session = AsyncSession(database)
    setattr(app, 'db_session', session)
    yield
    await database.dispose()


if __name__ == '__main__':
    env_file: str = find_dotenv('.env')
    if env_file != '':
        load_dotenv(env_file)
    
    app.cleanup_ctx.append(init_orm)
    web.run_app(app)