from uuid import UUID
from datetime import datetime
import json
from sqlalchemy.orm import Session
from sqlalchemy import and_
from jsonschema import validate, ValidationError
from app.models.model import Model
from app.models.revision import Revision
from app.models.audit_log import AuditLog

class ModelService:
    def __init__(self, db: Session):
        self.db = db

    def create_revision(self, model_id: UUID, changes: dict) -> Revision:
        model = self.db.query(Model).filter(Model.id == model_id).one()
        last = (
            self.db.query(Revision)
            .filter(Revision.model_id == model_id)
            .order_by(Revision.created_at.desc())
            .first()
        )
        old_version = last.version if last else "0.0.0"
        major, minor, patch = map(int, old_version.split("."))
        new_version = f"{major}.{minor}.{patch+1}"
        if last:
            last.active = False
        rev = Revision(
            model_id=model.id,
            version=new_version,
            config=changes,
            active=True,
            created_at=datetime.utcnow(),
        )
        self.db.add(rev)
        log = AuditLog(
            action="create_revision",
            model_id=model.id,
            revision_id=rev.id,
            timestamp=datetime.utcnow(),
            details=json.dumps({"version": new_version, "changes": changes}),
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(rev)
        return rev

    def get_active_config(self, model_code: str) -> dict:
        rev = (
            self.db.query(Revision)
            .join(Model, Revision.model_id == Model.id)
            .filter(and_(Model.code == model_code, Revision.active.is_(True)))
            .one()
        )
        return rev.config

    def validate_assembly(self, assembly_data: dict, revision_id: UUID) -> bool:
        rev = self.db.query(Revision).filter(Revision.id == revision_id).one()
        try:
            validate(instance=assembly_data, schema=rev.config)
        except ValidationError as e:
            log = AuditLog(
                action="validate_assembly_failed",
                model_id=rev.model_id,
                revision_id=rev.id,
                timestamp=datetime.utcnow(),
                details=json.dumps({"error": e.message}),
            )
            self.db.add(log)
            self.db.commit()
            return False
        log = AuditLog(
            action="validate_assembly_success",
            model_id=rev.model_id,
            revision_id=rev.id,
            timestamp=datetime.utcnow(),
            details=json.dumps({"assembly": assembly_data}),
        )
        self.db.add(log)
        self.db.commit()
        return True
