# 风力发电电量
def win_generate_electricity(data_win):
    return data_win * 1   # 每个小时风电发电电量，单位：KWh

# 光伏发电电量
def light_generate_electricity(data_light):
    return data_light * 1   # 每个小时光伏发电电量，单位：KWh

# 电网购电量
def power_grid_buy(pnd, pspw, pspl):
    """

    :param pnd: 园区系统需求电量
    :param pspw: 风电发电电量
    :param pspl: 光伏发电电量
    :return: 电网购电电量
    """
    if judge(pnd, pspw, pspl):
        return (pnd - pspw - pspl) * 1    # 单位：KWh
    else:
        return 0

def abandon_win_light(pnd, pspw, pspl):
    """

    :param pnd: 园区系统需求电量
    :param pspw: 风电发电电量
    :param pspl: 光伏发电电量
    :return: 弃风弃光电量
    """
    if judge(pnd, pspw, pspl) == 0:
        # 如果光伏发电量减去园区系统需求电量大于0
        if pspl - pnd > 0:
            # 返回值：光伏弃电量，风电弃电量
            return pspl - pnd, pspw
        # 如果光伏发电量减去园区系统需求电量小于0
        else:
            # 返回值：光伏弃电量，风电弃电量
            return 0, pspw + pspl - pnd
    else:
        return 0, 0

def judge(pnd, pspw, pspl):
    """

    :param pnd: 园区系统需求电量
    :param pspw: 风电发电电量
    :param pspl: 光伏发电电量
    :return:
    """
    if pnd > (pspw + pspl):
        return 1
    else:
        return 0

# 未配置储能系统
# 计算系统总成本以及购电量
def no_battery_system_cost(data, data_light, data_win,):
    """
    计算系统总成本以及各类购电量和弃风弃光电量

    :param data: 目标购电量数据
    :param data_light: 光伏发电数据
    :param data_win: 风电发电数据
    :return: 总成本, 电网购电量, 弃风弃光电量, 光伏购电量, 风电购电量
    """
    cost = []   # 总成本列表
    e_light = []    # 光伏购电量列表
    e_win = []  # 风电购电量列表
    e_buy = []  # 电网购电量列表
    e_abandon_win = []  # 弃风电量列表
    e_abandon_light = []    # 弃光电量列表
    for i in range(len(data)):
        pnd = data[i]
        if data_light:
            pspl = light_generate_electricity(data_light[i])
        else:
            pspl = 0
        if data_win:
            pspw = win_generate_electricity(data_win[i])
        else:
            pspw = 0
        pbuy = power_grid_buy(pnd, pspw, pspl)

        # 计算总成本（假设电网电价1元/kWh，光伏电价0.4元/kWh，风电电价0.5元/kWh）
        e_light.append(pspl)
        e_win.append(pspw)
        e_buy.append(pbuy)
        e_light_temp, e_win_temp = abandon_win_light(pnd, pspw, pspl)
        e_abandon_light.append(e_light_temp)
        e_abandon_win.append(e_win_temp)
    for i in range(len(e_abandon_light)):
        cost.append(1 * e_buy[i] + 0.4 * (e_light[i] - e_abandon_light[i]) + 0.5 * (e_win[i] - e_abandon_win[i]))

    return cost, e_buy, e_abandon_light, e_abandon_win, e_light, e_win

# 追加写入CSV文件
def write_file(data, e_win, e_light, e_buy, e_abandon_light, e_abandon_win, file_name):
    """
    将数据追加写入CSV文件

    :param data: 目标功率
    :param e_win: 风电购电量
    :param e_light: 光伏购电量
    :param e_buy: 电网购电量
    :param e_abandon: 弃风弃光电量
    :param file_name: 文件名
    """
    with open(file_name, 'a', encoding='utf-8') as f:
        data, e_buy, e_abandon_light, e_abandon_win, e_light, e_win = round(data, 3), round(e_buy, 3), round(e_abandon_light, 3),  round(e_abandon_win, 3),round(e_light, 3), round(e_win, 3)
        data, e_buy, e_abandon_light, e_abandon_win, e_light, e_win = str(data), str(e_buy), str(e_abandon_light),  str(e_abandon_win),str(e_light), str(e_win)
        f.write(f'{data},{e_win},{e_light},{e_buy},{e_abandon_light},{e_abandon_win}\n')
        f.close()
