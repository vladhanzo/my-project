from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from backend.app.models.base import Base

class Component(Base):
    __tablename__ = "components"

    id: Mapped[int] = mapped_column(primary_key=True)
    part_number: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    component_actions: Mapped[list["ComponentAction"]] = relationship(back_populates="component")
