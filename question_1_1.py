import generate_electricity
import pandas as pd
import os
import draw_pic

# 主函数
def main():
    data = pd.read_excel('附件2.xlsx')
    data = data.dropna()  # 删除缺失值
    data_1 = pd.read_excel('附件1.xlsx')
    data_1 = data_1.dropna()  # 删除缺失值

    # 每个小时每个园区的负荷功率
    data_A, data_B, data_C = [], [], []
    for i in data_1['园区A负荷(kW)']:
        data_A.append(i)
    for i in data_1['园区B负荷(kW)']:
        data_B.append(i)
    for i in data_1['园区C负荷(kW)']:
        data_C.append(i)

    # 将每小时风电光伏发电功率导入列表
    data_light_A, data_win_B, data_light_C, data_win_C = [], [], [], []
    for i in data['Lsp_A(Kw)']:
        data_light_A.append(i)
    for i in data['Wsp_B(Kw)']:
        data_win_B.append(i)
    for i in data['Lsp_C(Kw)']:
        data_light_C.append(i)
    for i in data['Wsp_C(Kw)']:
        data_win_C.append(i)

    # 各个园区的数据计算
    # 总成本， 电网购电量， 弃电量， 光伏发电量， 风电发电量
    cost_A, e_buy_A, e_abandon_A, e_light_A, e_win_A = generate_electricity.no_battery_system_cost(data_A, data_light_A, 0)
    cost_B, e_buy_B, e_abandon_B, e_light_B, e_win_B = generate_electricity.no_battery_system_cost(data_B, 0, data_win_B)
    cost_C, e_buy_C, e_abandon_C, e_light_C, e_win_C = generate_electricity.no_battery_system_cost(data_C, data_light_C, data_win_C)

    # 总购电成本计算
    cost_A = sum(cost_A)
    cost_B = sum(cost_B)
    cost_C = sum(cost_C)

    # 单位购电成本计算
    cu_A = cost_A / sum(data_A)
    cu_B = cost_B / sum(data_B)
    cu_C = cost_C / sum(data_C)

    file_name = ['问题1：（1）A.csv', '问题1：（1）B.csv', '问题1：（1）C.csv']
    for i in file_name:
        # 检查并删除已有的结果文件
        if os.path.exists(i):
            os.remove(i)

        # 创建并初始化结果文件
        f = open(i, 'a', encoding='utf-8')
        f.write('目标功率,风电购电量,光伏购电量,电网购电量,弃风弃光电量\n')
        f.close()

    # 逐行写入各园区的数据
    for i in range(len(data_A)):
        generate_electricity.write_file(data_A[i], e_win_A[i], e_light_A[i], e_buy_A[i], e_abandon_A[i], file_name[0])

    for i in range(len(data_B)):
        generate_electricity.write_file(data_B[i], e_win_B[i], e_light_B[i], e_buy_B[i], e_abandon_B[i], file_name[1])

    for i in range(len(data_C)):
        generate_electricity.write_file(data_C[i], e_win_C[i], e_light_C[i], e_buy_C[i], e_abandon_C[i], file_name[2])

    # 打印各园区的总供电成本和单位电量平均供电成本
    print(f'A园区：电网购电量：{sum(e_buy_A)}, 光伏发电量：{sum(e_light_A)}, 风电发电量：{sum(e_win_A)}, 弃电量：{sum(e_abandon_A)}, 总供电成本：{cost_A}, 单位电量平均供电成本：{cu_A}')
    print(f'B园区：电网购电量：{sum(e_buy_B)}, 光伏发电量：{sum(e_light_B)}, 风电发电量：{sum(e_win_B)}, 弃电量：{sum(e_abandon_B)}, 总供电成本：{cost_B}, 单位电量平均供电成本：{cu_B}')
    print(f'C园区：电网购电量：{sum(e_buy_C)}, 光伏发电量：{sum(e_light_C)}, 风电发电量：{sum(e_win_C)}, 弃电量：{sum(e_abandon_C)}, 总供电成本：{cost_C}, 单位电量平均供电成本：{cu_C}')

    # 绘制折线图
    draw_pic.draw_pic(e_abandon_A, e_abandon_B, e_abandon_C, '各园区弃风弃光电量与时间的关系-问题1-1.png')

if __name__ == '__main__':
    main()
