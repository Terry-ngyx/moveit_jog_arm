#!/usr/bin/env python

# Siemens AG, 2018
# Author: Berkay Alp Cakal (berkay_alp.cakal.ct@siemens.com)
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# <http://www.apache.org/licenses/LICENSE-2.0>.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rospy
import numpy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import TwistStamped

clk = 0.008
scale_factor_pos = 625

def UnityToTwist():
	# initialize node
	rospy.init_node('UnityToTwist', anonymous=True)
	# setup joy topic subscription
	joy_subscriber = rospy.Subscriber("odom", PoseStamped, handlePoseMsg, queue_size=10)
	

	rospy.loginfo('Success')
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()

	
def handlePoseMsg(data):
	#### Initialize Speed Parameter
	#   axes  [l.x   l.y   l.z   a.x     a.y    a.z]
	# scalers = [0.7,  0.7,  0.7,  -3.14, -3.14, -3.14]	
	
	twist_publisher = rospy.Publisher("jog_server/delta_jog_cmds", TwistStamped)
	#### Setup Twist Publisher 
	twist = TwistStamped()

	#### Start Mapping from PoseStamped to Twist
	twist.header.stamp = rospy.get_rostime()

	# twist.twist.linear.x=data.pose.position.y*clk*scale_factor_pos*-1
	# twist.twist.linear.y=data.pose.position.z*clk*scale_factor_pos
	# twist.twist.linear.z=data.pose.position.x*clk*scale_factor_pos

	twist.twist.linear.x=data.pose.position.x
	twist.twist.linear.y=data.pose.position.y
	twist.twist.linear.z=data.pose.position.z

	twist.twist.angular.x=data.pose.orientation.x
	twist.twist.angular.y=data.pose.orientation.y
	twist.twist.angular.z=data.pose.orientation.z

	#### Publish msg
	rate = rospy.Rate(100) # 100hz
	rospy.loginfo(twist)
	twist_publisher.publish(twist)
	rate.sleep()

if __name__ == '__main__':
	UnityToTwist()