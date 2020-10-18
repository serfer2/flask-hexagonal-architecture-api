class WrongFileStructureException(Exception):

    def __init__(self, data=None):
        Exception.__init__(self)
        self.data = data or {}

    def to_dict(self):
        return self.data
