# -*- coding:utf-8 -*-

# import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sql_tool import *
from PyQt5.QtWidgets import QMessageBox, QComboBox
import threading
from actions import wonf

@wonf
def xrotor_params_init(self):
    """
    Init xrotor groupbox all QCombobox
    """
    # db table init
    create_table_motorList()
    create_table_motorData()
    create_table_motorInfo()
    create_table_propellerInfo()

    self.xrotor_params = [self.le_weight, \
                          self.cb_copter_frame, \
                          self.le_uav_axisDist, \
                          self.le_flight_height, \
                          self.le_ground_temperature, \
                          self.cb_motor_type, \
                          self.cb_prop_type, \
                          self.cb_volt, \
                          self.le_battery_capacity, \
                          self.le_capacity_residual]
    self.xrotor_params_key = ["weight", \
                              "frame", \
                              "axisDist", \
                              "height", \
                              "temperature", \
                              "motor", \
                              "propeller", \
                              "voltage", \
                              "capacity", \
                              "residual"]

    self.cb_copter_frame.clear()
    self.cb_copter_frame.addItems(["", "Quad", "Hexa", "Octo"])

    params = {"table": "motorData"}
    params["fields"] = ["Motor", "Propeller"]
    ret = table_query(params)

    motors = set([item[0] for item in ret if item[0]])
    propellers = set([str(item[1]) for item in ret if item[1]])

    self.cb_motor_type.clear()
    self.cb_motor_type.addItem("")
    self.cb_motor_type.addItems(motors)
    self.cb_prop_type.clear()
    self.cb_prop_type.addItem("")
    self.cb_prop_type.addItems(propellers)

    volt_list = [""]
    for i in range(2, 13):
        item = "{}S--{:.1f}V".format(i, i * 3.7)
        volt_list.append(item)
    self.cb_volt.clear()
    self.cb_volt.addItems(volt_list)

    self.xrotor_initialised = True

@wonf
def check_xrotor_params(self, params):
    if not (params["weight"] and params["frame"] and params["motor"] and params["propeller"]):
        return False
    try:
        "convert string weight to int"
        params["weight"] = int(params["weight"])
        assert params["weight"] > 0

        for i in range(len(self.xrotor_params_key)):
            if isinstance(self.xrotor_params[i], QComboBox):
                continue
            if params[self.xrotor_params_key[i]]:
                params[self.xrotor_params_key[i]] = float(params[self.xrotor_params_key[i]])
                if self.xrotor_params_key[i] == "temperature":
                    continue
                assert params[self.xrotor_params_key[i]] > 0

    except Exception:
        return False
    return True

@wonf
def copter_estimator(self):
    # get params
    param_values = []
    for i in range(len(self.xrotor_params)):
        if isinstance(self.xrotor_params[i],QComboBox):
            param_values.append(self.xrotor_params[i].currentText())
        else:
            param_values.append(self.xrotor_params[i].text())
    params = dict(zip(self.xrotor_params_key, param_values))

    if self.check_xrotor_params(params):
        xrotor_estimate_thread = threading.Thread(target=estimator,args=(params,))
        xrotor_estimate_thread.setDaemon(True)
        xrotor_estimate_thread.start()
    else:
        """
        StandardButton QMessageBox::critical(
            QWidget *parent,
            const QString &title,
            const QString &text,
            StandardButtons buttons = Ok,
            StandardButton defaultButton = NoButton)
        """
        mb_text = "You have selected parameters below"
        just = 0
        for key, _ in params.items():
            just = max(len(key),just)

        lst = ['%s: %s' % (k.rjust(just), str(v)) for (k, v) in params.items()]
        lst.sort()
        mb_text = '\n'.join(lst)

        QMessageBox.critical(self, "Parameters Invalid", mb_text)

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

class motor(object):
    """
    根据电机拉力数据，获取数据中的最大功率，扭矩系数，拉力-功率曲线系数
    遥杆指令与转速间是什么关系呢？油门百分比与稳态转速呈线性关系，但系数与负载有关。
    """
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
        pass


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
    剔除数据不全的行:RPM为空
    因为这两个字段为关键数据

    输出功率 = 扭矩 * 角速度
    电机转换效率差别有多大呢？实际上不大
    因此，同一个桨，其模型建立之后，可以放在不同的电机上使用，至于选用什么样的电机，就看其工作特性，能否带的动桨。
    电机的效率数据，实际上可以认为是桨的效率,同一个桨在不同的电机上测试，效率应该差别不大
    """

    def __init__(self, data, params):
        """
        根据桨拉力数据，计算转速-拉力-扭矩曲线系数，拉力、扭矩系数
                 ["Motor",\
                  "Voltage",\
                  "Propeller",\
                  "Throttle",\
                  "Amps",\
                  "Watts",\
                  "Thrust",\
                  "RPM",\
                  "Moment",\
                  "Efficiency"]
        """
        self.data = data
        self.params = params
        self.rotor_factors()

    def rotor_factors(self):
        """
        数据分组，并根据拉力-转速数据计算拉力、扭矩因子
        """
        self.factors = {}

        max_thrust = self.data["Thrust"].values.max()
        min_thrust = self.data["Thrust"].values.min()
        max_power = self.data["Watts"].values.max()
        min_power = self.data["Watts"].values.min()

        print self.data

        # Thrust --> Watts
        g = self.data.groupby("Motor")
        for item in g:
            pass

        # cT,cM
        d = self.data[self.data["RPM"].isnull().values == False]

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
    "voltage"无人机动力系统工作电压,6,10,12S等
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
    # 电压
    params["voltage"] = params.get("voltage","")
    if params["voltage"]:
        params["voltage"] = float(params["voltage"].split("--")[0].rstrip('S'))
    # 飞行高度
    params["height"] = float(params.get("height",100.0))
    # 近地温度
    params["temperature"] = float(params.get("temperature",25.0))
    # 电量
    params["capacity"] = float(params.get("capacity",10000.0))
    # 放电剩余百分比
    params["residual"] = float(params.get("residual",15.0))/100.0


def estimator(params):
    """

    """
    parameter_convert(params)

    db_file = os.path.split(os.path.realpath(__file__))[0] + "\\rotor_db\\motors.db"
    conn = sqlite3.connect(db_file)

    # 选定电机的拉力数据中可能没有相应选定桨的数据，选定桨肯定有数据，有可能不止一组
    # 获取电机拉力数据
    motor_data = pd.read_sql(motor_data_sql(motor = params["motor"]),conn)
    # 获取数据库中关于选定桨的数据
    rotor_data = pd.read_sql(motor_data_sql(propeller = params["propeller"]),conn)

    rotor = rotorModel(rotor_data,params)



def motor_info_sql(motor):
    sql = {"table":"motorInfo"}
    sql["condition"] = "Motor='{}'".format(motor)
    return dql_encapsulate(sql)

def motor_data_sql(motor=None,propeller=None):
    sql = {"table":"motorData"}
    if motor:
        sql["condition"] = "Motor='{}'".format(motor)
    if propeller:
        sql["condition"] = "Propeller='{}'".format(propeller)
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
