from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# Para desenvolvimento rápido, usamos SQLite assíncrono. 
# Em produção, basta trocar para a URL do seu PostgreSQL/MySQL.
DATABASE_URL = "sqlite+aiosqlite:///./centelha_workshop.db"

engine = create_async_engine(DATABASE_URL, echo=False)

async_session = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Dependência para injetar a sessão nas rotas do FastAPI
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()