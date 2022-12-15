from marshmallow import Schema, ValidationError, fields, validates_schema


class UserValidation(Schema):
    username = fields.String()
    password = fields.String()

    @validates_schema
    def valid_fields(self, data, **kwargs):
        if len(data) != 2:
            raise ValidationError("you mast fill two field: username and password")

        name = data["username"]
        password = data["password"]

        if not 3 <= len(name) <= 50:
            raise ValidationError("username: min length 3, max length 50")

        if not 8 <= len(password) <= 25:
            raise ValidationError("password: min length 8, max length 25")
