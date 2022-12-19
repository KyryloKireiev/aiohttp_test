from marshmallow import Schema, fields
from marshmallow.validate import Length


class SignUpSchema(Schema):
    username = fields.String(required=True, validate=Length(min=3, max=50))
    password = fields.String(required=True, validate=Length(min=8, max=25))


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    created_at = fields.DateTime()
