# Сгенерируем app/models/__init__.py с импортом всех моделей
models_dir = os.path.join(backend_path, "app", "models")
init_path = os.path.join(models_dir, "__init__.py")

model_imports = """
from .product_model import ProductModel
from .assembly import Assembly
from .operation import Operation
from .component import Component
from .assembler import Assembler
from .component_action import ComponentAction
from .model_revision import ModelRevision
from .user import User
"""

base_definition = """
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
"""

with open(init_path, "w", encoding="utf-8") as f:
    f.write((model_imports + base_definition).strip())

# Подтвердим, что __init__.py создан
os.listdir(models_dir)
