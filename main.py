import json
import time

EPSILON = 1e-9
REPEAT = 10
WARMUP = 3
SIZE_MODE1 = 3
DATA_FILE = 'data.json'

LABEL_TABLE = {
    '+': 'Cross',
    'cross': 'Cross',
    'x': 'X',
}


# ---------- 공용 ----------

def normalize_label(raw):
    """제각각인 표기를 Cross / X 로 통일. 표에 없으면 None."""
    if raw is None:
        return None
    return LABEL_TABLE.get(str(raw).strip().lower())


def mac(pattern, filt):
    """같은 위치끼리 곱해서 전부 더한다."""
    total = 0.0
    for r in range(len(pattern)):
        for c in range(len(pattern)):
            total = total + pattern[r][c] * filt[r][c]
    return total


def judge(score_a, score_b, label_a, label_b):
    """점수가 높은 쪽. 차이가 EPSILON 미만이면 UNDECIDED."""
    if abs(score_a - score_b) < EPSILON:
        return 'UNDECIDED'
    if score_a > score_b:
        return label_a
    return label_b


def make_cross(n):
    """n x n 십자가 패턴을 만든다."""
    mid = n // 2
    return [[1.0 if (r == mid or c == mid) else 0.0 for c in range(n)]
            for r in range(n)]


def make_x(n):
    """n x n X 패턴을 만든다."""
    return [[1.0 if (r == c or r + c == n - 1) else 0.0 for c in range(n)]
            for r in range(n)]


# ---------- 성능 측정 ----------

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


# ---------- 모드 1 ----------

def parse_row(line, n):
    """한 줄을 숫자 n개로 바꾼다. 잘못되면 ValueError를 낸다."""
    tokens = line.split()

    if len(tokens) != n:
        raise ValueError('%d개의 숫자를 공백으로 구분해 입력하세요. (입력된 개수: %d)'
                         % (n, len(tokens)))

    numbers = []
    for tok in tokens:
        try:
            numbers.append(float(tok))
        except ValueError:
            raise ValueError("'%s' 은(는) 숫자가 아닙니다." % tok)
    return numbers


def read_matrix(name, n=SIZE_MODE1):
    """n x n 배열을 한 줄씩 입력받는다. 틀린 줄만 다시 물어본다."""
    print('\n[%s] 한 줄에 %d개씩, 공백으로 구분해 입력하세요.' % (name, n))

    rows = []
    while len(rows) < n:
        try:
            line = input('  %d행 > ' % (len(rows) + 1))
        except (EOFError, KeyboardInterrupt):
            raise SystemExit('\n입력이 중단되었습니다. 프로그램을 종료합니다.')

        if not line.strip():
            print('  ! 빈 줄입니다. 숫자 %d개를 입력하세요.' % n)
            continue

        try:
            rows.append(parse_row(line, n))
        except ValueError as err:
            print('  ! 입력 형식 오류: %s 다시 입력하세요.' % err)
    return rows


def show_matrix(name, matrix):
    """저장된 배열을 확인용으로 출력한다."""
    print('[%s] 저장 완료' % name)
    for row in matrix:
        print('   ', ' '.join('%g' % v for v in row))


def run_mode1():
    """모드 1: 콘솔 입력 → MAC → 판정 → 성능 분석."""
    print('\n=== 모드 1: 사용자 입력 (%dx%d) ===' % (SIZE_MODE1, SIZE_MODE1))

    filter_a = read_matrix('필터 A')
    show_matrix('필터 A', filter_a)

    filter_b = read_matrix('필터 B')
    show_matrix('필터 B', filter_b)

    pattern = read_matrix('패턴')
    show_matrix('패턴', pattern)

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    verdict = judge(score_a, score_b, 'A', 'B')

    print('\n[결과]')
    print('  필터 A 점수 : %.4f' % score_a)
    print('  필터 B 점수 : %.4f' % score_b)
    if verdict == 'UNDECIDED':
        print('  판정        : 판정 불가 (동점)')
    else:
        print('  판정        : %s' % verdict)

    print_performance([SIZE_MODE1])


# ---------- 모드 2 ----------

def size_from_key(key):
    """'size_5_1' 에서 5를 뽑는다."""
    parts = key.split('_')
    return int(parts[1])


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


def fail_reason(verdict, expected, score_cross, score_x):
    """FAIL 사유를 종류별로 분류해 문구로 만든다."""
    if verdict == 'UNDECIDED':
        return ('동점(Cross %.4f = X %.4f) - 두 필터의 값 크기(scale)가 달라 '
                '모양 유사도가 아닌 필터 값 크기가 점수를 지배함 [데이터 문제]'
                % (score_cross, score_x))
    return ('판정 %s, 기대 %s (Cross %.4f / X %.4f) [판정 로직 확인 필요]'
            % (verdict, expected, score_cross, score_x))


def check_case(key, item, filters):
    """한 케이스를 검증한다. 문제가 있으면 ValueError를 낸다."""
    n = size_from_key(key)

    filter_key = 'size_%d' % n
    if filter_key not in filters:
        raise ValueError('%s 필터가 없습니다' % filter_key)

    grid = item['input']
    if len(grid) != n:
        raise ValueError('키는 %d를 가리키는데 실제 배열은 %d행' % (n, len(grid)))

    normalized = normalize_filters(filters[filter_key])
    cross_filter = normalized['Cross']
    x_filter = normalized['X']

    if len(cross_filter) != n or len(x_filter) != n:
        raise ValueError('필터 크기가 %d가 아닙니다' % n)

    expected = normalize_label(item.get('expected'))
    if expected is None:
        raise ValueError('알 수 없는 expected 값: %r' % item.get('expected'))

    score_cross = mac(grid, cross_filter)
    score_x = mac(grid, x_filter)
    return score_cross, score_x, judge(score_cross, score_x, 'Cross', 'X'), expected


def run_mode2():
    """모드 2: data.json 로드 → 케이스별 판정/채점 → 성능 분석 → 요약."""
    print('\n=== 모드 2: %s 분석 ===' % DATA_FILE)

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print('%s 파일을 찾을 수 없습니다. main.py와 같은 폴더에 두세요.' % DATA_FILE)
        return
    except json.JSONDecodeError as err:
        print('%s 파일이 올바른 JSON이 아닙니다: %s' % (DATA_FILE, err))
        return

    filters = data.get('filters', {})
    patterns = data.get('patterns', {})

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
            failures.append((key, '%s [스키마 문제]' % err))
            print('%-12s %10s %10s %-10s %-8s %s'
                  % (key, '-', '-', '-', '-', 'FAIL'))
            continue

        if verdict == expected:
            pass_count = pass_count + 1
            result = 'PASS'
        else:
            failures.append((key, fail_reason(verdict, expected, score_cross, score_x)))
            result = 'FAIL'

        print('%-12s %10.4f %10.4f %-10s %-8s %s'
              % (key, score_cross, score_x, verdict, expected, result))

    print('-' * 64)

    print_performance([3, 5, 13, 25])

    print('\n[결과 요약]')
    print('  전체 %d개 / 통과 %d개 / 실패 %d개'
          % (total_count, pass_count, total_count - pass_count))

    if failures:
        print('\n[실패 케이스]')
        for key, reason in failures:
            print('  %-12s %s' % (key, reason))


# ---------- 메뉴 ----------

def main():
    while True:
        print('\n=== Mini NPU 시뮬레이터 ===')
        print('  1) 사용자 입력 (3x3)')
        print('  2) %s 분석' % DATA_FILE)
        print('  0) 종료')

        try:
            choice = input('선택 > ').strip()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit('\n프로그램을 종료합니다.')

        if choice == '0':
            print('프로그램을 종료합니다.')
            return
        elif choice == '1':
            run_mode1()
        elif choice == '2':
            run_mode2()
        else:
            print('  ! 0, 1, 2 중에서 입력하세요.')


main()