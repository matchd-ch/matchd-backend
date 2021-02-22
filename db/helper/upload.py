from db.validators import UploadValidator


def validate_upload(file, types=None, size=None):
    image_validator = UploadValidator(max_size=size, content_types=types)
    image_validator(file)
