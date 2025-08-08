from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from backend.app.models.base import Base

class ComponentAction(Base):
    __tablename__ = "component_actions"

    id: Mapped[int] = mapped_column(primary_key=True)
    operation_id: Mapped[int] = mapped_column(ForeignKey("operations.id"))
    component_id: Mapped[int] = mapped_column(ForeignKey("components.id"))

    operation: Mapped["Operation"] = relationship(back_populates="component_actions")
    component: Mapped["Component"] = relationship(back_populates="component_actions")
