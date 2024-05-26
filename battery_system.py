# 对象：电池系统
class BatterySystem:
    def __init__(self, contain, p):
        self.battery = contain * 0.1   # 电池电量，设定初始值为电池容量的最小值，即为10%的电池容量
        self.battery_transfer = 0.95   # 电池传输效率
        self.battery_contain = contain  # 电池容量
        self.battery_p = p  # 电池功率
        self.battery_SOC = [0.1, 0.9]   # 电池SOC允许范围
        self.battery_age = 10 * 365 * 24   # 电池寿命：10年，此处单位：小时
        self.battery_p_price = 800  # 功率单价：800元/kW
        self.battery_e_price = 1800 # 能量单价：1800元/kWh

    # 充放电函数
    def battery_charge(self, charge):
        init_battery = self.battery  # 初始电量
        init_charge = charge  # 初始充放电量

        # 判断：如果电池电量在SOC的范围内，开始充放电
        # charge > 0 为充电，charge < 0 为放电
        if self.judge_battery() == 1:
            # 初始充放电量
            charge, judge_power_num = self.judge_power(charge)  # 充进去/放出来的电量，超出额定功率判断标志

            if charge > 0:
                if init_charge > 0:
                    self.battery += init_charge * self.battery_transfer
            else:
                self.battery += charge / self.battery_transfer

        # 充电情况，超出额定值
        # 判断：如果电池电量高于90%，设定电池电量为额定最高容量
        # 返回值：多出的充电电量，返回为弃电量
        if self.judge_battery() == 'up':
            self.battery = self.battery_contain * self.battery_SOC[1]
            return self.battery, init_charge - charge + self.battery_p

        # 放电情况，超出额定值
        # 判断：如果电池的容量低于10%，设定电池电量为额定的最低容量
        # 返回值：少的放电电量，返回为电网购电量（负数）
        if self.judge_battery() == 'down':
            self.battery = self.battery_contain * self.battery_SOC[0]
            return self.battery, init_charge - charge - self.battery_p

        if self.judge_battery() == 1:
            return self.battery, 0

    # 判断电池的容量是否超过额定的SOC
    def judge_battery(self):
        # 如果电池电量大于SOC额定的上限值，即90%的电池容量
        # 返回值 'up'
        if self.battery > self.battery_contain * self.battery_SOC[1]:
            return 'up'

        # 如果电池电量小于SOC额定的下限值 ，即10%的电池容量
        # 返回值 'down'
        elif self.battery < self.battery_contain * self.battery_SOC[0]:
            return 'down'

        # 其他情况，即为电池电量在SOC规定的范围内
        # 返回值 1
        else:
            return 1

    def judge_power(self, charge):
        if charge > self.battery_p:
            return self.battery_p, 1

        elif charge < -self.battery_p:
            return -self.battery_p, 1

        else:
            return charge, 0

    def battery_cost(self):
        return (self.battery_p * 800 + self.battery_contain * 1800) / self.battery_age

    def current_capacity(self):
        return self.battery
