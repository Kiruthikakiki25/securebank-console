import bisect
import timeit
from sortedcontainers import SortedDict


def bench_bisect(n: int):
    data = []
    for i in range(n):
        bisect.insort(data, i)


def bench_sorteddict(n: int):
    sd = SortedDict()
    for i in range(n):
        sd[i] = i


def bisect_demo():
    ids = []
    for acc_id in [105, 101, 110, 103]:
        bisect.insort(ids, acc_id)         
    print("Sorted IDs via bisect.insort:", ids)  

    # bisect_left / bisect_right — find insertion point
    pos = bisect.bisect_left(ids, 103)
    print("bisect_left(103):", pos)         

    
    sd = SortedDict({101: "A", 103: "B", 105: "C", 110: "D"})
    print("irange(100, 108):", list(sd.irange(100, 108))) 


if __name__ == "__main__":
    bisect_demo()
    print()
    print(f"{'n':>8}  {'bisect':>12}  {'SortedDict':>12}")
    print("-" * 36)
    for size in [1000, 5000, 10000]:
        t1 = timeit.timeit(lambda: bench_bisect(size), number=3)
        t2 = timeit.timeit(lambda: bench_sorteddict(size), number=3)
        print(f"{size:>8}  {t1:>12.4f}s  {t2:>12.4f}s")