# _*_ coding: utf8 _*_
# @Date     : 2017-04-11 21:27:00
# @Author   : Alan Lau (rlalan@outlook.com)
# @Language : Python3.5
# https://blog.csdn.net/AlanConstantineLau/article/details/70173561
from service import service_logger
from model.LotteryModel import LotteryModel

import numpy as np

#指数平滑公式
def exponential_smoothing(alpha, s):
    s2 = np.zeros(s.shape)
    s2[0] = s[0]
    for i in range(1, len(s2)):
        s2[i] = alpha*s[i]+(1-alpha)*s2[i-1]
    return s2

def get_yuce(phase):
    new = phase+1
    limit = 20
    list = LotteryModel.get_list('period<'+str(new), limit)
    olds = []
    i = limit
    for vo in list:
        olds.append([
            int(vo['period']), i, int(vo['pram1'])
        ])
        i = i - 1

    arrs = olds[::-1]
    print '============================'+str(new)
    # print olds
    print arrs

    alpha = .70                # 设置alphe，即平滑系数
    pre_year = np.array([new]) # 将需要预测的两年存入numpy的array对象里
    data = np.array(arrs)
    year, time_id, number = data.T # 将数据分别赋值给year, time_id, number
    initial_line = np.array([0, 0, number[0]]) # 初始化，由于平滑指数是根据上一期的数值进行预测的，原始数据中的最早数据为1995，没有1994年的数据，这里定义1994年的数据和1995年数据相同
    initial_data = np.insert(data, 0, values=initial_line, axis=0) # 插入初始化数据
    initial_year, initial_time_id, initial_number = initial_data.T # 插入初始化年

    s_single = exponential_smoothing(alpha, initial_number) # 计算一次指数平滑
    s_double = exponential_smoothing(alpha, s_single) # 计算二次平滑字数，二次平滑指数是在一次指数平滑的基础上进行的，三次指数平滑以此类推

    a_double = 2*s_single-s_double # 计算二次指数平滑的a
    b_double = (alpha/(1-alpha))*(s_single-s_double) # 计算二次指数平滑的b
    s_pre_double = np.zeros(s_double.shape) # 建立预测轴
    for i in range(1, len(initial_time_id)):
        s_pre_double[i] = a_double[i-1]+b_double[i-1] # 循环计算每一年的二次指数平滑法的预测值，下面三次指数平滑法原理相同
    pre_next_year = a_double[-1]+b_double[-1]*1 # 预测下一年
    s_pre_double = np.insert(s_pre_double, len(s_pre_double), values=np.array([pre_next_year]), axis=0) # 组合预测值

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
    # print output

    newyear = new_year[0:]
    predouble = s_pre_double[0:]
    pretriple = s_pre_triple[0:]

    k = len(newyear)
    real = str(round(predouble[k],2))+','+str(round(pretriple[k],2))
    if predouble[k]<=4:
        lottery = ['1','2','3','4','5','6']
    elif predouble[k]>=7:
        lottery = ['5','6','7','8','9','10']
    elif predouble[k]>5 and pretriple[k]>4:
        lottery = ['3','4','5','6','7','8']
    else:
        lottery = ['1','2','3','4','5','6','7']

    return [new, real, lottery]
if __name__ == '__main__':

    list = LotteryModel.get_list('period<=718503', 30)
    for vo in list:
        resu = get_yuce(vo['period'])
        print resu
        LotteryModel.update_lottery('period='+str(resu[0]), real=resu[1], yuce=','.join(resu[2]))
        # break
