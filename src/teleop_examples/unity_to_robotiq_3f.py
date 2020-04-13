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
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from sensor_msgs.msg import JointState
# from geometry_msgs.msg import PoseStamped


clk = 0.008
scale_factor_pos = 625

def UnityToRobotiq3f():
	# initialize node
	rospy.init_node('UnityToRobotiq3f', anonymous=True)
	# setup joint_traj_relay topic subscription
	joint_traj_subscriber = rospy.Subscriber("joint_traj_relay", JointState, handleJointTrajMsg, queue_size=10)
	
	rospy.loginfo('Success')
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()

	
def handleJointTrajMsg(data):
	#### Initialize Speed Parameter
	#   axes  [l.x   l.y   l.z   a.x     a.y    a.z]
	# scalers = [0.7,  0.7,  0.7,  -3.14, -3.14, -3.14]	

	joint_traj_publisher = rospy.Publisher("robotiq_3f_controller/command", JointTrajectory)
	#### Setup JointTraj Publisher 
	JointTraj = JointTrajectory()
	JointTrajPoints = JointTrajectoryPoint()
	#### Start Mapping from PoseStamped to JointTraj
	JointTraj.header.stamp = rospy.get_rostime()
	JointTraj.joint_names = ['finger_1_joint_1','finger_1_joint_2','finger_1_joint_3','finger_2_joint_1','finger_2_joint_2','finger_2_joint_3','finger_middle_joint_1','finger_middle_joint_2','finger_middle_joint_3','palm_finger_1_joint','palm_finger_2_joint']
	# data size is 30
	JointTrajPoints.positions = data.position
	JointTrajPoints.velocities = data.velocity
	JointTrajPoints.accelerations = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	JointTrajPoints.effort = [0]  
	JointTrajPoints.time_from_start = rospy.Duration.from_sec(0.1)

	JointTraj.points.append(JointTrajPoints)
	# JointTraj.JointTraj.linear.x=data.pose.position.y*clk*scale_factor_pos*-1
	# JointTraj.JointTraj.linear.y=data.pose.position.z*clk*scale_factor_pos
	# JointTraj.JointTraj.linear.z=data.pose.position.x*clk*scale_factor_pos

	# JointTraj.JointTraj.angular.x=data.pose.orientation.x
	# JointTraj.JointTraj.angular.y=data.pose.orientation.y
	# JointTraj.JointTraj.angular.z=data.pose.orientation.z


	#### Publish msg
	rate = rospy.Rate(100) # 100hz
	rospy.loginfo(data)
	joint_traj_publisher.publish(JointTraj)
	rate.sleep()

if __name__ == '__main__':
	UnityToRobotiq3f()
