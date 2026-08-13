import json
import time

REPEAT = 10
WARMUP = 3


def mac(pattern, filt):
    """같은 위치끼리 곱해서 전부 더한다."""
    total = 0.0
    for r in range(len(pattern)):
        for c in range(len(pattern)):
            total = total + pattern[r][c] * filt[r][c]
    return total


def make_cross(n):
    """n x n 십자가 패턴을 만든다."""
    mid = n // 2
    return [[1.0 if (r == mid or c == mid) else 0.0 for c in range(n)]
            for r in range(n)]


def make_x(n):
    """n x n X 패턴을 만든다."""
    return [[1.0 if (r == c or r + c == n - 1) else 0.0 for c in range(n)]
            for r in range(n)]


def measure_avg_ms(pattern, filt, repeat=REPEAT):
    """MAC 연산만 repeat회 반복 측정하고 평균 시간(ms)을 돌려준다."""
    for _ in range(WARMUP):
        mac(pattern, filt)

    total_sec = 0.0
    for _ in range(repeat):
        start = time.perf_counter()
        mac(pattern, filt)
        total_sec = total_sec + (time.perf_counter() - start)

    return (total_sec / repeat) * 1000.0


def print_performance(sizes, repeat=REPEAT):
    """크기별 평균 시간과 연산 횟수를 표로 출력한다."""
    print('\n[성능 분석] MAC 연산 %d회 반복 평균' % repeat)
    print('-' * 46)
    print('%-10s %16s %14s' % ('크기', '평균 시간(ms)', '연산 횟수(N^2)'))
    print('-' * 46)

    for n in sizes:
        avg_ms = measure_avg_ms(make_cross(n), make_x(n), repeat)
        print('%-10s %16.6f %14d' % ('%dx%d' % (n, n), avg_ms, n * n))

    print('-' * 46)


print_performance([3, 5, 13, 25])