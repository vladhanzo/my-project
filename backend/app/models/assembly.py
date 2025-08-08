from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, String
from backend.app.models.base import Base

class Assembly(Base):
    __tablename__ = "assemblies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    product_model_id: Mapped[int] = mapped_column(ForeignKey("product_models.id"))

    product_model: Mapped["ProductModel"] = relationship(back_populates="assemblies")
    operations: Mapped[list["Operation"]] = relationship(back_populates="assembly")
