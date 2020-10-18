from expects import (
    equal,
    expect
)

from infrastructure.repositories import ReportRepository
from test import BaseTestCase


class StubReport:

    def as_dict(self):
        return {
            'patient_id': '123456',
            'document_text': 'Any random text'
        }


class ReportRepositoryTestCase(BaseTestCase):

    def test_it_inserts_a_report(self):
        report = StubReport()
        repository = ReportRepository(self.db_connection)
        query = "SELECT * FROM report WHERE patient_id = '123456'"

        repository.insert(report)

        expect(self._read_from_db(query)).to(
            equal({
                'patient_id': '123456',
                'document_text': 'Any random text'
            })
        )

    def _read_from_db(self, sql_query):
        registry = self.db_connection.execute(sql_query).first()
        return dict(registry.items())
