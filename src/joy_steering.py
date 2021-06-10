#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import can
from numpy import interp





# try:
# baud_rate=rospy.get_param('baudrate')
# channel=rospy.get_param('channel_can')
# bus_type=rospy.get_param('bustype')



# if channel=='vcan0' or channel=='can0':
#     pass
# else:
#     print("YOU ENTERED "+str(channel))
#     print("GIVEN INVALID CAN CHANNEL NAME ")
#     sys.exit()

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
#bus = can.interface.Bus(bustype=bus_type, channel=channel, bitrate=baud_rate)

print("---------------------------------------------------------------")

print("         CONNECTION TO CAN DEVICE-- SUCCESS")
print("---------------------------------------------------------------")
    
# except Exception as e:
#     print("---------------------------------------------------------------")
#     print("                CONNECTION TO CAN DEVICE-- FAILED")
#     print("     			PLEASE MAKE CAN UP              	 ")
#     print("                                OR                                ")
#     print("            PLEASE DO CHECK BAUDRATE AND CHANNEL NAME IN LAUNCH FILE")
#     print(' ERROR is --',e)
#     print("----------------------------------------------------------------")
#     sys.exit()



def callback(data):
    
    x_angular=data.data
    c = x_angular
    rospy.loginfo("twist.linear: %f ; angular %f", data.data, c)


    if c==0:
        f=0
    elif c<0:
        f = c*40
    elif c>0:
        f = c*40
    
    angle_of_rotation=127+(f*3)
    angle_of_rotation=int(hex(int(angle_of_rotation))[2:],16) 
    steer_msg=[0X02,angle_of_rotation,0X0,0X0,0X0,0X0,0X0,0X0]
    steer_can_msg = can.Message(arbitration_id=0x298,
                    data=steer_msg,
                    extended_id=False)
    bus.send(steer_can_msg)


    
    
def listener():
    rospy.init_node('mobile_subscriber', anonymous=True)
    rospy.Subscriber("/sensor/joystick/left_stick_x", Float32, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()