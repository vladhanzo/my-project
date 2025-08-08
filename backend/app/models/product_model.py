from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from backend.app.models.base import Base

class ProductModel(Base):
    __tablename__ = "product_models"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    assemblies: Mapped[list["Assembly"]] = relationship(back_populates="product_model")
