# _*_ coding: utf8 _*_
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

import sys
import time
import random

reload(sys)
sys.setdefaultencoding('utf-8')

# 算法说明
# https://www.cnblogs.com/hhh5460/p/6713287.html

# 投点次数
n = 1000000

# 圆的信息
r = 1.0         # 半径
a, b = (0., 0.) # 圆心

# 正方形区域边界
x_min, x_max = a-r, a+r
y_min, y_max = b-r, b+r

# 在正方形区域内随机投点
x = np.random.uniform(x_min, x_max, n) # 均匀分布
y = np.random.uniform(y_min, y_max, n)

# 计算 点到圆心的距离
d = np.sqrt((x-a)**2 + (y-b)**2)

# 统计 落在圆内的点的数目
res = sum(np.where(d < r, 1, 0))
print res*4
print n

# 计算 pi 的近似值（Monte Carlo方法的精髓：用统计值去近似真实值）
pi = (4 * res) / float(n)

# 公式: 圆内点数/总点数 = 圆面积/正方形面积
# res/n = (pi * r*r)/(4*r*r)
print pi

# 画个图看看
fig = plt.figure()
axes = fig.add_subplot(111)
axes.plot(x, y,'ro',markersize = 1)
plt.axis('equal') # 防止图像变形

circle = Circle(xy=(a,b), radius=r, alpha=0.5)
axes.add_patch(circle)

plt.show()
