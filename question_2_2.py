import pandas as pd
import battery_system
from sko.PSO import PSO

def battery_cost(x):
    p, contain = x
    data = pd.read_csv('问题2：（1）.csv')
    data = data.dropna()

    # 目标功率
    data_target = data['目标功率'].tolist()

    # 风力发电发电量
    data_win = data['风电购电量'].tolist()

    # 光伏发电量
    data_light = data['光伏购电量'].tolist()

    # 弃风弃电量
    e_abandon_win = data['弃风电量'].tolist()
    e_abandon_light = data['弃光电量'].tolist()
    e_abandon = []
    for i, j in zip(e_abandon_light, e_abandon_win):
        e_abandon.append(i + j)

    # 电网购电量
    e_buy = data['电网购电量'].tolist()

    battery = battery_system.BatterySystem(contain, p)

    # 初始化一个弃电量和电网购电量的列表
    e_abandon_buy = []

    # 初始化一个电池电量的列表
    battery_capacity = []

    for i in range(len(e_abandon)):
        abandon = e_abandon[i]
        buy = e_buy[i]
        if abandon > 0:
            capacity, temp = battery.battery_charge(abandon)
            battery_capacity.append(capacity)
            e_abandon_buy.append(temp)
        elif buy > 0:
            capacity, temp = battery.battery_charge(0 - buy)
            battery_capacity.append(capacity)
            e_abandon_buy.append(temp)
        else:
            # 如果既没有弃电量也没有购电量，电池状态不变
            battery_capacity.append(battery.current_capacity)
            e_abandon_buy.append(0)

    e_abandon_res = []
    e_buy_res = []

    for value in e_abandon_buy:
        # 列表为正数的时候，为弃电量
        if value > 0:
            e_abandon_res.append(value)
            e_buy_res.append(0)
        elif value < 0:
            e_abandon_res.append(0)
            e_buy_res.append(0 - value)
        else:
            e_abandon_res.append(0)
            e_buy_res.append(0)

    # 初始化总成本列表
    total_cost = 0
    for i in range(len(data_target)):
        total_cost += (1 * e_buy_res[i] + 0.4 * data_light[i] + 0.5 * data_win[i] + battery.battery_cost())

    return total_cost

def main():
    # PSO粒子群优化，优化储能系统的功率和容量配置
    # 调整PSO的参数，以增强粒子的探索能力
    pso = PSO(func=battery_cost, dim=2, pop=100, max_iter=200, lb=[0, 0], ub=[100, 1000], w=0.9, c1=0.8, c2=0.8)
    pso.run()
    print('best_x is ', pso.gbest_x, 'best_y is', pso.gbest_y)

    # # 遗传算法，优化储能系统的功率和容量配置
    # # 调整GA的参数，以增强种群的多样性
    # ga = GA(func=battery_cost, n_dim=2, size_pop=100, max_iter=200, lb=[0, 0], ub=[100, 1000], precision=1e-7)
    #
    # best_x, best_y = ga.run()
    #
    # print('best_x is ', best_x, 'best_y is', best_y)

if __name__ == '__main__':
    main()
