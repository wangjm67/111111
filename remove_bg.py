from PIL import Image
from collections import deque

INPUT = "character.png"
OUTPUT = "character_transparent.png"

img = Image.open(INPUT).convert("RGBA")
w, h = img.size
pixels = img.load()

visited = [[False] * w for _ in range(h)]
queue = deque()

def near_white(r, g, b):
    return r >= 245 and g >= 245 and b >= 245

# 从四条边缘开始寻找背景
for x in range(w):
    queue.append((x, 0))
    queue.append((x, h - 1))

for y in range(h):
    queue.append((0, y))
    queue.append((w - 1, y))

while queue:
    x, y = queue.popleft()

    if x < 0 or x >= w or y < 0 or y >= h:
        continue

    if visited[y][x]:
        continue

    r, g, b, a = pixels[x, y]

    if not near_white(r, g, b):
        continue

    visited[y][x] = True

    # 根据颜色深浅处理边缘透明度
    darkness = 255 - min(r, g, b)
    alpha = min(180, max(0, darkness * 5))
    pixels[x, y] = (r, g, b, alpha)

    queue.append((x + 1, y))
    queue.append((x - 1, y))
    queue.append((x, y + 1))
    queue.append((x, y - 1))

img.save(OUTPUT)
print(f"Generated：{OUTPUT}")
