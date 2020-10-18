from controller.exceptions import BadRequestException


def file_by_mimetype(request, mimetype):
    if 'file' not in request.files:
        raise BadRequestException({'file': 'mandatory'})

    file = request.files['file']
    if file.mimetype != mimetype:
        raise BadRequestException({'file': 'wrong file type'})

    return file
