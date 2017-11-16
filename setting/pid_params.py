# -*- coding: utf-8 -*-
"""
SYSID_SW_TYPE
ReadOnly	Values
True
Value	Meaning
0	ArduPlane
4	AntennaTracker
10	Copter
20	Rover
40	ArduSub

旋翼机PID参数
x_rol_p                 ：
x_pit_p
x_yaw_p
x_rol_spd_p
x_rol_spd_i
x_rol_spd_d
x_rol_spd_imax
x_rol_spd_filter
x_pit_spd_p
x_pit_spd_i
x_pit_spd_d
x_pit_spd_imax
x_pit_spd_filter
x_yaw_spd_p
x_yaw_spd_i
x_yaw_spd_d
x_yaw_spd_imax
x_yaw_spd_filter
x_height_hold_p
x_throttle_accel_p
x_throttle_accel_i
x_throttle_accel_d
x_throttle_accel_imax
x_throttle_spd_p
x_loiter_spd_p
x_loiter_spd_i
x_loiter_spd_d
x_loiter_spd_imax
x_loiter_p
x_nav_descend_spd
x_nav_wp_radius
x_nav_climb_spd
x_nav_spd
x_nav_land_spd


固定翼机PID参数
f_rol_p
f_rol_i
f_rol_d
f_rol_imax
f_pit_p
f_pit_i
f_pit_d
f_pit_imax
f_yaw_p
f_yaw_i
f_yaw_d
f_yaw_imax
f_cruise_pct
f_throttle_min_pct
f_throttle_max_pct
f_rotate_speed
f_cruise_speed
f_speed_min
f_speed_max
f_speed_pct
f_angle_rol_limit
f_angle_pitch_up_max
f_angle_pitch_down_max
f_climb_spd_max
f_descend_spd_min
f_descend_spd_max
f_pitch_restrain
f_tecs_time
f_l1_period
f_l1_drag
f_tilt_time
f_tilt_failspeed

"""

from PyQt5.QtWidgets import QDoubleSpinBox

class uavPID(object):
    SW_TYPE = {0:"ArduPlane",10:"ArduCopter"}

    def __init__(self, params, obj):
        """
        params : dronekit.vehicle.Parameters
        obj    : self.f_pid, tab widget
        """
        self.spinboxes = obj.findChildren(QDoubleSpinBox)
        self.sw_type = uavPID.SW_TYPE[int(params["SYSID_SW_TYPE"])]
        # for item in self.spinboxes:
        #     print item.objectName()
        #
        # print self.sw_type


    def reset(self):
        pass

    def write(self, params):
        pass

    def read(self):
        pass

    def update(self):
        pass

class copterPID(uavPID):
    def __init__(self, params, obj):
        """
        params : dronekit.vehicle.Parameters
        obj    : self.f_pid
        """
        super(fwPID,self).__init__(params, obj)

    def :
        pass

class fwPID(uavPID):
    def __init__(self, params, obj):
        """
        params : dronekit.vehicle.Parameters
        obj    : self.f_pid
        """
        super(fwPID,self).__init__(params, obj)
