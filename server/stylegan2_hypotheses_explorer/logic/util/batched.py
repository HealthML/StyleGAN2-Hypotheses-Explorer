from typing import Iterable, List, TypeVar

ContentT = TypeVar("ContentT")


def batched(iterable: Iterable[ContentT], batch_size: int) -> Iterable[List[ContentT]]:
    try:
        batch = [None for _ in range(batch_size)]
        while True:
            for index in range(batch_size):
                batch[index] = next(iterable)
            yield batch
    except StopIteration:
        if index > 0:
            yield batch[:index]
