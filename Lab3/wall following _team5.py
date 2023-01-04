#! /usr/bin/env python

# import ros stuff
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations
import numpy as np
import csv
import matplotlib.pyplot as plt

import math
pub_ = None
regions_ = {
    'right': 0,
    'front': 0,
    'left': 0,
}
robo_sta=0
state_ = 0
state_dict_ = {
    0:'find the wall',
    1:'turn left',
    2:'turn right',
    3:'back',
    4:'follow the wall',
    
}

def callback_laser(msg):
    
    global regions_
    regions_ = {
        'front': min(min(msg.ranges[0:20]),min(msg.ranges[340:360])),
    
        'right': min(msg.ranges[270:300]),
        'left': min(msg.ranges[70:90]),
    }
    plot_laser(msg.ranges, x, y, theta)
    take_action()
   



#def state_robot():
    
def change_state(state):
    global d
    if state==1:
        regions_['right']==d+0.1
        robo_sta=1 #following right wall
    elif state==2:
        regions_['left']==d+0.1
        robo_state=2 #following left wall
    elif state==4 and robo_sta==1:
        regions_['right']==d+0.1
        robo_sta=1
    elif state==4 and robo_sta==2:
        regions_['left']==d+0.1
        robo_sta=2
    global state_, state_dict_
    if state is not state_:
        print ('Wall follower - [%s] - %s' % (state, state_dict_[state]))
        state_ = state
def take_action():
    global regions_
    regions = regions_
    
    msg = Twist()
    linear_x = 0
    angular_z = 0
    
    state_description = ''
    global d
    d =0.5
    #if regions['fleft']=='inf' and regions['left']=='inf' and regions['right']=='inf' and regions['fright']=='inf' and regions['front']=='inf':
        #pass
    if regions['front'] > d: #and regions['fleft'] > d and regions['fright'] > d:
        state_description = 'case 1 - nothing'
        change_state(0)
    elif regions['front'] < d and regions['left'] > d and regions['right'] > d:
        state_description = 'case 2 - front'
        change_state(1)
    elif regions['front'] > d and regions['left'] > d and regions['right'] < d:
        state_description = 'case 3 - fright'
        change_state(4)
    elif regions['front'] > d and regions['left'] < d and regions['right'] > d:
        state_description = 'case 4 - fleft'
        change_state(4)
    elif regions['front'] < d and regions['left'] > d and regions['right'] < d:
        state_description = 'case 5 - front and fright'
        change_state(1)
    elif regions['front'] < d and regions['left'] < d and regions['right'] > d:
        state_description = 'case 6 - front and fleft'
        change_state(2)
    elif regions['front'] < d and regions['left'] < d and regions['right'] < d:
        state_description = 'case 7 - front and fleft and fright'
        change_state(3)
    elif regions['front'] > d and regions['left'] < d and regions['right'] < d:
        state_description = 'case 8 - fleft and fright'
        change_state(4)
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)


def plot_laser(ranges, x, y, theta):
    # Clear the current figure
    plt.clf()

    # Create a subplot
    ax = plt.subplot()

    # Set the title and labels
    ax.set_title('Laser scan')
    ax.set_xlabel('X position (m)')
    ax.set_ylabel('Y position (m)')

    # Set the limits of the plot
    ax.set_xlim(-10,10)
    ax.set_ylim(-10, 10)

    # Plot the robot's position as a point
    ax.plot(x, y, color='red', marker='o', markersize=12)

    # Plot the ranges as a line plot
    ax.plot(x + ranges * np.cos(theta + np.radians(range(360))),
            y + ranges * np.sin(theta + np.radians(range(360))),
            color='blue', linewidth=1, zorder=1)
    ax.set_autoscale_on(False)
 

    # Draw the plot
    plt.draw()
    plt.pause(0.001)





def find_wall():
    
    msg = Twist()
    msg.linear.x = 0.1
    msg.angular.z = -0.1
    return msg
def turn_left():
    msg = Twist()
    msg.linear.x=0.2
    msg.angular.z = 0.6
    return msg

def turn_right():
    msg = Twist()
    msg.linear.x=0.2
    msg.angular.z = -0.2
    return msg
def back():
    msg=Twist()
    msg.linear.x=-0.2
    msg.angular.z=0.1
    return msg
def follow_the_wall():
    global regions_
    
    msg = Twist()
    msg.linear.x = 0.3
    return msg

def main():
    global x, y, theta

# Define the variables
    x = 0
    y = 0
    theta = 0
    global pub_
    
    rospy.init_node('reading_laser')
    
    pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    sub = rospy.Subscriber('/scan', LaserScan, callback_laser, queue_size=1)
    
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
       
        msg = Twist()
        #print("1")
        if state_ == 0:
            msg = find_wall()
           # print("2")
        elif state_ == 1:
            msg = turn_left()
        elif state_ ==2:
        	msg=turn_right()
        elif state_ == 3:
            msg = back()
        elif state_ ==4:
            msg= follow_the_wall()
            pass
        else:
            rospy.logerr('Unknown state!')
        
        pub_.publish(msg)
        
        rate.sleep()

if __name__ == '__main__':
    main()
