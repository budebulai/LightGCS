# -*- coding:utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

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

def rpm_to_rad(rpm):
    """
    rpm --> rad/s : 2 * pi * rpm / 60
    """
    return 2 * np.pi * rpm / 60.0

def rad_to_rpm(radps):
    """
    rad/s --> rpm : rad * 30 / pi
    """
    return radps * 30.0 / np.pi

class xrotor(object):
    """

    """

    def __init__(self,params,rotor,deg = 5.0):
        """
        params: xrotor params, dict type
        rotor: handler of class rotorModel instance
        deg: angle between rotor center line and uav perpendicular line
        """
        self.rotor = rotor
        self.params = params
        # 机臂上反5度
        self.scaler = np.cos(np.deg2rad(deg))

    def xrotor_check(self):
        """
        - 重量检查
        - 桨径计算
        。。。
        """
        pass

    def propeller_check(self, gap = 15.0):
        """
        Given copter diagonal motor axises's distance and vehicle frame,
        calculating the max size propeller that vehicle can use.
        And check if the given propeller size is suitable.
        dist: distance between two diagonal motor axises in millimeter
        frame: 4,6,8.  vehicle with numbers of axises
        gap: distance between two propellers' tip
        """
        dist = self.params["axisDist"]
        frame = self.params["frame"]

        if frame == 4:
            size = (dist / math.sqrt(2)) - gap
        elif frame == 6:
            size = (dist / 2.0) - gap
        elif frame == 8:
            size = (dist * np.sin(np.deg2rad(22.5))) - gap
        self.propeller_size = int(size / 25.4) # millimeter converted to inch

        if self.params["propeller"] > self.propeller_size:
            pass

    def weight_check(self):
        """
        给定各部件重量，计算无人机总重量
        """
        pass

    def get_power(self):
        """
        给定无人机重量，求解最小所需功率
        """
        pass


    def uav_max_weight(self):
        """
        给定无人机功率，求得最大起飞重量
        """
        pass

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
给定电池电压及容量，估算重量、电量，后期给出电池放电平台曲线
'''
class batterty():
    def __init__(self,volt, capacity=10000):
        """
        volt: working voltage, such as 22.2, 44.4, etc.
        capacity: LiPo capacity, deault 10000 mAh
        """


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
    def __init__(self, height=100.0, groundTemperature=25.0):
        """
        height： 海拔，m
        """
        self.height = height
        self.air_density_base = 1.293
        self.temp = self.temperature(groundTemperature)

    def pressure(self):
        return 101325.0 * ((1 - 0.0065 * self.height / (273.15 + self.temp)) ** 5.2561)

    def density(self):
        return 273.15 * self.pressure() / (101325.0 * (273.15 + self.temp)) * self.air_density_base

    def temperature(self, groundTemperature):
        """
        在国际标准中，设海平面处温度为15摄氏度，10000米高空温度为-50摄氏度
        垂直区间温度变化均匀，空气密度与温度成反比
        T = 273.15 + t_down - (t_down - t_up) / 10000 * H
        这里使用默认近地温度25度
        """
        temperature_up = 50.0
        temperature_down = groundTemperature
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

    六、桨转动一圈前进的距离
    http://www.wulong9.com/jiaocheng/20160901631.html
    螺旋桨规格定义：直径(D) x 螺距(Pitch)
    Pitch：螺距，桨转动一周前进的距离
    R：桨半径
    U：3/4*R处的平均叶片角度
    转动一圈前进的距离Pitch = 3/4 * R * tan(U)
    - 3/4半径处圆周长
        L = 2 * pi * (D/2*3/4) = pi * D * 3 / 4 (inch)
    - 桨叶平均角度
        U = atan(Pitch/L) (deg)
    如22x10桨，平均叶片角度是多少呢？
        L = 3.1415926 * 22 * 3 / 4 = 51.83627878423158 inch
        U = atan(10/L) = 10.919083051507858 deg
        `
        import numpy as np
        L = np.pi * 22 * 3 / 4
        U = np.arctan2(10,L)
        `
    如果要进行变距操作，可根据螺旋桨前进的速度来改变螺距角

    关于螺旋桨的另一点，
    攻角：桨前进方向与翼弦中心线之间的夹角，一般稍低于叶片角度2~5度（视翼型）

    七、性能参数
        悬停时间
        油门百分比
        最大载重
        最大倾斜角
        最大飞行速度
        最大飞行距离
        综合飞行时间
        抗风等级

    """
    def __init__(self, data, params):
        """
        检索电机测试数据库，查询相应尺寸桨测试数据，计算拉力、扭矩系数

        """
        self.data = data
        self.params = params

    def data_cleaning(self):
        """
        桨数据分组，并剔除数据不全的行
        """
        pass

    def rotor_factors(self):
        """
        根据拉力数据计算拉力、扭矩因子
        """
        pass

    



class report_output():
    """
    生成markdown文件，并用浏览器打开
    或
    生成doc： python-docx
    https://github.com/trentm/python-markdown2

    http://www.cnblogs.com/rencm/p/6285304.html
    http://blog.csdn.net/mlgglm/article/details/51463588

    http://www.bagualu.net/wordpress/archives/5304

    http://john88wang.blog.51cto.com/2165294/1424968
    """
    pass

def parameter_convert(params):
    """
    params = {"KEYS":"VALUES"}
    KEYS = ["weight","frame","axisDist","height","temperature","motor","propeller","voltage","capacity","residual"]
    无人机重量、机型、电机、桨必不可少，其它数据为可选。
    "weight"值已在界面处转换为整形数值
    "frame"机型不指定时，默认为4轴
    "axisDist"轴距可不填。有值时评估桨、电机是否合适。
    "motor/propeller"电机、桨指定型号，从数据库查询数据
    "temperature"为近地温度，默认25摄氏度
    "height"无人机飞行高度，默认100m
    "voltage"无人机动力系统工作电压
    "capacity"无人机能源容量，mAh
    "residual"无人机能量剩余百分比乘以100，可预处理,除以100
    """
    for key, value in params.items():
        if not value:
            del params[key]

    # 默认值填充
    # 机型，其它异型不考虑
    uav_frame = {"Quad":4,"Hexa":6,"Octo":8}
    params["frame"] = uav_frame.get(params["frame"],4)

    # 轴距
    params["axisDist"] = float(params.get("axisDist",0))

    params["voltage"] = params.get("voltage","")
    if params["voltage"]:
        params["voltage"] = float(params["voltage"].split("--")[1].rstrip('V'))

    # 飞行高度
    params["height"] = float(params.get("height",100.0))

    # 近地温度
    params["temperature"] = float(params.get("temperature",25.0))

    # 电量
    params["capacity"] = float(params.get("capacity",10000.0))

    # 放电剩余百分比
    params["residual"] = float(params.get("residual",15.0))/100.0


def xrotor_estimate(params):
    """

    """
    parameter_convert(params)

    db_file = os.path.split(os.path.realpath(__file__))[0] + "\\rotor_db\\motors.db"
    conn = sqlite3.connect(db_file)

    # 选定电机的拉力数据中可能没有相应选定桨的数据，选定桨肯定有数据，有可能不止一组
    # 获取电机拉力数据
    motor_data = pd.read_sql(motor_data_sql(params["motor"]),conn)
    # 获取数据库中关于选定桨的数据
    rotor_data = pd.read_sql(motor_data_sql(params["propeller"]),conn)



def motor_info_sql(motor):
    sql = {"table":"motorInfo"}
    sql["condition"] = "Motor='{}'".format(motor)
    return dql_encapsulate(sql)

def motor_data_sql(motor):
    sql = {"table":"motorData"}
    sql["condition"] = "Motor='{}'".format(motor)
    return dql_encapsulate(sql)

def dql_encapsulate(params):
    """
    params = {"table":tablename, "fields":["ID","name",...], "conditions":xxx}
    """
    table = params["table"]
    fields = params.get("fields","")
    condition = params.get("condition","")

    if not fields:
        fields = "*"

    fields = ",".join(fields)

    if condition:
        condition = "WHERE " + condition

    return "SELECT {} FROM {} {};".format(fields, table, condition)


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
