#!/usr/bin/env python
import os
import sys
import can



bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=250000)
msg1=can.Message(arbitration_id=0x501, data=[101,0,0],is_extended_id=False)
msg3=can.Message(arbitration_id=0x501, data=[101,0,0x02],is_extended_id=False)
msg4=can.Message(arbitration_id=0x501, data=[101,0,0x05],is_extended_id=False)

autoModeRequestAccepted = False
autoMode = False


def start():
    while True:
        if (input("Do you want to use auto mode? 'y'") =="y"):
            bus.send(msg1)
            while True:
                message=bus.recv()
                msg=message.data
                if message.arbitration_id==0x501:
                    if msg[2]==0x01:
                        bus.send(msg3)
                        autoModeRequestAccepted = True

                    elif msg[2]==0x04 and autoModeRequestAccepted:
                        autoModeRequestAccepted = False
                        autoMode= True
                        print ("we are in autonomus mode")
                        print("close stop auto mode by presing ctrl+c")
                        break
                    elif msg[2]==0x03:
                        autoMode = False

                        if msg[1]==1:
                            print("Motor RPM above safe threshold")
                        elif msg[1]==2:
                            print("throttle pressed above threshold")
                        elif msg[1]==3:
                            print("automode request timeout")
                        break
            
            while autoMode:
                message=bus.recv()
                msg=message.data
                if message.arbitration_id==0x501:
                    if msg[2]==0x03:
                        autoMode = False
                        print("Automode interrupted. \n")
                        
                        if msg[1]==10:
                            print("Driver command message timeout")
                        elif msg[1]==11:
                            print("No response from On-Board computer")
                        
                        elif msg[1] == 12:
                            print("User pressed throttle")
                        
                        elif msg[1] == 13:
                            print("User changed FNR state")
                        break
                    elif msg[2]==0x04 and msg[1]==0x01:
                        bus.send(msg4)
                    
start()

# def stop():
#     while True:
        
#         a = input("")
#         if a == "n":
#             sys.exit(start)



                


            
   
