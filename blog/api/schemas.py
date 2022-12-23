from marshmallow import Schema, fields
from marshmallow.validate import Length, Range


class SignUpSchema(Schema):
    username = fields.String(required=True, validate=Length(min=3, max=50))
    password = fields.String(required=True, validate=Length(min=8, max=25))


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    created_at = fields.DateTime()


class UserListSchema(Schema):
    users = fields.Nested(UserSchema(many=True))
    count = fields.Integer()
    previous_page = fields.URL()
    next_page = fields.URL()


class PageQueryParamsSchema(Schema):
    page = fields.Integer(
        required=True, validate=[Range(min=1, error="Number of page must be above 0")]
    )
    count = fields.Integer(
        required=True,
        validate=[Range(min=1, error="Count of elements must be above 0")],
    )
