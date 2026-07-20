from typing import Optional
from pydantic import BaseModel, Field


class IncidentPredictionRequest(BaseModel):
    incident_text: str = Field(
        ...,
        example="Payment API timeout increased and downstream database is unavailable."
    )


class RolloutConfigUpdateRequest(BaseModel):
    active_model: Optional[str] = None
    shadow_enabled: Optional[bool] = None
    canary_enabled: Optional[bool] = None
    canary_model: Optional[str] = None
    canary_percent: Optional[int] = None