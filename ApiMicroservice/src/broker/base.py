import typing as tp
from abc import abstractmethod


class IBrokerProducer(tp.Protocol):
    @abstractmethod
    async def produce(self, message: str) -> None: ...
