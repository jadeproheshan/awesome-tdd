"""积分账户的最小可调用契约；本轮不实现业务。"""


class PointsAccount:
    @property
    def balance(self) -> int:
        """当前积分余额。"""
        ...

    def add(self, points: int) -> None:
        """增加正整数积分；类型错误抛 TypeError，非正数抛 ValueError。"""
        ...

    def spend(self, points: int) -> None:
        """消费正整数积分；无效输入或余额不足时拒绝且保持余额。"""
        ...
