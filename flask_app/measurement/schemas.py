from marshmallow import Schema, validate, fields, validates_schema, ValidationError


class MeasurementGet(Schema):  # GET uopste ne ulazi dump -- procitaj jos

    id = fields.Int(required=True, allow_none=False)
    temperature = fields.Int(required=True, allow_none=False)
    air_quality = fields.Int(required=True, allow_none=False)
    humidity = fields.Int(required=True, allow_none=False)
    created_datetime = fields.DateTime(required=True)



class MeasurementPost(Schema):
    id = fields.Int(required=False, allow_none=False)
    temperature = fields.Int(required=True, allow_none=False)
    air_quality = fields.Int(required=True, allow_none=False)
    humidity = fields.Int(required=True, allow_none=False)
    created_datetime = fields.DateTime(required=False)


    @validates_schema
    def validate_parameters(self, data, **kwargs):

        if data["temperature"] < 0:
            raise ValidationError("Temperature error")

        if data["humidity"] < 0 or data["humidity"] > 100:
            raise ValidationError("humidity error")

        if data["air_quality"] < 0 or data["air_quality"] > 100:
            raise ValidationError("air_quality error")

