from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ProductSeries(Base):
    __tablename__ = "product_series"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    models = relationship("ProductModel", back_populates="series")

class ProductModel(Base):
    __tablename__ = "product_model"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    series_id = Column(Integer, ForeignKey("product_series.id"), nullable=False)
    series = relationship("ProductSeries", back_populates="models")
    revisions = relationship("ModelRevision", back_populates="model")

class ModelRevision(Base):
    __tablename__ = "model_revision"
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, nullable=False)
    product_model_id = Column(Integer, ForeignKey("product_model.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    model = relationship("ProductModel", back_populates="revisions")
    required_components = relationship("RequiredComponent", back_populates="revision")

class RequiredComponent(Base):
    __tablename__ = "required_component"
    id = Column(Integer, primary_key=True, index=True)
    revision_id = Column(Integer, ForeignKey("model_revision.id"), nullable=False)
    component_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    revision = relationship("ModelRevision", back_populates="required_components")

