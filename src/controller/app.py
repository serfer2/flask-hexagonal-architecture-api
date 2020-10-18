import os

from flask import (
    Flask,
    g,
    jsonify,
    request
)

from application.exceptions import WrongFileStructureException
from application.services import (
    AcquirePdfFile,
    AnonymizeTxtFile
)
from controller.exceptions import BadRequestException
from controller.utils import file_by_mimetype
from infrastructure.database import (
    close_db_connection,
    init_db_engine,
    db_connect
)
from infrastructure.repositories import ReportRepository


app = Flask(__name__)


def get_db_connection(app):
    if 'db_con' not in g:
        db_engine = app.config.get('DB_ENGINE', None) or init_db_engine()
        g.db_con = db_connect(db_engine)
    return g.db_con


@app.errorhandler(BadRequestException)
@app.errorhandler(WrongFileStructureException)
def handle_bad_request(error):
    response = jsonify(error.to_dict())
    response.status_code = 400
    return response


@app.route('/acquire/pdf', methods=['GET', 'POST'])
def acquire_pdf():
    if request.method == 'GET':
        return jsonify({'status': 'alive!'})

    file = file_by_mimetype(request, 'application/pdf')
    plain_text = AcquirePdfFile().do(
        file_content=file.stream.read()
    )

    return jsonify({'plain_text': plain_text})


@app.route('/anonymize/txt', methods=['GET', 'POST'])
def anonymize_txt():
    if request.method == 'GET':
        return jsonify({'status': 'alive!'})

    file = file_by_mimetype(request, 'text/plain')
    anonymized_data = AnonymizeTxtFile().do(
        file_content=file.stream.read().decode("utf-8"),
        repository=ReportRepository(get_db_connection(app))
    )

    return jsonify(anonymized_data)


@app.teardown_appcontext
def teardown_db(exception=None):
    db_con = g.pop('db_con', None)
    if db_con is not None:
        close_db_connection(db_con)


if __name__ == '__main__':
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'))
