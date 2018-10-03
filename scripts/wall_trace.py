#!/usr/bin/env python

#motors.py
#Copyright (c) 2016 Ryuichi Ueda <ryuichiueda@gmail.com>
#This software is released under the MIT License.
#http://opensource.org/licenses/mit-license.php

import rospy,copy,math
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
from pimouse_ros.msg import LightSensorValues

class WallTrace():
    def __init__(self):
        self.cmd_vel = rospy.Publisher('/cmd_vel',Twist,queue_size=1)

        self.sensor_values = LightSensorValues()
        rospy.Subscriber('/lightsensors', LightSensorValues, self.callback_lightsensors)

    def callback_lightsensors(self,messages):
        self.sensor_values = messages

    def run(self):
        rate = rospy.Rate(20)
        data = Twist()

        accel = 0.01
        decel = 0.1
        data.linear.x = 0.0
        data.angular.z = 0
        while not rospy.is_shutdown():
            s = self.sensor_values
            data.linear.x += accel

            if self.sensor_values.sum_forward >= 50:
                #data.linear.x = 0
                rate = rospy.Rate(20)
                while data.linear.x > 0:
                    data.linear.x -= decel
                    if data.linear.x < 0.2:
                        data.linear.x = 0
                    print(data.linear.x)
                    self.cmd_vel.publish(data)
                    rate.sleep()
                rate = rospy.Rate(10)
                    
            elif data.linear.x <= 0.2:
                data.linear.x = 0.2
            elif data.linear.x >= 0.8:
                data.linear.x = 0.8

            if data.linear.x < 0.2:
                data.angular.z = 0.0
            elif s.left_side < 10:
                data.angular.z = 0.0
            else:
                target = 50
                error = (target - s.left_side)/50.0
                data.angular.z = error * 100 * math.pi / 180.0
                
            print(data.linear.x)
            self.cmd_vel.publish(data)
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('wall_trace')

    rospy.wait_for_service('/motor_on')
    rospy.wait_for_service('/motor_off')
    rospy.on_shutdown(rospy.ServiceProxy('/motor_off',Trigger).call)
    rospy.ServiceProxy('/motor_on',Trigger).call()

    w = WallTrace()
    w.run()
