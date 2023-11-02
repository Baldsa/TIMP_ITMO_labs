#Версия компилятора 3.8.10 64-bit
def decimal_to_ternary(n):    
    summa = 0
    while n > 0:
        remainder = n % 3
        summa += remainder
        n //= 3
    return summa
ans = 0 
for i in range(4096, 65536): #Дипазон был взят такой. Так как меньше число имеющее 4 разряда в 16 СС это 1000, а максимальное FFFF. 
    if (i % 4 == 0 and i % 3 != 0):
        result = decimal_to_ternary(i)
        if result == 8:
            print(i)
            ans += i
print(ans)