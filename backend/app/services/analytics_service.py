from fastapi import APIRouter
from datetime import date, timedelta

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/assemblies-per-day")
def assemblies_per_day():
    today = date.today()
    data = [
        {"date": (today - timedelta(days=i)).isoformat(), "count": (i + 1) * 5}
        for i in range(7)
    ]
    return {"data": data}

@router.get("/error-heatmap")
def error_heatmap():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    data = [
        {"day": day, "hour": hour, "errors": (hour + idx) % 7}
        for idx, day in enumerate(days)
        for hour in range(0, 24, 6)
    ]
    return {"data": data}
