#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    temperature and humidity measurement Tango Device Server
    
    Created on Wed Apr 22 15:19:58 2020

    @author: mbi

"""

import numpy
from tango import AttrWriteType, DevState, ErrorIt, FatalIt
from tango import LogIt, DebugIt, InfoIt, WarnIt
from tango.server import Device, attribute, command
import AM2315 as am_driver

class TempHum(Device):
    
    temperature = attribute(name='Temperature',access=AttrWriteType.READ,
                            dtype=float,fget='get_temperature',format='.2f',
                            min_value=-273.15,doc='the measured temperature')
    
    humidity = attribute(name='Humidity',access=AttrWriteType.READ
                         ,dtype=float,fget='get_humidity',format='.2f',
                         doc='the measured humidity')
    
    def init_device(self):
        try:
            Device.init_device(self)
            self.am2315 = am_driver.AM2315()
            self.set_state(DevState.ON)
            self.temp = 0
            self.humid = 0
            self.info_stream("conenction established")
            
        except:
            return('There was no AM2315-Device found.')
        
    @DebugIt()            
    @command(polling_period=500)
    def get_data(self):
        #_read_data measures both humidity and temperature
        self.am2315._read_data()
        self.temp = self.am2315.temperature
        self.humid = self.am2315.humidity
        
    @InfoIt(show_ret=True)               
    def get_temperature(self):
        return self.temp
    
    @InfoIt(show_ret=True)    
    def get_humidity(self):
        return self.humid   

    def read_state(self):
        return self.state()

if __name__ == "__main__":
    TempHum.run_server()
