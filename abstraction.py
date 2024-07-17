from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from sqlmodel import select
import json
from abc import abstractmethod


class AbstractView(web.View):
    @property
    def async_db_session(self) -> AsyncSession:
        return self.request.db_session
    
    @classmethod
    def return_error(cls, error_class: web.HTTPException, data):
        return error_class(body = json.dumps(data, indent=2), content_type='application/json')
    

class AbstractGroupView(AbstractView):
    @abstractmethod
    async def list(self):
        pass
    
    @abstractmethod
    async def create(self):
        pass


class AbstractItemView(AbstractView):
    @abstractmethod
    async def retrieve(self):
        pass

    @abstractmethod
    async def partitial_update(self):
        pass

    @abstractmethod
    async def delete_object(self):
        pass

    async def get_object(self, model_class):
        id = int(self.request.match_info.get('pk'))
        results: AsyncResult = await self.async_db_session.execute(
            select(model_class)
            .where(model_class.id == id)
        )
        return results.scalar()