pattern = [[0, 1, 0],
           [1, 1, 1],
           [0, 1, 0]]

cross_filter = [[0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]]

total = 0

for r in range(3):
    for c in range(3):
        product = pattern[r][c] * cross_filter[r][c]
        total = total + product
        print('%d행 %d열:  %d x %d = %d   (누적 %d)'
              % (r, c, pattern[r][c], cross_filter[r][c], product, total))

print()
print('최종 점수:', total)