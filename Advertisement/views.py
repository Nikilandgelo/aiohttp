from aiohttp.web_response import Response
from views import Routes, GroupView, ItemView
from models import Advertisement
from serializers import AdvertisementSerializer


adverts_routes = Routes()


@adverts_routes.view('/advertisements')
class AdvertisementView(GroupView):
    async def get(self) -> Response:
        return await self.list(Advertisement, AdvertisementSerializer)
    
    async def post(self) -> Response:
        return await self.create(Advertisement, AdvertisementSerializer)


@adverts_routes.view(f'/advertisements/{adverts_routes.regex_for_retrieve}')
class AdvertisementRetrieveView(ItemView):
    async def get(self) -> Response:
        return await self.retrieve(Advertisement, AdvertisementSerializer)
    
    async def patch(self) -> Response:
        return await self.partitial_update(Advertisement, AdvertisementSerializer)

    async def delete(self) -> Response:
        return await self.delete_object(Advertisement)
