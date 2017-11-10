# -*- coding: utf-8 -*-

class uavPID():
    def __init__(self, params):
        pass
    pass

class copterPID(uavPID):
    pass

class fwPID(uavPID):
    def __init__(self, params, obj):
        """
        params : dronekit.vehicle.Parameters
        obj    : self.f_pid
        """
        cbs = obj.findChildren(QDoubleSpinBox)
        for item in cbs:
            print item.objectName()
    pass
