from aiohttp import web
from abstraction import AbstractGroupView, AbstractItemView
from sqlalchemy.ext.asyncio import AsyncResult
from sqlmodel import select
from sqlmodel import SQLModel
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError


class Routes(web.RouteTableDef):
    def __init__(self):
        self.regex_for_retrieve: str = r'{pk:\d+}'
        super().__init__()


class GroupView(AbstractGroupView):
    async def list(self, model_class: SQLModel, serializer_class: SQLModel):
        results: AsyncResult = await self.async_db_session.execute(
            select(model_class)
        )
        response: list[dict] = [serializer_class.model_validate(result).model_dump()
                                for result in results.scalars().all()]
        return web.json_response(response)

    async def create(self, model_class: SQLModel, serializer_class: SQLModel):
        body: dict = await self.request.json()
        try:
            validated_object: dict = serializer_class(**body).model_dump()
        except ValidationError as error:
            return self.return_error(web.HTTPConflict,
                                error.errors(include_context=False, include_input=False, include_url=False))
        model_instance = model_class(**validated_object)
        self.async_db_session.add(model_instance)
        try:
            await self.async_db_session.commit()
        except IntegrityError as error:
            await self.async_db_session.rollback()
            return self.return_error(web.HTTPConflict, 'Error when trying to insert data')
        
        return web.Response(body = "Object has been created")
    

class ItemView(AbstractItemView):
    async def retrieve(self, model_class: SQLModel, serializer_class: SQLModel):
        model_instance = await self.get_object(model_class)
        if model_instance is None:
            return self.return_error(web.HTTPNotFound, 'Object not found')
        validated_object: dict = serializer_class.model_validate(model_instance).model_dump()
        return web.json_response(validated_object)
    
    async def partitial_update(self, model_class: SQLModel, serializer_class: SQLModel):
        model_instance = await self.get_object(model_class)
        if model_instance is None:
            return self.return_error(web.HTTPNotFound, 'Object not found')
        
        body: dict = await self.request.json()
        for key, value in body.items():
            if hasattr(model_instance, key) == False:
                return self.return_error(web.HTTPConflict, f'Object does not have {key} field')
        
        try:
            validated_attrs: dict = serializer_class.model_validate(model_instance, update=body).model_dump()
        except ValidationError as error:
            return self.return_error(web.HTTPConflict,
                                     error.errors(include_context=False, include_input=False, include_url=False))
        
        for key, value in validated_attrs.items():
            setattr(model_instance, key, value)
        self.async_db_session.add(model_instance)
        try:
            await self.async_db_session.commit()
        except IntegrityError as error:
            await self.async_db_session.rollback()
            return self.return_error(web.HTTPConflict, 'Error when trying to insert data')
        
        return web.Response(body = "Object has been updated")

    async def delete_object(self, model_class: SQLModel):
        model_instance = await self.get_object(model_class)
        if model_instance is None:
            return self.return_error(web.HTTPNotFound, 'Object not found')
        await self.async_db_session.delete(model_instance)
        await self.async_db_session.commit()
        return web.Response(body = "Object has been deleted")