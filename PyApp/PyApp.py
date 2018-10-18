"""
数字numpy, 绘图, 机器学习sklearn
ctrl回车只执行不换行, shift回车执行换行, alt回车在执行, 当前语句下空行

py没有{}, 靠缩进
2-3人一组, 内容不能相同
允许开源拼凑
"""
# 这是一个注释
import numpy as np
import matplotlib as matpl
import matplotlib.pyplot as plt
import sklearn
import scipy as sp
# import ClassifierComparison
# import NumberGuess

# 此环境下貌似用不了这个(不需要用这个绘图)
# %matplotlib inline

a=1;
b=2;
if(a>b):
    print('a>b');
else:
    print('b>a');
    
for i in [0,1,2,3]:
    print(i);


"""
#内嵌画图
%matplotlib inline
import matplotlib # 注意这个也要import一次
import matplotlib.pyplot as plt
myfont = matplotlib.font_manager.FontProperties(fname=r'C:/Windows/Fonts/msyh.ttf') # 这一行
plt.plot((1,2,3),(4,3,-1))
plt.xlabel(u'横坐标',  fontproperties=myfont) # 这一段
plt.ylabel(u'纵坐标',  fontproperties=myfont) # 这一段
#plt.show() # 有了%matplotlib inline 就可以省掉plt.show()了

"""

from sklearn.datasets.samples_generator import make_blobs

centers=[[-2, 2], [2, 2], [0, 4]];
c=np.array(centers);
# cluster_std 方差 ? 越大数据越混乱
X,Y=make_blobs(n_samples=100,centers=centers,random_state=0,cluster_std=0.6);
size = 100;
plt.scatter(X[:,0], X[:,1], c=Y, s=size, cmap='cool');
#所有行的第一列, 第二列, maker是绘图符号 大小写敏感
plt.scatter(c[:,0], c[:,1], s=size, marker='d',c='orange');
plt.show();

