import pytest
from typing import List
from math import inf


def cut_rod(p: List[int], n: int) -> int:
    """
    自顶向下的递归实现
    会重复计算已经计算过的子问题
    """
    if n == 0:
        return 0
    q = -inf
    # ! i的遍历范围为[1..j],目的是为了跟长度的物理意义统一,方便理解,在获取长度为i的钢条的价值时要用p[i - 1]来获取
    for i in range(1, n + 1):
        q = max(q, p[i - 1] + cut_rod(p, n - i))
    return q


def memoized_cut_rod_aux(p: List[int], n: int, r: List[int]) -> int:
    """
    带备忘的自顶向下法(记忆化搜索)
    还是递归实现,不过在第一次计算某个子问题时将其保存起来,后续直接查询
    """
    if r[n] >= 0:
        return r[n]
    if n == 0:
        q = 0
    else:
        q = -inf
        # ! i的遍历范围为[1..n],目的是为了跟长度的物理意义统一,方便理解,在获取长度为i的钢条的价值时要用p[i - 1]来获取
        for i in range(1, n + 1):
            q = max(q, p[i - 1] + memoized_cut_rod_aux(p, n - i, r))

    r[n] = q
    return q


def memoized_cut_rod(p: List[int], n: int) -> int:
    """
    初始化备忘录,调用递归函数
    """
    r = [-inf] * (len(p) + 1)
    return memoized_cut_rod_aux(p, n, r)


def bottom_up_cut_rod(p: List[int], n: int) -> int:
    """
    自底向上法(常规意义上的动态规划)
    """
    r = [0] * (len(p) + 1)
    # ! j的遍历为[1..n],i的遍历为[1..j],目的是为了跟长度的物理意义统一,方便理解,在获取长度为i的钢条的价值时要用p[i - 1]来获取
    for j in range(1, n + 1):
        q = -inf
        for i in range(1, j + 1):
            q = max(q, p[i - 1] + r[j - i])
        r[j] = q
    return r[n]


def extended_bottom_up_cut_rod(p: List[int], n: int) -> int:
    """
    s[i]的物理意义是,当当前长度为i时,切断钢条的左边部分的长度
    """
    r = [0] * (len(p) + 1)
    s = [0] * (len(p) + 1)
    for j in range(1, n + 1):
        q = -inf
        for i in range(1, j + 1):
            if q < p[i - 1] + r[j - i]:
                q = p[i - 1] + r[j - i]
                s[j] = i

        r[j] = q
    return r, s


def print_cut_rod_solution(p: List[int], n: int) -> None:
    """
    输出的时候是从n开始
    """
    _, s = extended_bottom_up_cut_rod(p, n)
    while n > 0:
        print(s[n])
        n = n - s[n]


p = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
# * 将长度为10的钢条[10]划分为[10]
print_cut_rod_solution(p, 10)
print("---")
# * 将长度为7的钢条[7]划分为[1, 6]
print_cut_rod_solution(p, 7)

test_data = [
    (p, 0, 0),
    (p, 1, 1),
    (p, 2, 5),
    (p, 3, 8),
    (p, 4, 10),
    (p, 5, 13),
    (p, 6, 17),
    (p, 7, 18),
    (p, 8, 22),
    (p, 9, 25),
    (p, 10, 30),
]


@pytest.mark.parametrize("p, n, expected", test_data)
def test_cut_rod(p, n, expected):
    assert cut_rod(p, n) == expected


@pytest.mark.parametrize("p, n, expected", test_data)
def test_memoized_cut_rod(p, n, expected):
    assert memoized_cut_rod(p, n) == expected


@pytest.mark.parametrize("p, n, expected", test_data)
def test_bottom_up_cut_rod(p, n, expected):
    assert bottom_up_cut_rod(p, n) == expected
