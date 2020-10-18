from domain.repositories import ReportRepositoryInterface
from infrastructure.database import reports_table
from infrastructure.repositories import BaseRepository


class ReportRepository(BaseRepository, ReportRepositoryInterface):

    def insert(self, report):
        with self.db_connection.begin():
            self.db_connection.execute(
                reports_table.insert(),
                report.as_dict()
            )
