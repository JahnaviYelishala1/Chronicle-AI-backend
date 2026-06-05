from pydantic import BaseModel


class VideoCreate(BaseModel):
    title: str
    source_type: str
    file_path: str | None = None