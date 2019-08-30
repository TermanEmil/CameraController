from typing import Iterable


class EmailingSettings:
    @property
    def emails(self) -> Iterable[str]:
        raise NotImplementedError()

    @property
    def email_subject_prefix(self) -> str:
        raise NotImplementedError()