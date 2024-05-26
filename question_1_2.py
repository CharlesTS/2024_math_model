import os
import pandas as pd
import generate_electricity
import battery_system


def main():
    file_name_1 = ['问题1：（1）A.csv', '问题1：（1）B.csv', '问题1：（1）C.csv']
    file_name_2 = ['问题1：（2）A.csv', '问题1：（2）B.csv', '问题1：（2）C.csv']
    name = ['A', 'B', 'C']

    for file in range(len(file_name_1)):
        # 检查并删除已有的结果文件
        if os.path.exists(file_name_2[file]):
            os.remove(file_name_2[file])

        # 创建并初始化结果文件
        with open(file_name_2[file], 'a', encoding='utf-8') as f:
            f.write('目标功率,风电购电量,光伏购电量,电网购电量,弃风弃光电量\n')

        data = pd.read_csv(file_name_1[file])
        data = data.dropna()

        # 目标功率
        data_target = data['目标功率'].tolist()

        # 风力发电发电量
        data_win = data['风电购电量'].tolist()

        # 光伏发电量
        data_light = data['光伏购电量'].tolist()

        # 弃光电量
        e_abandon_light = data['弃光电量'].tolist()

        # 弃风电量
        e_abandon_wind = data['弃风电量'].tolist()

        # 电网购电量
        e_buy = data['电网购电量'].tolist()

        # 初始化电池对象
        contain = 100  # 电池容量：100kWh
        p = 50  # 电池充放电功率：50kW
        battery = battery_system.BatterySystem(contain, p)

        # 初始化一个弃电量和电网购电量的列表
        e_abandon_buy = []

        # 初始化一个电池电量的列表
        battery_capacity = []

        for i in range(len(e_abandon_wind)):
            abandon_light = e_abandon_light[i]
            abandon_win = e_abandon_wind[i]
            abandon = abandon_win + abandon_light
            buy = e_buy[i]
            if abandon > 0:
                capacity, temp = battery.battery_charge(abandon)
            elif buy > 0:
                capacity, temp = battery.battery_charge(-buy)
            else:
                # 如果既没有弃电量也没有购电量，电池状态不变
                capacity, temp = battery.current_capacity, 0

            battery_capacity.append(capacity)
            e_abandon_buy.append(temp)

        e_abandon_res = []
        e_buy_res = []

        for value in e_abandon_buy:
            if value > 0:
                e_abandon_res.append(value)
                e_buy_res.append(0)
            elif value < 0:
                e_abandon_res.append(0)
                e_buy_res.append(-value)
            else:
                e_abandon_res.append(0)
                e_buy_res.append(0)

        # 检查列表长度是否一致
        assert len(data_target) == len(e_buy_res) == len(data_light) == len(data_win), \
            "列表长度不一致，无法计算成本"

        # 初始化总成本列表
        cost = []
        for i in range(len(data_target)):
            cost.append(1 * e_buy_res[i] + 0.4 * data_light[i] + 0.5 * data_win[i] + battery.battery_cost())

        cu = sum(cost) / sum(data_target)

        for i in range(len(data_target)):
            generate_electricity.write_file_1(data_target[i], data_win[i], data_light[i], e_buy_res[i],
                                              e_abandon_res[i], file_name_2[file])

        # 打印各园区的总供电成本和单位电量平均供电成本
        print(
            f'{name[file]}园区：电网购电量：{sum(e_buy_res)}, 光伏发电量：{sum(data_light)}, 风电发电量：{sum(data_win)}, 弃电量：{sum(e_abandon_res)}, 总供电成本：{sum(cost)}, 单位电量平均供电成本：{cu}')
        print(f'电池电量:{battery_capacity}')


if __name__ == '__main__':
    main()
