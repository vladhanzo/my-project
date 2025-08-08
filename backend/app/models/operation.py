from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, String
from backend.app.models.base import Base

class Operation(Base):
    __tablename__ = "operations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    assembly_id: Mapped[int] = mapped_column(ForeignKey("assemblies.id"))
    assembler_id: Mapped[int] = mapped_column(ForeignKey("assemblers.id"))

    assembly: Mapped["Assembly"] = relationship(back_populates="operations")
    assembler: Mapped["Assembler"] = relationship(back_populates="operations")
    component_actions: Mapped[list["ComponentAction"]] = relationship(back_populates="operation")
