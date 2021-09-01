from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from typing import Dict, Generic, List, TypeVar
from weakref import ReferenceType, ref

Backend = TypeVar('Backend')


class BackendLazyLoader(ABC, Generic[Backend]):
    _allocated_backends_dict: Dict[type,
                                   List[ReferenceType[BackendLazyLoader]]] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._backend = None

    def __del__(self):
        self.deallocate_backend()

    @abstractproperty
    def max_allocated_backends(self) -> int:
        pass

    @abstractmethod
    def construct_backend(self) -> Backend:
        pass

    @property
    def backend(self) -> Backend:
        if not self.backend_is_allocated:
            self._allocate_backend()
        return self._backend

    def deallocate_backend(self):
        allocated_backends = self._allocated_backends
        new_allocated_backends = [backend
                                  for backend in self._allocated_backends
                                  if backend != ref(self) and backend() is not None]
        allocated_backends.clear()
        allocated_backends.extend(new_allocated_backends)

    @property
    def _allocated_backends(self) -> List[ReferenceType[BackendLazyLoader]]:
        if type(self) not in BackendLazyLoader._allocated_backends_dict:
            BackendLazyLoader._allocated_backends_dict[type(self)] = []
        return BackendLazyLoader._allocated_backends_dict[type(self)]

    def _allocate_backend(self):
        allocated_backends = self._allocated_backends
        while len(allocated_backends) >= self.max_allocated_backends:
            next_backend = allocated_backends[0]()
            if next_backend is None:
                allocated_backends.pop(0)
            else:
                next_backend.deallocate_backend()
        self._backend = self.construct_backend()
        allocated_backends.append(ref(self))

    @property
    def backend_is_allocated(self):
        return self._backend is not None
