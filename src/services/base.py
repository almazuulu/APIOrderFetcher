from __future__ import annotations

import abc
import logging

logger = logging.getLogger("api")


class BaseService(abc.ABC):
    @abc.abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError()
