x = input("Enter a password: ")
newx = [int(digit) for digit in x]
e = 0
f = 0
evnum = []
for i in range(len(newx)):
    if newx[i] > e:
        e = newx[i]
for i in range(len(newx)):
    if newx[i] < f:
        f = newx[i]
for i in range(len(newx)):
    if newx[i] % 2 == 0:
        evnum.append(newx[i])



if int(x) >= 100 and int(x) % 5 != 0 and newx[0] + newx[1] + newx[2] >= 12:
    if e >= 2 * f and f != 0 and len(evnum) >= 2:
        print("Password accepted.")
else:
    print("Password rejected.")