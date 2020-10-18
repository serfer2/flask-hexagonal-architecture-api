class Report:

    def __init__(self, patient_id, document_text):
        self.patient_id = patient_id
        self.document_text = document_text

    def __repr__(self):
        return f'<Report {self.patient_id}>'

    def as_dict(self):
        return {
            'patient_id': self.patient_id,
            'document_text': self.document_text
        }
