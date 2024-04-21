from __future__ import annotations

import abc


class BaseService(abc.ABC):
    @abc.abstractmethod
    def __init__(self) -> None:
        pass