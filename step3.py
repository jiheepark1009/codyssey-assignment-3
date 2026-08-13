SIZE = 3


def mac(pattern, filt):
    """패턴과 필터를 같은 위치끼리 곱해서 전부 더한다."""
    total = 0
    for r in range(SIZE):
        for c in range(SIZE):
            total = total + pattern[r][c] * filt[r][c]
    return total


def judge(score_a, score_b, label_a, label_b):
    """점수가 높은 쪽 라벨을 돌려준다. 같으면 UNDECIDED."""
    if score_a > score_b:
        return label_a
    elif score_b > score_a:
        return label_b
    else:
        return 'UNDECIDED'


def parse_row(line):
    """한 줄을 숫자 SIZE개로 바꾼다. 잘못되면 ValueError를 낸다."""
    tokens = line.split()

    if len(tokens) != SIZE:
        raise ValueError('%d개의 숫자를 공백으로 구분해 입력하세요. (입력된 개수: %d)'
                         % (SIZE, len(tokens)))

    numbers = []
    for tok in tokens:
        try:
            numbers.append(float(tok))
        except ValueError:
            raise ValueError("'%s' 은(는) 숫자가 아닙니다." % tok)
    return numbers

def read_matrix(name):
    """SIZE x SIZE 배열을 한 줄씩 입력받는다. 틀린 줄만 다시 물어본다."""
    print('\n[%s] 한 줄에 %d개씩, 공백으로 구분해 입력하세요.' % (name, SIZE))

    rows = []
    while len(rows) < SIZE:
        try:
            line = input('  %d행 > ' % (len(rows) + 1))
        except (EOFError, KeyboardInterrupt):
            raise SystemExit('\n입력이 중단되었습니다. 프로그램을 종료합니다.')

        if not line.strip():
            print('  ! 빈 줄입니다. 숫자 %d개를 입력하세요.' % SIZE)
            continue

        try:
            rows.append(parse_row(line))
        except ValueError as err:
            print('  ! 입력 형식 오류: %s 다시 입력하세요.' % err)
    return rows


def show_matrix(name, matrix):
    print('[%s] 저장 완료' % name)
    for row in matrix:
        print('   ', ' '.join('%g' % v for v in row))


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
print('  필터 A 점수 :', score_a)
print('  필터 B 점수 :', score_b)
print('  판정        :', verdict)