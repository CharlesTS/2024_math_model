# 绘制各园区弃风弃光电量与时间的关系图
from matplotlib.ticker import MultipleLocator
from matplotlib import pyplot as plt
import pandas as pd

def draw_pic(y1, y2, y3, file_name):
    """

    :param y1:
    :param y2:
    :param y3:
    :return:
    """
    plt.figure(figsize=(7, 3), dpi=800)
    ax = plt.subplot(111)

    data_wind = pd.read_excel('timeline.xlsx').dropna()
    time = data_wind['时间']

    # 重新格式化时间数据，每隔4个点取一个时间值
    time_new = [time[i] for i in range(0, len(time), 4)]
    time_new.append('24:00:00')

    # 准备x轴的数据点，每隔4个点取一个索引值
    data_new = list(range(0, 24, 4))
    data_new.append(24)

    # 设置中文字体支持
    plt.rcParams['font.sans-serif'] = ['SimHei']

    # 绘制三条弃电量曲线，分别用红色、蓝色和绿色表示
    plt.plot(y1, 'r-', label='A园区')
    plt.plot(y2, 'b-', label='B园区')
    plt.plot(y3, 'g-', label='C园区')

    # 设置图表标题和轴标签
    plt.title('各园区弃风弃光电量与时间的关系')
    plt.xlabel('时间')
    plt.ylabel('弃风弃光电量')

    # 显示图例
    plt.legend()

    # 添加网格线
    plt.grid()

    # 自动调整子图参数以适应图形区域
    plt.tight_layout()

    # 设置x轴的主刻度间隔为4
    xmajorLocator = MultipleLocator(4)
    ax.xaxis.set_major_locator(xmajorLocator)

    # 设置x轴的标签
    plt.xticks(data_new, time_new)

    # 保存图像为文件
    plt.savefig(file_name)

    # 显示图像
    plt.show()