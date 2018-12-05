# -*- coding: utf-8 -*-
# @Date     : 2017-04-11 21:27:00
# @Author   : Alan Lau (rlalan@outlook.com)
# @Language : Python3.5
# https://blog.csdn.net/AlanConstantineLau/article/details/70173561

import numpy as np

#指数平滑公式
def exponential_smoothing(alpha, s):
    s2 = np.zeros(s.shape)
    s2[0] = s[0]
    for i in range(1, len(s2)):
        s2[i] = alpha*s[i]+(1-alpha)*s2[i-1]
    return s2


def main():
    # 设置alphe，即平滑系数
    alpha = .70
    # pre_year = np.array([2016, 2017])
    # data_path = 'data1.txt'  # 设置数据路径
    pre_year = np.array([718324])#将需要预测的两年存入numpy的array对象里
    # data_path = 'data2.txt'  # 设置数据路径
    # data = np.loadtxt(data_path)#用numpy读取数据
    data = np.array([[718305,1,1],[718306,2,8],[718307,3,9],[718308,4,5],[718309,5,1],[718310,6,3],[718311,7,3],[718312,8,9],[718313,9,4],[718314,10,6],[718315,11,9],[718316,12,2],[718317,13,5],[718318,14,4],[718319,15,3],[718320,16,5],[718321,17,3],[718322,18,9],[718323,19,6]])
    year, time_id, number = data.T#将数据分别赋值给year, time_id, number
    print year
    print time_id
    print number
    initial_line = np.array([0, 0, number[0]])#初始化，由于平滑指数是根据上一期的数值进行预测的，原始数据中的最早数据为1995，没有1994年的数据，这里定义1994年的数据和1995年数据相同
    initial_data = np.insert(data, 0, values=initial_line, axis=0)#插入初始化数据
    initial_year, initial_time_id, initial_number = initial_data.T#插入初始化年

    s_single = exponential_smoothing(alpha, initial_number)#计算一次指数平滑
    s_double = exponential_smoothing(alpha, s_single)#计算二次平滑字数，二次平滑指数是在一次指数平滑的基础上进行的，三次指数平滑以此类推

    a_double = 2*s_single-s_double#计算二次指数平滑的a
    b_double = (alpha/(1-alpha))*(s_single-s_double)#计算二次指数平滑的b
    s_pre_double = np.zeros(s_double.shape)#建立预测轴
    for i in range(1, len(initial_time_id)):
        s_pre_double[i] = a_double[i-1]+b_double[i-1]#循环计算每一年的二次指数平滑法的预测值，下面三次指数平滑法原理相同
    pre_next_year = a_double[-1]+b_double[-1]*1#预测下一年
    s_pre_double = np.insert(s_pre_double, len(s_pre_double), values=np.array([pre_next_year]), axis=0)#组合预测值

    s_triple = exponential_smoothing(alpha, s_double)

    a_triple = 3*s_single-3*s_double+s_triple
    b_triple = (alpha/(2*((1-alpha)**2)))*((6-5*alpha)*s_single -2*((5-4*alpha)*s_double)+(4-3*alpha)*s_triple)
    c_triple = ((alpha**2)/(2*((1-alpha)**2)))*(s_single-2*s_double+s_triple)

    s_pre_triple = np.zeros(s_triple.shape)

    for i in range(1, len(initial_time_id)):
        s_pre_triple[i] = a_triple[i-1]+b_triple[i-1]*1 + c_triple[i-1]*(1**2)

    pre_next_year = a_triple[-1]+b_triple[-1]*1 + c_triple[-1]*(1**2)
    s_pre_triple = np.insert(s_pre_triple, len(s_pre_triple), values=np.array([pre_next_year]), axis=0)

    new_year = np.insert(year, len(year), values=pre_year, axis=0)
    output = np.array([new_year, s_pre_double, s_pre_triple])
    print(output)

    newyear = new_year[0:]
    predouble = s_pre_double[0:]
    pretriple = s_pre_triple[0:]
    print len(newyear)
    print len(predouble)
    print len(predouble)

    items = []
    items.append(['#开奖期数#','#开奖号码#','#预测值#','#预测号码#','#是否中#'])
    k = 0
    for v in newyear:
        open = '9'
        if k < len(number):
             open = str(number[k])

        # print [k,v]
        # print [str(v), str(open), '--', '--', '--']

        if k>3:
            real = str(round(predouble[k],2))+'#'+str(round(pretriple[k],2))
            lottery = []
            if s_pre_double[k]<=4:
                lottery = ['1','2','3','4','5']
            elif s_pre_double[k]>=6:
                lottery = ['5','6','7','8','9','10']
            else:
                lottery = ['2','3','4','5','6','7']

            if open in lottery:
                resu = '中'
            else:
                resu = '否'
            # print [open, lottery]
            # print '-'.join(lottery)
            items.append([str(v), str(open), real, '_'.join(lottery), resu])
        else:
            items.append([str(v), str(open), '--', '--', '--'])
        k = k+1

    print items
    for vo in items:
        print '   '.join(vo)



if __name__ == '__main__':
    main()
