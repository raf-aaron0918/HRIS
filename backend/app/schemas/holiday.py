from pydantic import BaseModel, ConfigDict


class HolidayBase(BaseModel):
    holiday_id: str
    name: str
    holiday_date: str
    holiday_type: str = "Regular Holiday"
    notes: str | None = None


class HolidayCreate(HolidayBase):
    pass


class HolidayUpdate(BaseModel):
    name: str
    holiday_date: str
    holiday_type: str = "Regular Holiday"
    notes: str | None = None


class HolidayResponse(HolidayBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class HolidayListResponse(BaseModel):
    items: list[HolidayResponse]
    total: int
