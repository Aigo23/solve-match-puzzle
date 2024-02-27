#问题求解
numstr = ['1110111', '0010010', '1011101', '1011011', '0111010',
          '1101011', '1101111', '1010010', '1111111', '1111011']
oper = ['+', '-', '*']

def opdis(op1, op2):
    opdismatrix = [[[0, 0], [1, 0], [0, 2]],
                   [[-1, 0], [0, 0], [-1, 1]],
                   [[0, 2], [1, 1], [0, 0]]]
    return opdismatrix[oper.index(op1)][oper.index(op2)]
def dis(num1, num2):
    dis1 = count1 = count2 = 0
    for i in range(7):
        if numstr[num1][i] == '1' and numstr[num2][i] == '0':
            dis1 += 1; count1 += 1
        elif numstr[num1][i] == '0' and numstr[num2][i] == '1':
            dis1 -= 1; count2 += 1
    return [dis1, min(count1, count2)]
def judge(num):
    num1 = 10 * num[0] + num[1]
    num2 = 10 * num[2] + num[3]
    num3 = 10 * num[4] + num[5]
    if num[6] == '+' and num1 + num2 == num3: return True
    if num[6] == '-' and num1 - num2 == num3: return True
    if num[6] == '*' and num1 * num2 == num3: return True
    return False

def SolveProblem(step, str):

    numdismatrix = []
    for i in range(10):
        for j in range (10):
            numdismatrix.append(dis(i,j))
    origin = [ord(str[0]) - ord('0'), ord(str[1]) - ord('0'), ord(str[3]) - ord('0'),
              ord(str[4]) - ord('0'), ord(str[6]) - ord('0'), ord(str[7]) - ord('0'),
              str[2], 0, 0]
    list1 = [origin]
    list2 = []
    result = []

    for i in range(6):
        while len(list1) != 0:
            if abs(list1[0][7]) + list1[0][8] > step:
                list1.pop(0); continue
            for j in range(10):
                temp = list1[0].copy()
                temp[i] = j
                distant = numdismatrix[10 * list1[0][i] + j]
                temp[8] += min(abs(temp[7]), abs(distant[0])) + distant[1]
                temp[7] += distant[0]
                list2.append(temp)
                if list2[-1][7] == 0 and list2[-1][8] == step:
                    if judge(list2[-1]):
                        result.append(list2[-1])
            list1.pop(0)
        list1.extend(list2)
        list2.clear()


    while len(list1) != 0:
        if abs(list1[0][7]) + list1[0][8] > step:
            list1.pop(0)
            continue
        for j in range(3):
            temp = list1[0].copy()
            temp[6] = oper[j]
            distant = opdis(list1[0][6], temp[6])

            temp[8] += min(abs(temp[7]), abs(distant[0])) + distant[1]
            temp[7] += distant[0]
            list2.append(temp)
            if list2[-1][7] == 0 and list2[-1][8] == step:
                if judge(list2[-1]):
                    result.append(list2[-1])
        list1.pop(0)
    list1 = list2.copy()
    list2.clear()
    for el in range(len(result) - 1, -1, -1):
        if result.count(result[el]) > 1:
            result.remove(result[el])

    return result