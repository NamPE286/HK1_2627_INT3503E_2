from flask import Blueprint, request, jsonify
from extensions import db
from models.product import Product
from schemas.product import ProductInSchema, ProductSchema

bp = Blueprint("products", __name__, url_prefix="/api/v1/products")

product_in = ProductInSchema()
product_out = ProductSchema()
products_out = ProductSchema(many=True)


@bp.get("")
def list_products():
    rows = db.session.execute(db.select(Product)).scalars().all()
    return jsonify(products_out.dump(rows)), 200


@bp.post("")
def create_product():
    data = request.get_json(silent=True) or {}
    errors = product_in.validate(data)
    if errors:
        return jsonify({"errors": errors}), 422
    body = product_in.load(data)
    p = Product(**body)
    db.session.add(p)
    db.session.commit()
    return jsonify(product_out.dump(p)), 201


@bp.get("/<int:pid>")
def get_product(pid):
    p = db.get_or_404(Product, pid)
    return jsonify(product_out.dump(p)), 200


@bp.put("/<int:pid>")
def update_product(pid):
    p = db.get_or_404(Product, pid)
    data = request.get_json(silent=True) or {}
    errors = product_in.validate(data, partial=True)
    if errors:
        return jsonify({"errors": errors}), 422
    body = product_in.load(data, partial=True)
    for k, v in body.items():
        setattr(p, k, v)
    db.session.commit()
    return jsonify(product_out.dump(p)), 200


@bp.delete("/<int:pid>")
def delete_product(pid):
    p = db.get_or_404(Product, pid)
    db.session.delete(p)
    db.session.commit()
    return "", 204
