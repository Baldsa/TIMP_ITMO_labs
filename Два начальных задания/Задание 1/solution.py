f = open("27_B.txt", "r")
K = int(f.readline())
N = int(f.readline())
heights = [int(f.readline()) for _ in range(N)]
s = [0] * N # Массив префиксных сумм 
for i in range(N):
    s[i] = s[i - 1] + heights[i] # Заполнение массива префексных сумм. [1, 2, 3, 4, 5] => [1, 3, 6, 10, 15]
mxB = -10**20 # Макс значение
m = 10**20 # Минимальное значение
for i in range(K + 1, N):
    m = min(m, s[i - (K + 1)])
    mxB = max(mxB, s[i], s[i] - m)
print(mxB)