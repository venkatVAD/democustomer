#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import can
import sys
from numpy import interp

class RPM_control:
    def __init__(self):
        self.baud_rate=rospy.get_param('baud_rate','1000000')
        self.channel_can=rospy.get_param('channel_can','vcan0')
        self.bus_type_can=rospy.get_param('bustype_can','socketcan')
        rospy.Subscriber("/sensor/joystick/right_stick_y", Float32, self.cmd_callback)
        self.bus=bus = can.interface.Bus(bustype=self.bus_type_can, channel=self.channel_can, bitrate= self.baud_rate )
        rospy.Timer(rospy.Duration(0.02), self.timer)
        self.timer_cmd_vel=rospy.get_rostime()
        self.x_linear=0


    def cmd_callback(self,data):
        self.x_linear=data.data
        self.timer_cmd_vel=rospy.get_rostime()

    def timer(self,event):
        
        now=rospy.get_rostime()
        # print(now-self.timer_cmd_vel)
        time_diff=(now-self.timer_cmd_vel).to_nsec()/900000000
    
        if time_diff>1:
            rospy.loginfo('time out from cmd_vel')
            msg=[0X0,0X0,0X0,0X0,0X0,0X0,0X0,0X0]
            can_msg = can.Message(arbitration_id=0x510,
                    data=msg,
                    extended_id=False)
            print(msg)
            self.bus.send(can_msg)
                

        mapped=int(interp(abs(self.x_linear), [0,1], [0,3000]))
        # print('mapped',mapped)
        hex_value=hex(int(mapped))[2:]
        print(hex_value)
        if len(hex_value)==4:
                d1=hex_value[:2]
                d2=hex_value[2:]
        elif len(hex_value)==3:
            d1='0'+hex_value[0]
            d2=hex_value[1:]
        elif len(hex_value)==2:
            d1='00'
            d2=hex_value
        elif len(hex_value)==1:
            d1='00'
            d2='0'+hex_value
        else:
            d1='00'
            d2='00'
        d1 = int(d1, 16)
        d2 = int(d2, 16)
        # print(d1,d2)
        if self.x_linear>0:
            d3=0X1
        elif self.x_linear<0:
             d3=0X2
        else:
            d3=0X0

        msg=[d2,d1,d3,0X0,0X0,0X0,0X0,0X0]
        can_msg = can.Message(arbitration_id=0x510,
                            data=msg,
                            extended_id=False)
        print(msg)
        self.bus.send(can_msg)
    def run(self):
        rospy.spin()
if __name__=="__main__":
    rospy.init_node("rpm_test")
    rpm_control=RPM_control()
    rpm_control.run()
