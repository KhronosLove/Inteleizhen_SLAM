#!/usr/bin/env python3
#import roslib; roslib.load_manifest('ros_arduino_python')
import rospy
import os
import actionlib
from actionlib_msgs.msg import *
from math import sin, cos, pi,pow,sqrt
from move_base_msgs.msg import MoveBaseGoal,MoveBaseAction
from geometry_msgs.msg import Quaternion, Twist, Pose,Point,PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from tf.broadcaster import TransformBroadcaster
import serial 
import time
from random import sample
from arduino_driver_485 import Arduino485
import struct,binascii
from std_srvs.srv import Empty
from std_msgs.msg import String

""" Class to receive Twist commands and publish Odometry data """
class NavTest:
    def __init__(self):
        self.pub = rospy.Publisher("chatter",String,queue_size=10)
        rospy.init_node('nav_test',anonymous=True)
        rospy.on_shutdown(self.shutdown)
        #rospy.wait_for_service('global_localization')
        #rospy.ServiceProxy('global_localization', Empty)()
        
        #for i in range(2000):
        #    rospy.ServiceProxy('request_nomotion_update', Empty)()
            #rospy.sleep(0.5)
        #    if i % 50 ==0:
        #        rospy.ServiceProxy('move_base/clear_costmaps', Empty)()
        #    print(i)
        
        #rospy.ServiceProxy('move_base/clear_costmaps', Empty)()
        
        #rospy.sleep(100)
        
        
        
        
        self.rest_time = 5
        self.start_nav = False
        
        
     
     
    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose
    
    
    def action(self):
        self.start_nav = True
        
        goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED','SUCCEEDED',
                       'ABORTED', 'REJECTED','PREEMPTING', 'RECALLING', 
                       'RECALLED','LOST']
        
        locations = dict()
        locations[0] = Pose(Point(0.109, 0.01, 0.000),Quaternion(0.000, 0.000, 0.09, 0.995))
        #locations[1] = Pose(Point(0.597, 0.452, 0.000),Quaternion(0.000, 0.000, 0.723, 0.69))
        locations[1] = Pose(Point(1.25, 0.02, 0.000),Quaternion(0.000, 0.000, -0.631, 0.77))
        locations[2] = Pose(Point(1.75, -2.75, 0.000),Quaternion(0.000, 0.000, -0.643, 0.765))
        locations[3] = Pose(Point(1.75, -2.75, 0.000),Quaternion(0.000, 0.000, 0.766, 0.642))
        locations[4] = Pose(Point(1.25, -0.32, 0.000),Quaternion(0.000, 0.000, 0.766, 0.642))
        #locations[5] = Pose(Point(1.1, 0.000, 0.000),Quaternion(0.000, 0.000, 0.500, 0.500))        
        #locations[6] = Pose(Point(1.1, 0.000, 0.000),Quaternion(0.000, 0.000, 1.000, 0.000))
                
        #locations[3] = Pose(Point(0.08, 0.219, 0.000),Quaternion(0.000, 0.000, 0.855, 0.517))

        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
         
        # Wait 60 seconds for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(600))
        rospy.loginfo("Connected to move base server")
                
        # A variable to hold the initial pose of the robot to be set by the user in RViz
        initial_pose = PoseWithCovarianceStamped()
      
        n_locations = len(locations)
        
        n_goals = 0
        n_successes = 0
        i = n_locations
        distance_traveled = 0
        start_time = rospy.Time.now()
        running_time = 0
        location = ""
        last_location = ""
        # Get the initial pose from the user
        #rospy.loginfo("Click on the map in RViz to set the intial pose...")
        #rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)
        self.last_location = Pose()
        #rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)
        # Make sure we have the initial pose
        while initial_pose.header.stamp == "":
            rospy.sleep(1)
        rospy.loginfo("Starting navigation test")
        
        # Begin the main loop and run through a sequence of locations
        while not rospy.is_shutdown() and self.start_nav:
            rospy.ServiceProxy('move_base/clear_costmaps', Empty)()
        # If we've gone through the current sequence, start with a new random sequence
            if i == n_locations:
                i = 0
                #sequence = sample(locations, n_locations)
                sequence = sorted(locations)
                # Skip over first location if it is the same as the last location
                if sequence[0] == last_location:
                    i = 1
    
            # Get the next location in the current sequence
            location = sequence[i]
    
            # Keep track of the distance traveled.
            # Use updated initial pose if available.
            if initial_pose.header.stamp == "":
                distance = sqrt(pow(locations[location].position.x
                                        - locations[last_location].position.x, 2) +
                                    pow(locations[location].position.y -
                                   locations[last_location].position.y, 2))
            else:
                rospy.loginfo("Updating current pose.")
                distance = sqrt(pow(locations[location].position.x
                                        - initial_pose.pose.pose.position.x, 2) +
                                    pow(locations[location].position.y -
                                   initial_pose.pose.pose.position.y, 2))
                initial_pose.header.stamp = ""
    
            # Store the last location for distance calculations
            last_location = location
    
            # Increment the counters
            n_goals += 1
    
            # Set up the next goal location
            self.goal = MoveBaseGoal()
            self.goal.target_pose.pose = locations[location]
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()
    
            # Let the user know where the robot is going next
            rospy.loginfo("Going to: " + str(location))
            # Start the robot toward the next location
            self.move_base.send_goal(self.goal)
    
            # Allow 5 minutes to get there
            finished_within_time = self.move_base.wait_for_result(rospy.Duration(1200))
    
            # Check for success or failure
            if not finished_within_time:
                self.move_base.cancel_goal()
                rospy.loginfo("Timed out achieving goal")
            else:
                state = self.move_base.get_state()
                if state == GoalStatus.SUCCEEDED:
                    i += 1
                    
                    
                    rospy.loginfo("Goal succeeded!")
                    n_successes += 1
                    distance_traveled += distance
                    if location == 1:
                        self.platUp()
                        self.armUp()
                    elif location == 2:        
                        self.armDown()
                        self.platDown()
                elif state == GoalStatus.ABORTED:
                    rospy.loginfo("Goal failed with error code: " + str(goal_states[state]))
                    self.move_base.send_goal(self.goal)                    
                else:
                    rospy.loginfo("Goal failed with error code: " + str(goal_states[state]))
                   
    
            # How long have we been running?
            running_time = rospy.Time.now() - start_time
            running_time = running_time.secs / 60.0
    
            # Print a summary success/failure, distance traveled and time elapsed
            rospy.loginfo("Success so far: " + str(n_successes) + "/" +
                              str(n_goals) + " = " + str(100 * n_successes/n_goals) + "%")
            rospy.loginfo("Running time: " + str(trunc(running_time, 1)) +
                              " min Distance: " + str(trunc(distance_traveled, 1)) + " m")
            time.sleep(self.rest_time)        
    
    def shutdown(self):
        self.start_nav = False
        rospy.loginfo("Stopping the robot...")
        self.move_base.cancel_goal()
        rospy.sleep(2)
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)
        
    def platUp(self):
        self.pub.publish("SetFlagFalse")
        self.pub.publish("PlatUp")
        time.sleep(13)
        self.pub.publish("PlatStop")
        time.sleep(2)
    
    def platDown(self):
        self.pub.publish("PlatDown")
        rospy.sleep(13)
        self.pub.publish("PlatStop")
        rospy.sleep(2)
        self.pub.publish("SetFlagTrue")
        
    def armUp(self):
        self.pub.publish("ArmRightUp")
        time.sleep(2)
        self.pub.publish("ArmLeftUp")
        time.sleep(65)
        self.pub.publish("ArmRightStop")
        time.sleep(2)
        self.pub.publish("ArmLeftStop")
        time.sleep(2)
         
        
    def armDown(self):
        self.pub.publish("ArmRightDown")
        time.sleep(2)
        self.pub.publish("ArmLeftDown")
        time.sleep(65)
        self.pub.publish("ArmRightStop")
        time.sleep(2)
        self.pub.publish("ArmLeftStop")
        time.sleep(2)

         

def trunc(f, n):

    # Truncates/pads a float f to n decimal places without rounding
    slen = len('%.*f' % (n, f))
    return float(str(f)[:slen])

if __name__ == '__main__':
    try:
        nav = NavTest()
        nav.action()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("AMCL navigation test finished.")
