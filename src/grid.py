import numpy as np
import numpy.typing as npt
from states import FieldState


class Grid:
    def __init__(self, size: int = 3) -> None:
        self.__data: npt.NDArray[np.int32] = np.zeros((size, size), dtype=np.int32)

    @property
    def size(self) -> int:
        return self.__data.shape[0]

    @size.setter
    def size(self, size: int) -> None:
        if size == 0:
            return

        if self.__data.shape != (size, size):
            self.__data = np.zeros((size, size), dtype=np.int32)

    def iterator(self):
        for x, y in np.ndindex(self.__data.shape):
            yield FieldState(self.__data[x, y]), x, y

    @property
    def code(self) -> int:
        res = 0

        for val, _, _ in self.iterator():
            res *= len(FieldState)
            res += int(val)

        return res

    def __getitem__(self, indicies: tuple[int, int]) -> FieldState:
        return FieldState(self.__data[indicies])

    def __setitem__(self, indicies: tuple[int, int], value: FieldState) -> None:
        self.__data[indicies] = int(value)

    def __str__(self) -> str:
        return "\n".join(
            "".join(
                "[ ]"
                if item == int(FieldState.EMPTY)
                else "[X]"
                if item == int(FieldState.CROSS)
                else "[O]"
                for item in row
            )
            for row in self.__data
        )

    def clone(self) -> "Grid":
        res = Grid(0)
        res.__data = np.copy(self.__data)
        return res
