def battery_charge(battery_p, battery_contain, pnd, p_light, p_win, c_current):
    """

    :param battery_p: 电池传输功率
    :param battery_contain: 电池容量
    :param pnd: 园区目标负荷
    :param p_light: 光电发电量
    :param p_win: 风电发电量
    :param c_current: 当前电池容量
    :return:
    """
    SOC = [0.1, 0.9]
    down = battery_contain * SOC[0]
    up = battery_contain * SOC[1]
    if p_light + p_win > pnd:
        if p_light + p_win - pnd >= battery_p:
            if c_current > (up - battery_p * 0.95):
                