from sqlmodel import Field


class MixinModelId:
    id: int = Field(primary_key=True)