def mac(pattern, filt):
    """패턴과 필터를 같은 위치끼리 곱해서 전부 더한다."""
    total = 0
    for r in range(3):
        for c in range(3):
            total = total + pattern[r][c] * filt[r][c]
    return total


cross_filter = [[0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]]

x_filter = [[1, 0, 1],
            [0, 1, 0],
            [1, 0, 1]]

pattern = [[0, 1, 0],
           [1, 1, 1],
           [0, 1, 0]]

score_cross = mac(pattern, cross_filter)
score_x = mac(pattern, x_filter)

print('Cross 필터 점수:', score_cross)
print('X 필터 점수    :', score_x)

if score_cross > score_x:
    verdict = 'Cross'
elif score_x > score_cross:
    verdict = 'X'
else:
    verdict = 'UNDECIDED'

print('판정           :', verdict)