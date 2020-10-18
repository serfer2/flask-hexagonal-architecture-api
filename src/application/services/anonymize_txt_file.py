import hashlib
import re

from domain.models import Report
from ..exceptions import WrongFileStructureException


class AnonymizeTxtFile:
    # TODO:  we're assuming MR is number with four digits or more.

    def __init__(self):
        self.section_split_rule = re.compile('\n{2}')
        self.medical_record_rule = re.compile(' \d{4,}')

    def do(self, file_content, repository):
        sections = [section.strip() for section in self.section_split_rule.split(file_content) if section.strip() != '']

        if len(sections) < 2:
            error = {'file': 'wrong structure'}
            raise WrongFileStructureException(error)

        mr = self._mr(header=sections[0])
        if not mr:
            error = {'file': 'MR not found'}
            raise WrongFileStructureException(error)

        report = Report(
            patient_id=self._patient_id(mr),
            document_text=sections[1]
        )
        repository.insert(report)

        return {
            'patient_id': report.patient_id,
            'document_text': report.document_text
        }

    def _mr(self, header):
        match = self.medical_record_rule.search(header)
        if not match:
            return ''
        return match.group(0).strip()

    def _patient_id(self, mr):
        _hash = hashlib.new('ripemd160')
        _hash.update(bytes(mr, 'utf-8'))
        return _hash.hexdigest()
