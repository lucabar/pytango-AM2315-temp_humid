#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    temperature and humidity measurement Tango Device Server
    
    Created on Wed Apr 22 15:19:58 2020

    @author: mbi

"""

import numpy
from tango import AttrWriteType, DevState
from tango.server import Device, attribute, command
import AM2315 as am_driver

class TempHum(Device):
    
    temperature = attribute(access=AttrWriteType.READ,
                            fget='get_temperature', polling_period=500)
    
    humidity = attribute(access=AttrWriteType.READ,
                        fget='get_humidity', )
    
    def init_device(self):
        Device.init_device(self)
        self.am2315 = am_driver.AM2315()
        self.set_state(DevState.STANDBY)
        self.temp = 0
        self.humid = 0

    @command(polling_period=500)
    def get_data(self):
        print("get data")
        self.temp = self.am2315.read_temperature()
        self.humid = self.am2315.read_humidity()
        
    def get_temperature(self):
        return self.temp
    
    def get_humidity(self):
        return self.humid
        

    
    def read_state(self):
        return self.state()

if __name__ == "__main__":
    TempHum.run_server()
