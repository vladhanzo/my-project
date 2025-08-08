from sqlalchemy.orm import Session
from sqlalchemy import select, func
from backend.app.models.component import ComponentAction, Component, Assembly
from backend.app.schemas.component import ComponentInAssembly
from typing import List
from collections import defaultdict


def get_assembly_components(db: Session, assembly_id: int) -> List[ComponentInAssembly]:
    subquery = (
        select(
            ComponentAction.component_id,
            func.sum(
                func.case(
                    (ComponentAction.action == "add", ComponentAction.quantity),
                    (ComponentAction.action == "remove", -ComponentAction.quantity),
                    else_=0
                )
            ).label("net_quantity")
        )
        .where(ComponentAction.assembly_id == assembly_id)
        .group_by(ComponentAction.component_id)
        .subquery()
    )

    result = (
        db.query(
            Component.id,
            Component.name,
            subquery.c.net_quantity
        )
        .join(subquery, Component.id == subquery.c.component_id)
        .filter(subquery.c.net_quantity > 0)
        .all()
    )

    return [
        ComponentInAssembly(id=row.id, name=row.name, quantity=row.net_quantity)
        for row in result
    ]
