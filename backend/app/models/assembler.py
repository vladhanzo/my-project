from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from backend.app.models.base import Base

class Assembler(Base):
    __tablename__ = "assemblers"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    operations: Mapped[list["Operation"]] = relationship(back_populates="assembler")
