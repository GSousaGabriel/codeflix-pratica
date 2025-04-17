from abc import ABC
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T= TypeVar("T")

@dataclass
class ListPaginationInput:
    order_by: str = "id"
    current_page: int | str = 1
    
    def __post_init__(self):
        self.current_page = int(self.current_page)

@dataclass
class MetaPaginationOutput:
    current_page: int
    per_page: int
    total: int
    
@dataclass
class ListEntityResponse(Generic[T]):
    data: list[T]
    meta: MetaPaginationOutput = field(default_factory=MetaPaginationOutput)
    
@dataclass
class ListEntity(ABC):
    def paginate_data(self, page: int, sorted_data: list[T]) -> ListEntityResponse[T]:
        DEFAULT_PAGE_SIZE = 2
        page_offset = (page-1) * DEFAULT_PAGE_SIZE
        categories_paginated = sorted_data[page_offset: page_offset + DEFAULT_PAGE_SIZE]
        
        return ListEntityResponse(
            data = categories_paginated,
            meta = MetaPaginationOutput(
                current_page = page,
                per_page = DEFAULT_PAGE_SIZE,
                total = len(sorted_data)
            )
        )