#!/usr/bin/env python3

"""
    A base controller class for the Arduino microcontroller
    
    Borrowed heavily from Mike Feguson's ArbotiX base_controller.py code.
    
    Created for the Pi Robot Project: http://www.pirobot.org
    Copyright (c) 2010 Patrick Goebel.  All rights reserved.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details at:
    
    http://www.gnu.org/licenses
"""
#import roslib; roslib.load_manifest('ros_arduino_python')
import rospy
import os

from math import sin, cos, pi
from geometry_msgs.msg import Quaternion, Twist, Pose
from nav_msgs.msg import Odometry
from tf.broadcaster import TransformBroadcaster
import serial
import time
from ros_arduino_python.arduino_driver_485 import *
import struct,binascii
from std_msgs.msg import String
import sensor_msgs.msg

ODOM_POSE_COVARIANCE = [1e-3, 0, 0, 0, 0, 0, 
                        0, 1e-3, 0, 0, 0, 0,
                        0, 0, 1e6, 0, 0, 0,
                        0, 0, 0, 1e6, 0, 0,
                        0, 0, 0, 0, 1e6, 0,
                        0, 0, 0, 0, 0, 1e3]
ODOM_POSE_COVARIANCE2 = [1e-9, 0, 0, 0, 0, 0, 
                         0, 1e-3, 1e-9, 0, 0, 0,
                         0, 0, 1e6, 0, 0, 0,
                         0, 0, 0, 1e6, 0, 0,
                         0, 0, 0, 0, 1e6, 0,
                         0, 0, 0, 0, 0, 1e-9]

ODOM_TWIST_COVARIANCE = [1e-3, 0, 0, 0, 0, 0, 
                         0, 1e-3, 0, 0, 0, 0,
                         0, 0, 1e6, 0, 0, 0,
                         0, 0, 0, 1e6, 0, 0,
                         0, 0, 0, 0, 1e6, 0,
                         0, 0, 0, 0, 0, 1e3]
ODOM_TWIST_COVARIANCE2 = [1e-9, 0, 0, 0, 0, 0, 
                          0, 1e-3, 1e-9, 0, 0, 0,
                          0, 0, 1e6, 0, 0, 0,
                          0, 0, 0, 1e6, 0, 0,
                          0, 0, 0, 0, 1e6, 0,
                          0, 0, 0, 0, 0, 1e-9]

""" Class to receive Twist commands and publish Odometry data """
class BaseController:
    def __init__(self,controller, base_frame, name="base_controllers"):
        
        self.controller = controller
        return_data = self.controller.send485(act_enable)

        #self.arduino = arduino
        self.name = name
        self.base_frame = base_frame
        self.rate = float(rospy.get_param("~base_controller_rate", 10))
        self.timeout = rospy.get_param("~base_controller_timeout",1)
        self.stopped = False
                 
        pid_params = dict()
        pid_params['wheel_diameter'] = rospy.get_param("~wheel_diameter", 0.18)
        pid_params['wheel_track'] = rospy.get_param("~wheel_track", 0.38)
        pid_params['encoder_resolution'] = rospy.get_param("~encoder_resolution", 5600) 
        pid_params['gear_reduction'] = rospy.get_param("~gear_reduction", 1.0)
        pid_params['Kp'] = rospy.get_param("~Kp", 20)
        pid_params['Kd'] = rospy.get_param("~Kd", 12)
        pid_params['Ki'] = rospy.get_param("~Ki", 0)
        pid_params['Ko'] = rospy.get_param("~Ko", 50)
        
        self.accel_limit = rospy.get_param('~accel_limit', 0.1)
        self.motors_reversed = rospy.get_param("~motors_reversed", False)
        
        # Set up PID parameters and check for missing values
        self.setup_pid(pid_params)
            
        # How many encoder ticks are there per meter?
        self.ticks_per_meter = self.encoder_resolution * self.gear_reduction  / (self.wheel_diameter * pi)
        
        # What is the maximum acceleration we will tolerate when changing wheel speeds?
        self.max_accel = self.accel_limit * self.ticks_per_meter / self.rate
        
        print("self.max_accel",self.max_accel)
        # Track how often we get a bad encoder count (if any)
        self.bad_encoder_count = 0
                        
        now = rospy.Time.now()    
        self.then = now # time for determining dx/dy
        self.t_delta = rospy.Duration(1.0 / self.rate)
        self.t_next = now + self.t_delta

        # Internal data        
        self.enc_left = None            # encoderleft readings
        self.enc_right = None
        self.x = 0                      # position in xy plane
        self.y = 0
        self.th = 0                     # rotation in radians
        self.v_left = 0
        self.v_right = 0
        self.v_des_left = 0             # cmd_vel setpoint
        self.v_des_right = 0
        self.last_cmd_vel = now
        
        self.des_x = 0
        self.des_th = 0
        
        # Subscriptions
        rospy.Subscriber("cmd_vel", Twist, self.cmdVelCallback)
        
        # Clear any old odometry info
        #self.controller.reset_encoders()
               
        # Set up the odometry broadcaster
        self.odomPub = rospy.Publisher('odom', Odometry, queue_size=5)
        self.odomBroadcaster = TransformBroadcaster()
        
        rospy.loginfo("Started base controller for a base of " + str(self.wheel_track) + "m wide with " + str(self.encoder_resolution) + " ticks per rev")
        rospy.loginfo("Publishing odometry datlefta at: " + str(self.rate) + " Hz using " + str(self.base_frame) + " as base frame")
        
        rospy.Subscriber("chatter",String,self.cmdWorkCallback)

        
    def setup_pid(self, pid_params):
        # Check to see if any PID parameters are missing
        missing_params = False
        for param in pid_params:
            if pid_params[param] == "":
                print("*** PID Parameter " + param + " is missing. ***")
                missing_params = True
        
        if missing_params:
            os._exit(1)
                
        self.wheel_diameter = pid_params['wheel_diameter']
        self.wheel_track = pid_params['wheel_track']
        self.encoder_resolution = pid_params['encoder_resolution']
        self.gear_reduction = pid_params['gear_reduction']
        
        self.Kp = pid_params['Kp']
        self.Kd = pid_params['Kd']
        self.Ki = pid_params['Ki']
        self.Ko = pid_params['Ko']
        
        #self.arduino.update_pid(self.Kp, self.Kd, self.Ki, self.Ko)
    
    
    def hex_to_int(self,speed_hex):
        speed=0
        if speed_hex[:2]=="ff":
            speed =struct.unpack("i", binascii.unhexlify(speed_hex[::-1]+"ffff"))[0]
        elif speed_hex[:2]=="00":
            speed = struct.unpack("i",binascii.unhexlify(speed_hex[::-1]+"0000"))[0]
        return speed
    
    def poll(self):   
        
        now = rospy.Time.now()
        if now > self.t_next:
            # Read the encoders
            
            try:
                #left_enc, right_enc = 0 ,0
                left_enc, right_enc = self.controller.get_encoder_counts()
                #print("left_enc",left_enc,"right_enc",right_enc)
            except:
                self.bad_encoder_count += 1
                rospy.logerr("Encoder exception count: " + str(self.bad_encoder_count))
                return

            
            
            dt = now - self.then
            self.then = now
            dt = dt.to_sec()
            
            # Calculate odometry
            if self.enc_left == None:
                dright = 0
                dleft = 0
            else:
                dright = (right_enc - self.enc_right) / self.ticks_per_meter
                dleft = (left_enc - self.enc_left) / self.ticks_per_meter
            '''
            try:
                d= "014350005100"
                speed_data = self.controller.send485(d)
                speed_left = self.hex_to_int(speed_data[12:16])
                speed_left = -speed_left
                speed_right = self.hex_to_int(speed_data[16:20])
                if self.motors_reversed:
                    speed_left,speed_right = -speed_left,-speed_right
                
                dright = speed_right/1000 *dt
                dleft = speed_left/1000 *dt
                
            except:
                self.bad_encoder_count += 1
                rospy.logerr("Get Speed exception count: " + str(self.bad_encoder_count))
                return            
            '''
            
            self.enc_right = right_enc
            self.enc_left = left_enc
            
            dxy_ave = (dright + dleft) / 2.0
            dth = (dright - dleft) / self.wheel_track
            vxy = dxy_ave / dt
            vth = dth / dt
                        
            if (dxy_ave != 0):
                dx = cos(dth) * dxy_ave
                dy = -sin(dth) * dxy_ave
                self.x += (cos(self.th) * dx - sin(self.th) * dy)
                self.y += (sin(self.th) * dx + cos(self.th) * dy)
    
            if (dth != 0):
                self.th += dth 
            
            
            #print("self.x",self.x,"self.y",self.y)
            
            quaternion = Quaternion()
            quaternion.x = 0.0 
            quaternion.y = 0.0
            quaternion.z = sin(self.th / 2.0)
            quaternion.w = cos(self.th / 2.0)
    
            # Create the odometry transform frame broadcaster.
            #self.odomBroadcaster.sendTransform(
            #    (self.x, self.y, 0), 
            #    (quaternion.x, quaternion.y, quaternion.z, quaternion.w),
            #    rospy.Time.now(),
            #    self.base_frame,
            #    "odom_w"
            #    )
    
            odom = Odometry()
            odom.header.frame_id = "odom_combined"
            odom.child_frame_id = self.base_frame
            odom.header.stamp = now
            odom.pose.pose.position.x = self.x
            odom.pose.pose.position.y = self.y
            odom.pose.pose.position.z = 0
            odom.pose.pose.orientation = quaternion
            odom.twist.twist.linear.x = vxy
            odom.twist.twist.linear.y = 0
            odom.twist.twist.angular.z = vth
            
            if dxy_ave == 0:
                odom.pose.covariance = ODOM_POSE_COVARIANCE2
                odom.twist.covariance = ODOM_TWIST_COVARIANCE2
            else:
                odom.pose.covariance = ODOM_POSE_COVARIANCE
                odom.twist.covariance = ODOM_TWIST_COVARIANCE
	    
            self.odomPub.publish(odom)
            
            
            #if now > (self.last_cmd_vel + rospy.Duration(0.1)) and speed_left!=0 and speed_right!=0:
                #self.controller.drive485(0, 0)
            
            
            
            if now > (self.last_cmd_vel + rospy.Duration(self.timeout)):

                self.v_des_left = 0
                self.v_des_right = 0
            
            
            
            #print("left_enc",self.enc_left,"enc_right",self.enc_right,"v_left",self.v_left,"v_right",self.v_right,"v_des_left",self.v_des_left,"v_des_right",self.v_des_right)
                        
            if self.v_left < self.v_des_left:
                self.v_left += self.max_accel
                if self.v_left > self.v_des_left:
                    self.v_left = self.v_des_left
            else:
                self.v_left -= self.max_accel
                if self.v_left < self.v_des_left:
                    self.v_left = self.v_des_left
            
            if self.v_right < self.v_des_right:
                self.v_right += self.max_accel
                if self.v_right > self.v_des_right:
                    self.v_right = self.v_des_right
            else:
                self.v_right -= self.max_accel
                if self.v_right < self.v_des_right:
                    self.v_right = self.v_des_right
            
            # Set motor speeds in encoder ticks per PID loop
            if not self.stopped:
                #d = "01EA"+hex(int(self.x))[2:]+"00"+hex(int(vth))[2:]+"00"
                #self.controller.send485(d,8)
                #if self.v_left>0 or self.v_right>0:
                    
                
                #self.controller.drive485(10,0)
                #self.controller.drive(0,0)   
                #print("v_left",self.v_left,"v_right",self.v_right)
                self.controller.drive(self.v_left,self.v_right)
            
            
            self.t_next = now + self.t_delta
            
    def stop(self):
        self.stopped = True
        self.controller.drive485(0, 0)
            
    def cmdVelCallback(self, req):
        # Handle velocity-based movement requests
        self.last_cmd_vel = rospy.Time.now()
        #try:
        #    rospy.ServiceProxy('move_base/clear_costmaps', Empty)()
        #except:
        #    pass
        
        x = req.linear.x         # m/s
        th = req.angular.z       # rad/s
         
        #try:
        #    ustatus = self.controller.GetUltrasonicStatus()
        #    print("ustatus",ustatus)
        #    if ustatus=="1":
        #        x=0.0
        #        th=0.0
        #except:
        #    rospy.logerr("Ustatus exception")          
        
        
        #print("x",x,"th",th)
        
        #self.des_x = x
        #self.des_th = th

        #
        
        if x == 0:
            # Turn in place
            right = th * self.wheel_track  * self.gear_reduction / 2.0
            left = -right
        elif th == 0:
            # Pure forward/backward motion
            left = right = x
        else:
            # Rotation about a point in space
            left = x - th * self.wheel_track  * self.gear_reduction / 2.0
            right = x + th * self.wheel_track  * self.gear_reduction / 2.0
        
        self.v_des_left = int(left * self.ticks_per_meter / 240)
        self.v_des_right = int(right * self.ticks_per_meter / 240)
        #print("x",x,"th",th,"left",left,"right",right,"v_des_left",self.v_des_left,"v_des_right",self.v_des_right)
        
    def cmdWorkCallback(self,data):
        #rospy.loginfo(rospy.get_caller_id() + "I heard %s",data.data)  
        
        if data.data=="PlatUp":
            self.controller.PlatUp()
        elif data.data=="PlatStop":
            self.controller.PlatStop()
        elif data.data=="PlatDown":
            self.controller.PlatDown()    
        elif data.data=="ArmRightUp":
            self.controller.ArmRightUp()
        elif data.data=="ArmRightStop":
            self.controller.ArmRightStop()
        elif data.data=="ArmRightDown":
            self.controller.ArmRightDown()   
        elif data.data=="ArmLeftUp":
            self.controller.ArmLeftUp()
        elif data.data=="ArmLeftStop":
            self.controller.ArmLeftStop()
        elif data.data=="ArmLeftDown":
            self.controller.ArmLeftDown() 
      
            

    
