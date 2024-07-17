from sqlmodel import Field, Relationship
from serializers import UserCreateUpdateSerializer, AdvertisementSerializer
from sqlalchemy import func
from mixins import MixinModelId
from datetime import datetime


class User(MixinModelId, UserCreateUpdateSerializer, table = True):
    adverts: 'Advertisement' = Relationship(back_populates='user')


class Advertisement(MixinModelId, AdvertisementSerializer, table = True):
    user: User = Relationship(back_populates='adverts')
    created_at: datetime = Field(
        sa_column_kwargs = {'server_default': func.now()}
    )