from marshmallow import fields, Schema, validate

class SignUpSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    userid = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=8))

class SignInSchema(Schema):
    userid = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))