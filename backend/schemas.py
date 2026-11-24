from pydantic import BaseModel, Field


class RootResponse(BaseModel):
    message: str
    status: str
    project: str
    agent: str


class HealthResponse(BaseModel):
    status: str
    application: str
    agent: str


class InfoResponse(BaseModel):
    app_name: str
    agent_name: str
    app_version: str
    debug: bool


class EchoRequest(BaseModel):
    message: str = Field(
        ..., min_length=1, max_length=500, description="Text to send back"
    )


class EchoResponse(BaseModel):
    message: str
    length: int
    agent: str