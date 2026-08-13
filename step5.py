import json

EPSILON = 1e-9

# 막힘 3의 결정: 표기 통일표
LABEL_TABLE = {
    '+': 'Cross',
    'cross': 'Cross',
    'x': 'X',
}


def normalize_label(raw):
    """제각각인 표기를 Cross / X 로 통일. 표에 없으면 None."""
    if raw is None:
        return None
    return LABEL_TABLE.get(str(raw).strip().lower())


def size_from_key(key):
    """'size_5_1' 에서 5를 뽑는다."""
    parts = key.split('_')
    return int(parts[1])


def mac(pattern, filt):
    """같은 위치끼리 곱해서 전부 더한다."""
    total = 0.0
    for r in range(len(pattern)):
        for c in range(len(pattern)):
            total = total + pattern[r][c] * filt[r][c]
    return total


def judge(score_cross, score_x):
    """점수가 높은 쪽. 차이가 EPSILON 미만이면 동점."""
    if abs(score_cross - score_x) < EPSILON:
        return 'UNDECIDED'
    if score_cross > score_x:
        return 'Cross'
    return 'X'


def check_case(key, item, filters):
    """한 케이스를 검증하고 (Cross점수, X점수, 판정, 기대라벨) 을 돌려준다.
    문제가 있으면 ValueError 를 낸다."""
    n = size_from_key(key)

    filter_key = 'size_%d' % n
    if filter_key not in filters:
        raise ValueError('%s 필터가 없습니다' % filter_key)

    grid = item['input']
    if len(grid) != n:
        raise ValueError('키는 %d를 가리키는데 실제 배열은 %d행' % (n, len(grid)))

    filter_set = filters[filter_key]
    cross_filter = normalize_filters(filter_set)['Cross']
    x_filter = normalize_filters(filter_set)['X']

    if len(cross_filter) != n or len(x_filter) != n:
        raise ValueError('필터 크기가 %d가 아닙니다' % n)

    expected = normalize_label(item.get('expected'))
    if expected is None:
        raise ValueError('알 수 없는 expected 값: %r' % item.get('expected'))

    score_cross = mac(grid, cross_filter)
    score_x = mac(grid, x_filter)
    return score_cross, score_x, judge(score_cross, score_x), expected


def normalize_filters(filter_set):
    """필터 키 'cross' / 'x' 도 표준 라벨로 바꿔서 담는다."""
    result = {}
    for raw_key in filter_set:
        label = normalize_label(raw_key)
        if label is not None:
            result[label] = filter_set[raw_key]
    if 'Cross' not in result or 'X' not in result:
        raise ValueError('필터에 cross/x 가 모두 있어야 합니다')
    return result


with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

filters = data['filters']
patterns = data['patterns']

total_count = 0
pass_count = 0
failures = []

print('%-12s %10s %10s %-10s %-8s %s'
      % ('케이스', 'Cross점수', 'X점수', '판정', '기대', '결과'))
print('-' * 64)

for key in patterns:
    total_count = total_count + 1
    try:
        score_cross, score_x, verdict, expected = check_case(
            key, patterns[key], filters)
    except (ValueError, KeyError, TypeError, IndexError) as err:
        failures.append((key, str(err)))
        print('%-12s %10s %10s %-10s %-8s %s' % (key, '-', '-', '-', '-', 'FAIL'))
        continue

    if verdict == expected:
        pass_count = pass_count + 1
        result = 'PASS'
    else:
        failures.append((key, '판정 %s, 기대 %s' % (verdict, expected)))
        result = 'FAIL'

    print('%-12s %10.4f %10.4f %-10s %-8s %s'
          % (key, score_cross, score_x, verdict, expected, result))

print('-' * 64)
print('전체 %d개 / 통과 %d개 / 실패 %d개'
      % (total_count, pass_count, total_count - pass_count))

if failures:
    print('\n[실패 케이스]')
    for key, reason in failures:
        print('  %-12s %s' % (key, reason))