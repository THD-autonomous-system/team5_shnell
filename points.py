#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
import numpy as np
import csv
import matplotlib.pyplot as plt
#import pandas as pd

def callback(msg):
    # n=open ("coordinates.csv",'w') 
    # z= csv.writer(n,delimiter=',')
    list=msg.ranges
    n=[]
    m=[]
    
    for i in range(0,360):
        if list[i]=='inf':
            pass
        else:
            
            x=list[i]*np.cos(i*(2*np.pi)/360)
            n.append(x)
            y=list[i]*np.sin(i*(2*np.pi)/360)
            m.append(y)
    #z.writerow([x,y])
    # n.close()
    # df = pd.read_csv('coordinates.csv')
    # print(df.head())

    # x = df[0]
    # y = df[1]
    plt.clf()
        
    #plt.plot(0,0,c='g',alpha=1, marker=MarkerStyle('1','left',t),**common_style,markersize=24)
    #plt.plot(n,m, 'go--', linewidth=2, markersize=12)
    plt.plot(0,0, color='green', marker='>', linestyle='dashed',linewidth=2, markersize=12)
    
    plt.scatter(n,m)
    plt.title('Graph ploting')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.pause(0.01)
    plt.show


    
rospy.init_node('scan_values')
sub = rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()
