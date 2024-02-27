import solve
import random
#随机生成等式
def randequ():
    while True:
        ran_num1 = random.randrange(0, 100, 1)
        ran_num2 = random.randrange(0, 100, 1)
        op = random.randrange(0, 3, 1)
        if op == 0 and ran_num1 + ran_num2 < 100:
            ran_num3 = ran_num1 + ran_num2
        elif op == 1 and ran_num1 - ran_num2 > 0:
            ran_num3 = ran_num1 - ran_num2
        elif op == 2 and ran_num1 * ran_num2 < 100:
            ran_num3 = ran_num1 * ran_num2
        else:
            continue
        origin = [ran_num1 // 10, ran_num1 % 10, ran_num2 // 10, ran_num2 % 10,
                  ran_num3 // 10, ran_num3 % 10, solve.oper[op], 0, 0]
        break
    return origin
#更改等式
def SetProblem(step):
    origin = randequ()
    list1=[origin]
    list2=[]
    #更改等式
    pos_list = [i for i in range(7)]
    random.shuffle(pos_list)
    find = 0
    for i in pos_list:
        while len(list1) != 0:
            if abs(list1[0][7]) + list1[0][8] > step:
                list1.pop(0);
                continue
            if i == 6:
                op_list = [0, 1, 2]
                random.shuffle(op_list)
                for newop in op_list:
                    temp = list1[0].copy()
                    temp[6] = solve.oper[newop]
                    distant = solve.opdis(list1[0][6], temp[6])
                    temp[8] += min(abs(temp[7]), abs(distant[0])) + distant[1]
                    temp[7] += distant[0]
                    list2.append(temp)
                    if temp[7] == 0 and temp[8] == step:
                        find = 1;
                        break
                if find == 1: break

            else:
                num_list = [j for j in range(10)]
                random.shuffle(num_list)
                for newnum in num_list:
                    temp = list1[0].copy()
                    temp[i] = newnum
                    distant = solve.dis(list1[0][i], temp[i])
                    temp[8] += min(abs(temp[7]), abs(distant[0])) + distant[1]
                    temp[7] += distant[0]
                    list2.append(temp)
                    if temp[7] == 0 and temp[8] == step:
                        find = 1;
                        break
                if find == 1: break
            list1.pop(0)
        if find == 1: break
        list1 = list2.copy()
        list2.clear()
    return list2.pop()