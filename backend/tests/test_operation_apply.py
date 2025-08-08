# backend/tests/test_operation_apply.py

import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.models import Operation, Component
from backend.app.services.operation_service import apply_operation
from backend.app.db.session import get_db
from backend.app.schemas.operation import OperationCreate, OperationComponentChange

client = TestClient(app)


@pytest.fixture
def db(session: Session):
    yield session


@pytest.fixture
def base_components(db):
    component_a = Component(name="Base A")
    component_b = Component(name="Base B")
    db.add_all([component_a, component_b])
    db.commit()
    return component_a, component_b


def test_apply_operation_normal_workflow(db, base_components):
    component_a, component_b = base_components
    op_data = OperationCreate(
        name="Test Operation",
        changes=[
            OperationComponentChange(component_id=component_a.id, action="remove"),
            OperationComponentChange(component_id=component_b.id, action="add"),
        ]
    )
    operation = apply_operation(db=db, op_data=op_data)
    assert operation.name == "Test Operation"
    assert any(c.component_id == component_b.id and c.action == "add" for c in operation.changes)
    assert any(c.component_id == component_a.id and c.action == "remove" for c in operation.changes)


def test_apply_operation_remove_added_component(db):
    component = Component(name="Temp Component")
    db.add(component)
    db.commit()
    op_data = OperationCreate(
        name="Edge Case Operation",
        changes=[
            OperationComponentChange(component_id=component.id, action="add"),
            OperationComponentChange(component_id=component.id, action="remove"),
        ]
    )
    operation = apply_operation(db=db, op_data=op_data)
    adds = [c for c in operation.changes if c.action == "add"]
    removes = [c for c in operation.changes if c.action == "remove"]
    assert len(adds) == 1
    assert len(removes) == 1
    assert adds[0].component_id == component.id
    assert removes[0].component_id == component.id
