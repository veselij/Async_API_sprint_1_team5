from fastapi.param_functions import Query
from pydantic import BaseModel


class PaginatedParams(BaseModel):

    page_num: int = Query(1, ge=1)
    page_size: int = Query(50, ge=1)

    def get_starting_doc(self) -> int:
        return (self.page_num - 1) * self.page_size
