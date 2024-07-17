from aiohttp.web_response import Response
from views import Routes, GroupView, ItemView
from models import User
from serializers import UserSerializer, UserCreateUpdateSerializer


user_routes = Routes()


@user_routes.view('/users')
class UserView(GroupView):
    async def get(self) -> Response:
        return await self.list(User, UserSerializer)
    
    async def post(self) -> Response:
        return await self.create(User, UserCreateUpdateSerializer)
    

@user_routes.view(f'/users/{user_routes.regex_for_retrieve}')
class UserRetrieveView(ItemView):
    async def get(self) -> Response:
        return await self.retrieve(User, UserSerializer)

    async def delete(self) -> Response:
        return await self.delete_object(User)