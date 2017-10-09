# -*- coding:utf-8 -*-

try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import statsmodels.formula.api as smf
except Exception as e:
    print("导入库出错",str(e))


"""
旋翼机评估：
1、给定重量，求解悬停功率
2、给定功率，求解最大起飞重量
3、给定重量，（或有机型，）推荐搭配，电机、桨尺寸，
4、评估效率，悬停时间，最大飞行速度，抗风等级，。。。

基础数据获取：
1、爬虫：爬取网上各电机、电调、螺旋桨厂商，及相应的拉力测试数据。scrapy好好学吧，骚年...
2、测试获取，手动录入旋翼拉力数据。心塞！！！

参考：
http://www.modouwo.com/AMoDouWo/QC.html#result


"""

class xrotor(object):

    def __init__(self,motor,power=0,weight=0,frame=4):
        """
        初始化，获取motor()实例
        给定功率，给定无人机重量，旋翼机体类型
        """
        self._motor = motor
        self.UAV_WEIGHT = weight
        self.POWER_GIVEN = power
        self.FRAME = frame
        # 机臂上反5度
        self.SCALER = np.cos(np.deg2rad(5))

    def uav_data_check(self):
        """
        数据检查
        """
        pass

    def uav_weight_calc(self):
        """
        给定各部件重量，计算无人机总重量
        """
        pass

    def uav_propeller_size(self):
        """
        计算螺旋桨尺寸
        """
        pass

    def uav_rotor_data(self):
        """
        单个旋翼拉力
        单个旋翼功率
        单个旋翼效率
        """
        if self.UAV_WEIGHT:
            # 机臂水平，无上反角，旋翼所需提供拉力
            self.thrust_rotor = self.UAV_WEIGHT / self.FRAME
            # 机臂上反5度，旋翼所需提供拉力增加
            self.thrust_rotor_ita = self.thrust_rotor / self.SCALER

            # 拉力-->功率 多项式
            power_polynome = np.poly1d(self._motor.factors["thrust-power"])

            # 无上反角旋翼功率
            self.power_rotor = power_polynome(self.thrust_rotor)
            # 上反5度 旋翼功率
            self.power_rotor_ita = power_polynome(self.thrust_rotor_ita)

            # 功率-->效率 多项式
            efficiency_polynome = np.poly1d(self._motor.factors["power-efficiency"])

            # 无上反角，旋翼效率
            self.efficiency_rotor = efficiency_polynome(self.power_rotor)
            # 上反5度, 旋翼效率
            self.efficiency_rotor_ita = efficiency_polynome(self.power_rotor_ita)

    def uav_min_power(self):
        """
        给定无人机重量，求解最小所需功率
        """
        self.uav_rotor_data()
        if self.power_rotor:
            # 无上反角
            self.MIN_POWER = self.power_rotor * self.FRAME
            # 上反5度
            self.MIN_POWER_ITA = self.power_rotor_ita * self.FRAME


    def uav_max_weight(self):
        """
        给定无人机功率，求得最大起飞重量
        """
        if self.POWER_GIVEN:
            # 机臂无上反角
            power_rotor = self.POWER_GIVEN / self.FRAME

            thrust_polynome = np.poly1d(self._motor.factors["power-thrust"])
            thrust_rotor = thrust_polynome(power_rotor)

            self.MAX_WEIGHT = thrust_rotor * self.FRAME

            # 机臂上反5度，旋翼的垂向拉力减小
            thrust_rotor_ita = thrust_rotor * self.SCALER
            self.MAX_WEIGHT_ITA = thrust_rotor_ita * self.FRAME
        else:
            self.MAX_WEIGHT_ITA = 0


    def uav_min_diagonal_distance(self):
        """
        求解无人机最小轴距
        """
        pass

    def uav_info(self):
        """
        输出信息
        """
        UAV_DATA = {}

        self.uav_min_power()
        self.uav_max_weight()

        UAV_DATA["frame"] = self.FRAME
        UAV_DATA["weight"] = self.UAV_WEIGHT
        UAV_DATA["motor"] = self._motor.motor
        UAV_DATA["propeller"] = self._motor.propeller
        UAV_DATA["power"] = self.MIN_POWER
        UAV_DATA["power_rotor"] = self.power_rotor
        UAV_DATA["thrust_rotor"] = self.thrust_rotor
        UAV_DATA["efficiency_rotor"] = self.efficiency_rotor
        UAV_DATA["power_given"] = self.POWER_GIVEN
        UAV_DATA["max_weight"] = self.MAX_WEIGHT

        BASIC_DESC = """
{0}旋翼机重(g):{1} \n
电机型号:{2} \n
螺旋桨尺寸:{3} \n
所需最小悬停功率(w):{4}\n
单个旋翼所需提供的拉力(g):{5} \n
单个旋翼所需最小悬停功率(w):{6} \n
电机悬停效率为(g/w):{7} \n
给定额定功率(w):{8} \n
额定功率时旋翼总拉力(g):{9}
""".format(UAV_DATA["frame"], \
        UAV_DATA["weight"],UAV_DATA["motor"],UAV_DATA["propeller"], \
        UAV_DATA["power"],UAV_DATA["thrust_rotor"],UAV_DATA["power_rotor"], \
        UAV_DATA["efficiency_rotor"],UAV_DATA["power_given"],UAV_DATA["max_weight"])

        print("机臂水平时无人机动力系统信息：")
        print(BASIC_DESC)

        print('*'*50)

        # 机臂上反5度

        UAV_DATA["power_ita"] = self.MIN_POWER_ITA
        UAV_DATA["power_rotor_ita"] = self.power_rotor_ita
        UAV_DATA["thrust_rotor_ita"] = self.thrust_rotor_ita
        UAV_DATA["efficiency_rotor_ita"] = self.efficiency_rotor_ita
        UAV_DATA["max_weight_ita"] = self.MAX_WEIGHT_ITA

        BASIC_DESC_ITA = """
{0}旋翼机重(g):{1} \n
电机型号:{2} \n
螺旋桨尺寸:{3} \n
所需最小悬停功率(w):{4}\n
单个旋翼所需提供的拉力(g):{5} \n
单个旋翼所需最小悬停功率(w):{6} \n
电机悬停效率为(g/w):{7} \n
给定额定功率(w):{8} \n
额定功率时旋翼总拉力(g):{9}
""".format(UAV_DATA["frame"], \
        UAV_DATA["weight"],UAV_DATA["motor"],UAV_DATA["propeller"], \
        UAV_DATA["power_ita"],UAV_DATA["thrust_rotor_ita"],UAV_DATA["power_rotor_ita"], \
        UAV_DATA["efficiency_rotor_ita"],UAV_DATA["power_given"],UAV_DATA["max_weight_ita"])

        print("机臂上反5度时无人机动力系统信息：")
        print(BASIC_DESC_ITA)


"""
电机评估：
1、绘制图形，转速-拉力、转速-功率、功率-拉力
2、求解数据对因子: 功率-拉力、拉力-功率、转速-拉力、转速-功率
"""
class motor(object):

    def __init__(self):

        self.factors = {}
        self.vars = {} # save specific propeller's thrust,power and so on

    def read_motor_data(self,file):
        """
        读取CSV文件，加载电机数据
        """
        self.motor_data = pd.read_csv(file)


    def get_factors(self,propeller):
        """
        求解给定桨的线性拟合系数
        propeller : 桨尺寸，如2892
        从数据表中查询数据，得到字典类型,如{"power":[],"efficiency":[]}
        使用拟合函数求得关系因子，如线性关系： thrust = a * power + b
        返回 {"power-thrust":(a,b)}
        """

        self.propeller = propeller
        self.motor = self.motor_data["Item"][0]

        motor_data_propeller = self.motor_data[self.motor_data["Prop"] == self.propeller]

        self.vars['power'] = motor_data_propeller["Watts"].values
        self.vars['thrust'] = motor_data_propeller["Thrust"].values
        self.vars['efficiency'] = motor_data_propeller["Efficiency"].values
        self.vars['rpm'] = motor_data_propeller["RPM"].values

        # 功率-拉力
        self.factors["power-thrust"] = np.polyfit(self.vars['power'],self.vars['thrust'],2)
        # 拉力-功率
        self.factors["thrust-power"] = np.polyfit(self.vars['thrust'],self.vars['power'],2)

        # 转速-功率
        self.factors["rpm-power"] = np.polyfit(self.vars['rpm'],self.vars['power'],3)
        # 转速-拉力
        self.factors["rpm-thrust"] = np.polyfit(self.vars['rpm'],self.vars['thrust'],2)
        # 拉力-效率
        self.factors["thrust-efficiency"] = np.polyfit(self.vars['thrust'],self.vars['efficiency'],2)
        # 功率-效率
        self.factors["power-efficiency"] = np.polyfit(self.vars['power'],self.vars['efficiency'],2)
        print(self.factors)


    def figure_plot(self):

        length = len(self.factors)
        fig_row = 2
        if length % fig_row:
            fig_col = int(length/fig_row) + 1
        else:
            fig_col = int(length/fig_row)
        cur_fig = 1

        for key,value in self.factors.items():
            labels = key.split('-')
            x_label = labels[0]
            y_label = labels[1]

            polynome = np.poly1d(self.factors[key])
            # print("拟合多项式:",polynome)

            plt.subplot(fig_row,fig_col,cur_fig)

            yhat = polynome(self.vars[x_label])

            plt.plot(self.vars[x_label],self.vars[y_label],'b*')

            plt.plot(self.vars[x_label],yhat,'r')
            plt.title(key)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.legend()

            cur_fig += 1
        plt.show()

'''
给定电池数据，结合飞机数据，估算飞行时间
'''
class batterty():


    def __init__(self,xrotor,batt,num):
        self._xrotor = xrotor
        self.ACE_6S = {22000:488}
        self.capacity = batt
        self.ENERGY_PCT = 0.9
        self.energy = self.ACE_6S[batt]
        self.batt_num = num

    def time_calc(self):
        self.time = self.energy * self.ENERGY_PCT * self.batt_num / self._xrotor.MIN_POWER_ITA * 60

    def info(self):
        print("电池容量(mAh):",self.capacity,"\n")
        print("电池数量：",self.batt_num,"\n")
        print("单块电池电量(Wh):",self.energy,"\n")
        print("最大悬停时间(min):",self.time,"\n")
        pct = "放电百分比：{0}%".format(self.ENERGY_PCT*100)
        print(pct)

class airDensity():
    """
    根据环境温度、飞行高度估算空气密度
    公式：
    气压 P = 101325（1- 0.0065*h/(273.15+T)^5.2561
    密度 rho = 273.15*P/(101325 * (273.15 + T))*rho_b
    空气密度基数 rho_b = 1.293 kg/m^3，（0摄氏度，1标准大气压时101325帕）
    """
    def __init__(self, height=100):
        """
        height： 海拔，m
        """
        self.height = height
        self.air_density_base = 1.293
        self.temp = self.temperature()

    def pressure(self):
        return 101325.0 * ((1 - 0.0065 * self.height / (273.15 + self.temp)) ** 5.2561)

    def density(self):
        return 273.15 * self.pressure() / (101325.0 * (273.15 + self.temp)) * self.air_density_base

    def temperature(self):
        """
        在国际标准中，设海平面处温度为15摄氏度，10000米高空温度为-50摄氏度
        垂直区间温度变化均匀，空气密度与温度成反比
        T = 273.15 + t_down - (t_down - t_up) / 10000 * H
        """
        temperature_up = 50.0
        temperature_down = 15.0
        return temperature_down - (temperature_down + temperature_up) / 10000.0 * self.height

class rotorModel():
    """
    一、螺旋桨拉力逆模型
    拉力公式：f = C_T * rho * (N / 60)^2 * D^4
    C_T : 螺旋桨拉力系数
    rho : 空气密度
    N ：转速， rpm
    D : 螺旋桨直径, m

    单个旋翼拉力： f = G / n
    G ：飞机重量， N
    n ：螺旋桨个数

    旋翼拉力简化公式：f = c_T * w^2
        c_T = 1/(4*pi^2)*rho*D^4*C_T

    拉力逆模型：N = 60 * sqrt(G / (n * D^4 * C_T * rho))

    二、转矩模型
    转矩： M = C_M * rho * (N / 60)^2 * D^5
    C_M : 螺旋桨转矩系数
    拉力逆模型：N = 60 * sqrt(G / (n * D^4 * C_T * rho))
    可知，M = C_M * G / (n * C_T) * D

    旋翼扭矩简化公式： M = c_M * w ^ 2, c_M = 1/(4*pi^2)*rho*D^5*C_M

    the formula for calculating torque
    http://simplemotor.com/calculations/
    电机扭矩测试很费劲儿，上述网址给出一个简单的、不甚精确的计算扭矩的公式。
    1. P_in = I * V
        P_in : 电机输入电功率
    2. P_out = T * w
        P_out ：电机输出机械功率
        T ：扭矩
        w ：omega, 角速率，rad/s
    3. w = N * 2 * pi / 60
        转速转角速率，rpm --> rad/s
    4. E = P_out / P_in
        E : 效率
    5. P_out = P_in * E
       => T * w = I * V * E
       => T * rpm * 2 * pi / 60 = I * V * E
       => T = (I * V * E * 60)/(rpm * 2 * pi)

    http://simplemotor.com/torque-and-efficiency-calculation/
    电流、电压、转速可以准确测量，而转换效率却不能准确估计。
    In general for small electric motors (and the kit motor is not an exception)
    maximum power is at approximately 50% of stall torque where the speed usually is at 50% of maximum no-load speed.
    Maximum efficiency is usually at 10-30% of motor stall torque, or at 70-90% of no-load speed.
    一般地，小型电机最大功率点出现在大约50%堵转力矩处，此时转速约为最大空载转速的50%。
    而最大效率点为电机堵转力矩10~30%处，或70~90%空载转速处。

    三、电机模型
    Kv常数解释
    http://learningrc.com/motor-kv/
    https://en.wikipedia.org/wiki/Motor_constants
    Kv值常见的解释为：无刷直流电机空载时每增加1V工作电压增加的转速
    正确的解释：电机以1标准Kv值转动时产生的反电动势为1V
    1. K_E = 1/Kv
        K_E : 反电动势常数, v/rpm
        Kv : rpm/v
    2. K_T = T / I_A = 60 / (2 * Pi * Kv) = 9.55 * K_E = 9.55 / Kv
        K_T ：扭矩系数，N*m/A = V/(rad/s)
        Kv : rpm/v
        K_T与K_E是同一回事。

        Kv = 3600 (rpm/v) = 3600 * 2 * pi / 60 (rad/s)
        T = K_T * I_A = 9.55 / 3600 = 0.00265 (N*m/A)
        即是说，一个3600Kv的电机，当它转速为3600rpm时，每1A的电枢电流产生的扭矩为0.00265 N*m/A
    3. Kv值测量
        http://learningrc.com/motor-kv/
        Kv = rpm/(v * 1.414 * 0.95)

    输出转矩：
        M = K_T * （Im - Im0）
        Im : 等效电流
        Im0 : 电机空载电流

    等效电流：
        Im = M / K_T + Im0
    等效电压：
        Um = K_E * N + Rm * Im
        Rm : 电机内阻

    四、电调模型
        油门百分比： sigma
        电调调制后的等效直流电压：Ue0
            Ue0 = Um + Im * Re
            Re : 电调内阻

            sigma = Ue0 / Ue ~= Ue0 / Ub
            Ub : 电池电压
        如果不考虑电调内阻，则
            sigma = Um / Ub

        电调输入电流：
            Ie = sigma * Im
        电调输入电压（电池输出电压）：
            Ue = Ub - n*Ie*Rb
            n : 电调个数
            Rb：电池内阻

    五、电池模型
        Ib = n * Ie + Iother
        Iothre : 飞控、云台等电子设备消耗电流

        放电时间(min)：
            Tb = (Cb - Cmin) / Ib * 60 / 1000
            Cb : 电池容量，mAh
            Cmin : 电池放电剩余容量，mAh
    """
    def __init__(self, motor):
        """
        motor为电机实例
        
        """
        pass

def xrotor_estimate(params):
    pass

if __name__ == "__main__":
    file_path  = r'E:\DATAANALYSE\UAV\copter\motor_dataset\TMotorU8KV135.csv'
    # file_path  = r'F:\data_analysis\UAV\motor_dataset\TMotorU10KV170.csv'
    # file_path  = r'F:\data_analysis\UAV\motor_dataset\TMotorMN5212KV340.csv'
    # file_path  = r'F:\data_analysis\UAV\motor_dataset\TMotorMN5212KV340_M.csv'
    tMotor = motor()
    tMotor.read_motor_data(file_path)
    tMotor.get_factors(2995)
    tMotor.figure_plot()

    copter = xrotor(tMotor,1200,13000,6)
    copter.uav_info()

    batt = batterty(copter,22000,2)
    batt.time_calc()
    batt.info()
