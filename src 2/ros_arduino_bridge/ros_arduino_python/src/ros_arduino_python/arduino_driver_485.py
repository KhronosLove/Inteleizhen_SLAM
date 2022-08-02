#!/usr/bin/env python

"""
    A Python driver for the Arduino microcontroller running the
    ROSArduinoBridge firmware.

    Created for the Pi Robot Project: http://www.pirobot.org
    Copyright (c) 2012 Patrick Goebel.  All rights reserved.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details at:

    http://www.gnu.org/licenses/gpl.html

"""
import ctypes
import _thread as thread
from math import pi as PI, degrees, radians
import os
import time
import sys, traceback
from serial.serialutil import SerialException
from serial import Serial

SERVO_MAX = 180
SERVO_MIN = 0


act_enable  = "01442100310000010001"
act_disable = "01442100310000000000"
act_get_encoders  = "014350045104"


class Arduino485:
    ''' Configuration Parameters
    '''
    N_ANALOG_PORTS = 6
    N_DIGITAL_PORTS = 12

    def __init__(self, port="/dev/ttyUSB0", baudrate=19200, timeout=0.5, motors_reversed=False):

        self.PID_RATE = 30 # Do not change this!  It is a fixed property of the Arduino PID controller.30

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.encoder_count = 0
        self.writeTimeout = timeout
        self.interCharTimeout = timeout / 30.
        self.motors_reversed = motors_reversed
        # Keep things thread safe
        self.mutex = thread.allocate_lock()

        # An array to cache analog sensor readings
        self.analog_sensor_cache = [None] * self.N_ANALOG_PORTS

        # An array to cache digital sensor readings
        self.digital_sensor_cache = [None] * self.N_DIGITAL_PORTS  
        
        self.enc_left_last = 0 
        self.enc_right_last = 0
        
        self.enc_left = 0
        self.enc_right = 0

    def connect(self):
        try:
            print ("Connecting to Arduino RS485 on port", self.port, "...")
            self.port = Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout, writeTimeout=self.writeTimeout)
            # The next line is necessary to give the firmware time to wake up.
            #time.sleep(1)
            #test = self.get_baud()
            #if test != self.baudrate:
            #    time.sleep(1)
            #    test = self.get_baud()
            #    if test != self.baudrate:
            #        raise SerialException
            print ("Connected at", self.baudrate)
            print ("Arduino 485 is ready.")

        except SerialException:
            print ("Serself.mutexial Excr_leneption:")
            print (sys.exc_info())
            print ("Tracebackstr_return_data follows:")
            traceback.print_exc(file=sys.stdout)
            print ("Cannot connect to Arduino 485!")
            os._exit(1)

    def send485(self,data,r_len=12): 
        self.mutex.acquire()
        str_return_data = ""
        
        try:
            self.port.flushInput()
        except:
            pass
        
        try:
            data = data + crc16(data)
            #print(data)
            #self.port.write(data.decode("hex").encode())
            self.port.write(bytes.fromhex(data))
            time.sleep(0.1)
            len_return_date = self.port.inWaiting()
            if len_return_date:
                return_data = self.port.read(r_len)
                str_return_data = str(return_data.hex())
        except:
            self.mutex.release()
        
        self.mutex.release()
        return str_return_data
    

    def open(self):
        ''' Open the serial port.
        '''
        self.port.open()

    def close(self):


        ''' Close the serial port.
        '''
        self.port.close()

    def send(self, cmd):
        ''' This command should not be used on its own: it is called by the execute commands
            below in a thread safe manner.
        '''
        self.port.write((cmd + '\r').encode())

    def recv(self, timeout=0.5):
        timeout = min(timeout, self.timeout)
        ''' This command should not be used on its own: it is called by the execute commands
            below in a thread safe manner.  Note: we use read() instead of readline() since
            readline() tends to return garbage characters from the Arduino
        '''
        c = ''
        value = ''
        attempts = 0
        while c != '\r':
            c = self.port.read(1).decode()
            value += c
            attempts += 1
            if attempts * self.interCharTimeout > timeout:
                return None

        value = value.strip('\r')

        return value

    def recv_ack(self):
        ''' This command should not be used on its own: it is called by the execute commands
            below in a thread safe manner.
        '''
        ack = self.recv(self.timeout)
        return ack == 'OK'

    def recv_int(self):
        ''' This command should not be used on its own: it is called by the execute commands
            below in a thread safe manner.
        '''
        value = self.recv(self.timeout)
        try:
            return int(value)
        except:
            return None

    def recv_array(self):
        ''' This command should not be used on its own: it is called by the execute commands
            below in a thread safe manner.
        '''
        try:
            values = self.recv(self.timeout * self.N_ANALOG_PORTS).split()
            return map(int, values)
        except:
            return []

    def execute(self, cmd):
        ''' Thread safe execution of "cmd" on the Arduino returning a single integer value.
        '''
        self.mutex.acquire()

        try:
            self.port.flushInput()
        except:
            pass

        ntries = 1
        attempts = 0

        try:
            self.port.write((cmd + '\r').encode())
            value = self.recv(self.timeout)
            while attempts < ntries and (value == '' or value == 'Invalid Command' or value == None):
                try:
                    self.port.flushInput()
                    self.port.write((cmd + '\r').encode())
                    value = self.recv(self.timeout)
                except:
                    print ("Exception executing command: " + cmd)
                attempts += 1
        except:
            self.mutex.release()
            print ("Exception executing command: " + cmd)
            value = None

        self.mutex.release()
        return int(value)

    def execute_array(self, cmd):
        ''' Thread safe execution of "cmd" on the Arduino returning an array.
        '''
        self.mutex.acquire()

        try:
            self.port.flushInput()
        except:
            pass

        ntries = 1
        attempts = 0

        try:
            self.port.write((cmd + '\r').encode())
            values = self.recv_array()
            while attempts < ntries and (values == '' or values == 'Invalid Command' or values == [] or values == None):
                try:
                    self.port.flushInput()
                    self.port.write((cmd + '\r').encode())
                    values = self.recv_array()
                except:
                    print("Exception executing command: " + cmd)
                attempts += 1
        except:
            self.mutex.release()
            print ("Exception executing command: " + cmd)
            raise SerialException
            return []

        try:
            values = map(int, values)
        except:
            values = []

        self.mutex.release()
        return values

    def execute_ack(self, cmd):
        ''' Thread safe execution of "cmd" on the Arduino returning True if response is ACK.
        '''
        self.mutex.acquire()

        try:
            self.port.flushInput()
        except:
            pass

        ntries = 1
        attempts = 0

        try:
            self.port.write((cmd + '\r').encode())
            ack = self.recv(self.timeout)
            while attempts < ntries and (ack == '' or ack == 'Invalid Command' or ack == None):
                try:
                    self.port.flushInput()
                    self.port.write((cmd + '\r').encode())
                    ack = self.recv(self.timeout)
                except:
                    print ("Exception executing command: " + cmd)
            attempts += 1
        except:
            self.mutex.release()
            print ("execute_ack exception when executing", cmd)
            print (sys.exc_info())
            return 0

        self.mutex.release()
        return ack == 'OK'

    def update_pid(self, Kp, Kd, Ki, Ko):
        ''' Set the PID parameters on the Arduino
        '''
        print ("Updating PID parameters")
        cmd = 'u ' + str(Kp) + ':' + str(Kd) + ':' + str(Ki) + ':' + str(Ko)
        self.execute_ack(cmd)

    def get_baud(self):
        ''' Get the current baud rate on the serial port.
        '''
        try:
            return int(self.execute('b'));
        except:
            return None

    def get_encoder_counts(self):
        
        enc_l = self.send485("014350165015")
        enc_r = self.send485("014351165115")
        
        
        enc_l = ctypes.c_int32(int(enc_l[12:20],16)).value
        enc_r = -ctypes.c_int32(int(enc_r[12:20],16)).value
        
        if self.motors_reversed:
            enc_l,enc_r = -enc_l,-enc_r
        
        self.enc_left += enc_l - self.enc_left_last
        self.enc_right += enc_r - self.enc_right_last
        
        #print("left",left,"right",right)
        
                
        self.enc_left_last = enc_l
        self.enc_right_last = enc_r        
        
        #if self.motors_reversed:
            #self.enc_left,self.enc_right = -self.enc_left,-self.enc_right
            
        #print("left",self.enc_left,"right",self.enc_right)
        
        return self.enc_left,self.enc_right
        
        #values = self.execute_array('e')
        #if len(values) != 2:
        #    print "Encoder count was not 2"
        #    raise SerialException
        #    return None
        #else:
         #   if self.motors_reversed:
        #        values[0], values[1] = -values[0], -values[1]
        #    return values

    def init(self):
        # set can modify Pn5.00A = 0 and save data in memory
        d = "0106450A0001"
        self.send485(d)
        # set wheel A,B speed model 
        d = "010621020001"
        self.send485(d)
        
        d = "010631020001"
        self.send485(d)
        # set default speed = 0
        d = "010623180000"
        self.send485(d)
        
        d = "010633180000"
        self.send485(d)
        # set default disabled 
        d = "010621000000"
        self.send485(d)
        
        d = "010631000000"
        self.send485(d)
        
        # set stop modify
        d = "0106450A0000"
        self.send485(d)        

    def reset_encoders(self):
        ''' Reset the encoder counts to 0
        '''        
        
        enc_l = self.send485("014350165015")
        enc_r = self.send485("014351165115")
        
        enc_l = ctypes.c_int32(int(enc_l[12:20],16)).value
        enc_r = -ctypes.c_int32(int(enc_r[12:20],16)).value
        
        if self.motors_reversed:
            enc_l,enc_r = -enc_l,-enc_r
        
        self.enc_left_last = enc_l
        self.enc_right_last = enc_r
           
        self.enc_left = 0
        self.enc_right = 0

    def getSenceDistence(self,sendesIDs):
        results=[]
        for i in range(len(sendesIDs)):
            result = self.send485("050300"+hex(sendesIDs[i])[:-2])
            results.append(result[8:12],16)
        return results
    
    def drive(self,right,left ):
        ''' Speeds are given in encoder ticks per PID interval
        '''
        #if left>50:
            #left=5
        #elif left<-50:
            #left=-5
        
        #if right>50:
            #right=5
        #elif right<-50:
            #right=-5
        
        left = -int(left)
        right = int(right)
        if self.motors_reversed:
            left, right = -left, -right
        
        #if left>0:
        #    print("left",left)
        #    print("right",right)
        
        if left>=0:
            left_str = "00" + ("0"+hex(left)[2:])[-2:]
        else:
            left_str = "ff" + hex(left&0xFFFFFFFF)[-2:]
        
        if right>=0:
            right_str = "00" + ("0"+hex(right)[2:])[-2:]
        else:
            right_str = "ff" + hex(right&0xFFFFFFFF)[-2:]
        
        d = "014423183318"+right_str+left_str
        self.send485(d)
        
        #print(d)
            
        #return self.execute_ack('m %d %d' %(right, left))

    def drive485(self,x, th ):
        
        x = x*1000
        th = th*1000
        
        if x>200:
            x = 200
        
        if x>=0:
            x_str = ("0"+hex(int(x))[2:])[-2:] + "00"
        else:
            x_str = hex(int(x)&0xFFFFFFFF)[-2:] + "ff"
        
        if th>=0:
            th_str = ("0"+hex(int(th))[2:])[-2:] + "00"
        else:
            th_str = hex(int(th)&0xFFFFFFFF)[-2:] + "ff"
        
        d = "01EA"+x_str+th_str
        self.send485(d,8)
        

    

    def stop(self):
        ''' Stop both motors.
        '''
        self.drive(0, 0)

    def analog_read(self, pin):
        return self.execute('a %d' %pin)

    def analog_write(self, pin, value):
        return self.execute_ack('x %d %d' %(pin, value))

    def digital_read(self, pin):
        return self.execute('d %d' %pin)

    def digital_write(self, pin, value):
        return self.execute_ack('w %d %d' %(pin, value))

    def pin_mode(self, pin, mode):
        return self.execute_ack('c %d %d' %(pin, mode))

    def servo_write(self, id, pos):
        ''' Usage: servo_write(id, pos)
            Position is given in radians and converted to degrees before sending
        '''
        return self.execute_ack('s %d %d' %(id, min(SERVO_MAX, max(SERVO_MIN, degrees(pos)))))

    def servo_read(self, id):
        ''' Usage: servo_read(id)
            The returned position is converted from degrees to radians
        '''
        return radians(self.execute('t %d' %id))

    def ping(self, pin):
        ''' The srf05/Ping command queries an SRF05/Ping sonar sensor
            connected to the General Purpose I/O line pinId for a distance,
            and returns the range in cm.  Sonar distance resolution is integer based.
        '''
        return self.execute('p %d' %pin);

#    def get_maxez1(self, triggerPin, outputPin):
#        ''' The maxez1 command queries a Maxbotix MaxSonar-EZ1 sonar
#            sensor connected to the General Purpose I/O lines, triggerPin, and
#            outputPin, for a distance, and returns it in Centimeters. NOTE: MAKE
#            SURE there's nothing directly in front of the MaxSonar-EZ1 upon
#            power up, otherwise it wont range correctly for object less than 6
#            inches away! The sensor reading defaults to use English units
#            (inches). The sensor distance resolution is integer based. Also, the
#            maxsonar trigger pin is RX, and the echo pin is PW.
#        '''
#        return self.execute('z %d %d' %(triggerPin, outputPin))

    def PlatUp(self):
        print("PlatUp------------------")
        self.send485("110000000001", r_len=0)
    
    def PlatStop(self):
        print("PlatStop------------------")
        self.send485("110000000002", r_len=0)
    
    def PlatDown(self):
        print("PlatDown------------------")
        self.send485("110000000003", r_len=0)
    
    def ArmRightUp(self):
        print("ArmRightUp------------------")
        self.send485("110000000004", r_len=0)       
        
    def ArmRightStop(self):
        print("ArmRightStop------------------")
        self.send485("110000000005", r_len=0)  
        
    def ArmRightDown(self):
        print("ArmRightDown------------------")
        self.send485("110000000006", r_len=0)     
    
    def ArmLeftUp(self):
        print("ArmLeftUp------------------")
        self.send485("110000000007", r_len=0)       
        
    def ArmLeftStop(self):
        print("ArmLeftStop------------------")
        self.send485("110000000008", r_len=0)  
        
    def ArmLeftDown(self):
        print("ArmLeftDown------------------")
        self.send485("110000000009", r_len=0)    
    
    def GetUltrasonicStatus(self):
        result = self.send485("120000000001", r_len=6)
        print("result",result)
        return result[-1:]

table_crc_hi = (
        0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,
        0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
        0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
        0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
        0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1,
        0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,
        0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1,
        0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
        0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,
        0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40,
        0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1,
        0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
        0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,
        0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40,
        0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
        0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
        0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,
        0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
        0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
        0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
        0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
        0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40,
        0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1,
        0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
        0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,
        0x80, 0x41, 0x00, 0xC1, 0x81, 0x40)
    
table_crc_lo = (
        0x00, 0xC0, 0xC1, 0x01, 0xC3, 0x03, 0x02, 0xC2, 0xC6, 0x06,
        0x07, 0xC7, 0x05, 0xC5, 0xC4, 0x04, 0xCC, 0x0C, 0x0D, 0xCD,
        0x0F, 0xCF, 0xCE, 0x0E, 0x0A, 0xCA, 0xCB, 0x0B, 0xC9, 0x09,
        0x08, 0xC8, 0xD8, 0x18, 0x19, 0xD9, 0x1B, 0xDB, 0xDA, 0x1A,
        0x1E, 0xDE, 0xDF, 0x1F, 0xDD, 0x1D, 0x1C, 0xDC, 0x14, 0xD4,
        0xD5, 0x15, 0xD7, 0x17, 0x16, 0xD6, 0xD2, 0x12, 0x13, 0xD3,
        0x11, 0xD1, 0xD0, 0x10, 0xF0, 0x30, 0x31, 0xF1, 0x33, 0xF3,
        0xF2, 0x32, 0x36, 0xF6, 0xF7, 0x37, 0xF5, 0x35, 0x34, 0xF4,
        0x3C, 0xFC, 0xFD, 0x3D, 0xFF, 0x3F, 0x3E, 0xFE, 0xFA, 0x3A,
        0x3B, 0xFB, 0x39, 0xF9, 0xF8, 0x38, 0x28, 0xE8, 0xE9, 0x29,
        0xEB, 0x2B, 0x2A, 0xEA, 0xEE, 0x2E, 0x2F, 0xEF, 0x2D, 0xED,
        0xEC, 0x2C, 0xE4, 0x24, 0x25, 0xE5, 0x27, 0xE7, 0xE6, 0x26,
        0x22, 0xE2, 0xE3, 0x23, 0xE1, 0x21, 0x20, 0xE0, 0xA0, 0x60,
        0x61, 0xA1, 0x63, 0xA3, 0xA2, 0x62, 0x66, 0xA6, 0xA7, 0x67,
        0xA5, 0x65, 0x64, 0xA4, 0x6C, 0xAC, 0xAD, 0x6D, 0xAF, 0x6F,
        0x6E, 0xAE, 0xAA, 0x6A, 0x6B, 0xAB, 0x69, 0xA9, 0xA8, 0x68,
        0x78, 0xB8, 0xB9, 0x79, 0xBB, 0x7B, 0x7A, 0xBA, 0xBE, 0x7E,
        0x7F, 0xBF, 0x7D, 0xBD, 0xBC, 0x7C, 0xB4, 0x74, 0x75, 0xB5,
        0x77, 0xB7, 0xB6, 0x76, 0x72, 0xB2, 0xB3, 0x73, 0xB1, 0x71,
        0x70, 0xB0, 0x50, 0x90, 0x91, 0x51, 0x93, 0x53, 0x52, 0x92,
        0x96, 0x56, 0x57, 0x97, 0x55, 0x95, 0x94, 0x54, 0x9C, 0x5C,
        0x5D, 0x9D, 0x5F, 0x9F, 0x9E, 0x5E, 0x5A, 0x9A, 0x9B, 0x5B,
        0x99, 0x59, 0x58, 0x98, 0x88, 0x48, 0x49, 0x89, 0x4B, 0x8B,
        0x8A, 0x4A, 0x4E, 0x8E, 0x8F, 0x4F, 0x8D, 0x4D, 0x4C, 0x8C,
        0x44, 0x84, 0x85, 0x45, 0x87, 0x47, 0x46, 0x86, 0x82, 0x42,
        0x43, 0x83, 0x41, 0x81, 0x80, 0x40)
    
    
def crc16(st):
    crc_hi = crc_lo = 0xFF
    L = []
    #st = st.strip().replace(' ', '')
    if len(st) % 2:
        return None
    for j in range(0, len(st), 2):
        L.append(st[j:(j + 2)])
    i = 0
    for ch in L:
        ch = int(ch, 16)
        i = crc_hi ^ ch
        crc_hi = crc_lo ^ table_crc_hi[i]
        crc_lo = table_crc_lo[i]
    result = hex(crc_hi << 8 | crc_lo)
    addition = 6 - len(result)
    if addition > 0:
        result = result.replace('x', 'x' + '0' * addition)
    return result[2:]


""" Basic test for connectivity """
if __name__ == "__main__":
    if os.name == "posix":
        portName = "/dev/Serial0"
    else:
        portName = "COM43" # Windows style COM port.

    baudRate = 19200
    #baudRate = 115200

    myArduino = Arduino485(port=portName, baudrate=baudRate, timeout=0.5)
    myArduino.connect()

    print ("Sleeping for 1 second...")
    time.sleep(1)

    #print ("Reading on analog port 0", myArduino.analog_read(0))
    #print ("Reading on digital port 0", myArduino.digital_read(0))
    #print ("Blinking the LED 3 times")
    #for i in range(3):
    #    myArduino.digital_write(13, 1)
    #    time.sleep(1.0)
    #print "Current encoder counts", myArduino.encoders()

    print ("Connection test successful.",)
    #myArduino.send485(act_disable)
    myArduino.stop()
    myArduino.close()

    print ("Shutting down Arduino.")



