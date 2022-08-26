#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

first_x = 0
first_y = 0
first_yaw = 0

#  subscriber
def pose_callback(pose: Pose):
    global first_x , first_y , first_yaw
    first_x = pose.x
    first_y = pose.y
    first_yaw = pose.theta
    
# publisher  
def GO_TO (targa_x,targa_y):
    global first_x , first_y , first_yaw
    vel_msg = Twist()
    
    while True :
        dis_ans= math.sqrt( (targa_x - first_x)**2 +(targa_y - first_y) **2)
        
        # beta_vel = 0.6 we multiply this param for tuning the speed.
        beta_vel = rospy.get_param("/beta_move")
        vel_msg.linear.x = dis_ans * beta_vel
        
        # beta_angular = 5.0.
        beta_angular = rospy.get_param("/phi_move")
        
        dis_angular = math.atan2( (targa_y - first_y) , (targa_x - first_x))
        
        # we multiply for enlarging because the angle is on radian so it is very small.
        vel_msg.angular.z = (dis_angular - first_yaw) * (beta_angular)
        
        # we will publish the velocity message.
        pub.publish(vel_msg)
        if dis_ans <= 0.01 :
            break
              
if __name__ == '__main__':
    rospy.init_node("HELLO")
    pub = rospy.Publisher("/turtle1/cmd_vel",Twist, queue_size=10)
    sub = rospy.Subscriber("/turtle1/pose",Pose, callback=pose_callback)
    # to take from the user inputs.
    
    """
    while True  :
       # user_inter_x = float(input("Please enter the x value"))
       # user_inter_y = float(input("Please enter the y value"))
        user_inter_x = rospy.get_param("/x_move")
        user_inter_y = rospy.get_param("/y_move")
        
        GO_TO(user_inter_x , user_inter_y)
        
        ask = input("please enter y to continue else quit")
        if ask != "y" :
            break
        """

    # user_inter_x = float(input("Please enter the x value"))
    # user_inter_y = float(input("Please enter the y value"))
    user_inter_x = rospy.get_param("/x_move")
    user_inter_y = rospy.get_param("/y_move")
    
    GO_TO(user_inter_x , user_inter_y)
        
    