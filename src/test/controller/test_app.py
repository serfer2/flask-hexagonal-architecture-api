import io
from unittest.mock import patch

from expects import (
    be_true,
    equal,
    expect,
    have_keys
)

from infrastructure.repositories import ReportRepository
from test import BaseTestCase


class AcquirePdfEndpointTestCase(BaseTestCase):

    def test_endpoint_status_can_be_checked(self):
        response = self.client.get('/acquire/pdf')

        expect(response.status_code).to(equal(200))
        expect(response.json).to(equal({'status': 'alive!'}))

    def test_it_returns_bad_request_when_no_file_posted(self):
        response = self.client.post('/acquire/pdf', data={})

        expect(response.status_code).to(equal(400))
        expect(response.json).to(equal({'file': 'mandatory'}))

    def test_it_returns_bad_request_when_invalid_file_type(self):
        wrong_file = (io.BytesIO(b"Some text"), 'report.doc')
        data = {'file': wrong_file}

        response = self.client.post('/acquire/pdf', data=data)

        expect(response.status_code).to(equal(400))
        expect(response.json).to(equal({'file': 'wrong file type'}))

    @patch('controller.app.AcquirePdfFile.do')
    def test_it_calls_application_service_with_pdf_file_content(self, application_service):
        pdf_file = (io.BytesIO(b"Some text"), 'report.pdf')
        data = {'file': pdf_file}
        application_service.return_value = "Doesn't matter"

        self.client.post('/acquire/pdf', data=data)

        application_service.assert_called_with(
            file_content=b"Some text",
        )

    def test_it_returns_extracted_plain_text(self):
        pdf_file = (io.BytesIO(b"Some plain text"), 'report.pdf')
        data = {'file': pdf_file}

        response = self.client.post('/acquire/pdf', data=data)

        expect(response.status_code).to(equal(200))
        expect(response.json).to(equal(
            {'plain_text': 'Some plain text'})
        )


class AnonymizeTxtEndpointTestCase(BaseTestCase):

    def test_endpoint_status_can_be_checked(self):
        response = self.client.get('/anonymize/txt')

        expect(response.status_code).to(equal(200))
        expect(response.json).to(equal({'status': 'alive!'}))

    def test_it_returns_bad_request_when_no_file_posted(self):
        response = self.client.post('/anonymize/txt', data={})

        expect(response.status_code).to(equal(400))
        expect(response.json).to(equal({'file': 'mandatory'}))

    def test_it_returns_bad_request_when_invalid_file_type(self):
        wrong_file = (io.BytesIO(b"Some text"), 'report.pdf')
        data = {'file': wrong_file}

        response = self.client.post('/anonymize/txt', data=data)

        expect(response.status_code).to(equal(400))
        expect(response.json).to(equal({'file': 'wrong file type'}))

    @patch('controller.app.AnonymizeTxtFile.do')
    def test_it_calls_application_service(self, application_service):
        pdf_file = (io.BytesIO(b"Some text"), 'Report1.txt')
        data = {'file': pdf_file}
        application_service.return_value = "Doesn't matter"

        self.client.post('/anonymize/txt', data=data)

        kwargs = application_service.call_args.kwargs
        expect(kwargs['file_content']).to(equal("Some text"))
        expect(
            isinstance(kwargs['repository'], ReportRepository)
        ).to(be_true)

    @patch('controller.app.AnonymizeTxtFile.do')
    def test_it_returns_anonymized_content(self, application_service):
        pdf_file = (io.BytesIO(b"Some text"), 'Report1.txt')
        data = {'file': pdf_file}
        application_service.return_value = {
            'patient_id': '1234',
            'document_text': 'She\'s in good health!'
        }

        response = self.client.post('/anonymize/txt', data=data)
        expect(response.status_code).to(equal(200))
        expect(response.json).to(have_keys({
            'patient_id': '1234',
            'document_text': 'She\'s in good health!'
        }))
