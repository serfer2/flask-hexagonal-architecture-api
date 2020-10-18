from abc import (
    ABCMeta,
    abstractmethod
)


class ReportRepositoryInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def insert(self, report):
        pass
