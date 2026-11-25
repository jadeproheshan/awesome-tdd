"""仅依赖 Python 标准库的内存积分账户。"""


class PointsAccount:
    def __init__(self) -> None:
        self._balance = 0

    @property
    def balance(self) -> int:
        """当前积分余额。"""
        return self._balance

    def add(self, points: int) -> None:
        """增加正整数积分；类型错误抛 TypeError，非正数抛 ValueError。"""
        self._validate_points(points)
        self._balance += points

    def spend(self, points: int) -> None:
        """消费正整数积分；无效输入或余额不足时拒绝且保持余额。"""
        self._validate_points(points)
        if points > self._balance:
            raise ValueError("insufficient points")
        self._balance -= points

    @staticmethod
    def _validate_points(points: int) -> None:
        if isinstance(points, bool) or not isinstance(points, int):
            raise TypeError("points must be an integer")
        if points <= 0:
            raise ValueError("points must be positive")
