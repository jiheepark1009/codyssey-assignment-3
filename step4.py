import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('최상위 키:', list(data.keys()))

filters = data['filters']
patterns = data['patterns']

print()
print('=== 필터 %d개 ===' % len(filters))
for key in filters:
    inner = filters[key]
    print('  %-10s 안에 든 키: %s' % (key, list(inner.keys())))

print()
print('=== 패턴 %d개 ===' % len(patterns))
for key in patterns:
    item = patterns[key]
    grid = item['input']
    print('  %-12s 크기 %dx%d   expected = %r'
          % (key, len(grid), len(grid[0]), item['expected']))

print()
print('=== size_5 의 cross 필터 내용 ===')
for row in filters['size_5']['cross']:
    print('   ', row)

print()
print('=== size_5_1 패턴 내용 ===')
for row in patterns['size_5_1']['input']:
    print('   ', row)
print('  이 패턴의 정답(expected):', repr(patterns['size_5_1']['expected']))