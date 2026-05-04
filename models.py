from sqlalchemy import Column, Integer, String
from database import Base   # ✅ fixed (no dot)

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    streak = Column(Integer, default=0)