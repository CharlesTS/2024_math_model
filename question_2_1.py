import generate_electricity
import pandas as pd
import os

def main():
    data = pd.read_excel('附件2.xlsx')
    data = data.dropna()  # 删除缺失值
    data_1 = pd.read_excel('附件1.xlsx')
    data_1 = data_1.dropna()  # 删除缺失值

    # 目标功率
    data_target = []
    for a, b, c in zip(data_1['园区A负荷(kW)'], data_1['园区B负荷(kW)'], data_1['园区C负荷(kW)']):
        data_target.append(a + b + c)

    # 风力发电功率（总）
    data_win = []
    for w_b, w_c in zip(data['Wsp_B(Kw)'], data['Wsp_C(Kw)']):
        data_win.append(w_b + w_c)

    # 光伏发电功率（总）
    data_light = []
    for l_a, l_c in zip(data['Lsp_A(Kw)'], data['Lsp_C(Kw)']):
        data_light.append(l_a + l_c)

    # 调用generate_electricity模块中的函数计算成本等指标
    cost, e_buy, e_abandon, e_light, e_win = generate_electricity.no_battery_system_cost(data_target, data_light, data_win)
    cu = sum(cost) / sum(data_target)  # 修改为sum(data_target)而不是sum(data)

    # 检查并删除已有的结果文件
    if os.path.exists('问题2：（1）.csv'):
        os.remove('问题2：（1）.csv')

    # 创建并初始化结果文件
    f = open('问题2：（1）.csv', 'a', encoding='utf-8')
    f.write('目标功率,风电购电量,光伏购电量,电网购电量,弃风弃光电量\n')
    f.close()
    for i in range(len(data_target)):
        generate_electricity.write_file(data_target[i], e_win[i], e_light[i], e_buy[i], e_abandon[i], '问题2：（1）.csv')

    print(f'联合园区：电网购电量：{sum(e_buy)}, 光伏发电量：{sum(e_light)}, 风电发电量：{sum(e_win)}, 弃电量：{sum(e_abandon)}, 总供电成本：{sum(cost)}, 单位电量平均供电成本：{cu}')

if __name__ == '__main__':
    main()
