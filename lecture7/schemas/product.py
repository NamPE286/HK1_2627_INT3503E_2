from marshmallow import Schema, fields, validate


class ProductInSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    price = fields.Int(load_default=0, validate=validate.Range(min=0))
    stock = fields.Int(load_default=0, validate=validate.Range(min=0))


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    price = fields.Int()
    stock = fields.Int()
    created_at = fields.Str(dump_only=True)
