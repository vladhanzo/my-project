from sqlalchemy.orm import Session
from app.models.assembly import AssemblyModel
from app.models.product import ProductModel

def get_deviation(db: Session, assembly_id: int) -> dict:
    assembly = db.query(AssemblyModel).filter(AssemblyModel.id == assembly_id).first()
    if assembly is None:
        return {"percentage_match": 0.0, "discrepancies": []}
    product = db.query(ProductModel).filter(ProductModel.id == assembly.product_id).first()
    standard = product.standard_components  # list of dicts: {"component_id": ..., "quantity": ...}
    actual = assembly.components          # list of dicts: {"component_id": ..., "quantity": ...}
    total_expected = sum(item["quantity"] for item in standard)
    matched = 0
    discrepancies = []
    for std in standard:
        comp = next((a for a in actual if a["component_id"] == std["component_id"]), None)
        actual_qty = comp["quantity"] if comp else 0
        if actual_qty == std["quantity"]:
            matched += std["quantity"]
        else:
            discrepancies.append({
                "component_id": std["component_id"],
                "expected": std["quantity"],
                "actual": actual_qty
            })
    percentage_match = (matched / total_expected) * 100 if total_expected else 100.0
    return {"percentage_match": percentage_match, "discrepancies": discrepancies}
