from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

app = FastAPI(title="길이 단위 변환 서비스")

TO_METER = {
    "meter": 1.0,
    "yard": 0.9144,
    "inch": 0.0254,
    "feet": 0.3048,
}

Unit = Literal["meter", "yard", "inch", "feet"]
# 필요한 타입만 미리 지정해줘서 지정된 타입이 아니면 알아서 에러가 나오도록 함

class ConvertResponse(BaseModel):
    value: float
    from_unit: Unit
    to_unit: Unit
    result: float

@app.get("/convert/length")
def convert_length(value: float, from_unit: Unit, to_unit: Unit) -> ConvertResponse:
    meters = value * TO_METER[from_unit]
    # 이 부분을 통해 기본적으로 미터로 변환해두고 원하는 단위로 바꿀 수 있게함, 그러면 코드를 여러 개 짜야 하는 수고를 덜 수 있음
    result = meters / TO_METER[to_unit]
    return ConvertResponse(
        value=value,
        from_unit=from_unit,
        to_unit=to_unit,
        result=round(result, 3),
    )
# 반올림 3자리는 임의로 정함