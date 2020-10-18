from expects import (
    equal,
    expect,
    raise_error
)

from application.exceptions import WrongFileStructureException
from application.services import AnonymizeTxtFile
from domain.repositories import ReportRepositoryInterface
from test import BaseTestCase


class FakeReportRepository(ReportRepositoryInterface):

    def __init__(self):
        self.__reports = {}

    def insert(self, report):
        self.__reports[report.patient_id] = report

    def get_by_patient_id(self, patient_id):
        return self.__reports[patient_id]


class AnonymizeTxtFileTestCase(BaseTestCase):

    def test_it_raises_exception_when_wrong_file_content_structure(self):
        wrong_file_content = 'Bad news.\nThis is wrong.'

        expect(lambda: AnonymizeTxtFile().do(
            file_content=wrong_file_content,
            repository=FakeReportRepository()
        )).to(raise_error(WrongFileStructureException))

    def test_it_raises_exception_when_no_mr_in_report_header(self):
        wrong_header = (
            'Random data\n'
            'Some other header data\n'
        )
        free_text = (
            'Free text body, full of important data and\n'
            'annotations that we should save.\n'
            'We hope this report is good news for patient :)\n'
        )

        expect(lambda: AnonymizeTxtFile().do(
            file_content=f'{wrong_header}\n{free_text}',
            repository=FakeReportRepository()
        )).to(raise_error(WrongFileStructureException))

    def test_it_rerturns_free_text_and_hashed_medical_record_number(self):
        mr = '1234567890'
        hashed_mr = '9d752daa3fb4df29837088e1e5a1acf74932e074'
        header = (
            f'MR: {mr}\n'
            'Some other header data\n'
        )
        free_text = (
            'Free text body, full of important data and\n'
            'annotations that we should save.\n'
            'We hope this report is good news for patient :)'
        )

        result = AnonymizeTxtFile().do(
            file_content=f'{header}\n{free_text}',
            repository=FakeReportRepository()
        )

        expect(result['patient_id']).to(equal(hashed_mr))
        expect(result['document_text']).to(equal(free_text))

    def test_it_persists_report_in_repository(self):
        mr = '1234567890'
        hashed_mr = '9d752daa3fb4df29837088e1e5a1acf74932e074'
        header = (
            f'MR: {mr}\n'
            'Some other header data\n'
        )
        free_text = (
            'Free text body, full of important data and\n'
            'annotations that we should save.\n'
            'We hope this report is good news for patient :)'
        )
        repository = FakeReportRepository()

        result = AnonymizeTxtFile().do(
            file_content=f'{header}\n{free_text}',
            repository=repository
        )

        report = repository.get_by_patient_id(result['patient_id'])
        expect(report.patient_id).to(equal(hashed_mr))
        expect(report.document_text).to(equal(free_text))
