from pydantic import BaseModel
from typing import List

class RouteIdentifierOutputStops(BaseModel):
  source: str
  mode: str
  stop: str
  operator: str
  departure: str
  arrival: str
  duration: str
  flight_number: str

class RouteIdentifierOutput(BaseModel):
  stops: List[RouteIdentifierOutputStops]
  destination: str

