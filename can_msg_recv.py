from tabulate import tabulate
import can


class Dataa:
    def __init__(self):
        self.bus=can.interface.Bus(bustype="socketcan",channel="can0",bitrate=250000)
        self.avg_Stater_Crnt=0
        self.avgMtr_PhaseV=0
        self.tgt_torq=0
        self.mtractl_torq=0
        self.propspeedlmt=0
        self.MotorRPM=0
        self.calbattery_crnt=0
        self.ctrlcapctr_v=0
        self.trottleip=0
        self.mtr_temp=0
        self.ctrlr_temp=0
        self.dis_traveld=0
        self.drive_dirctn=0
        self.forward=0
        self.reverse=0
        self.seat_s=0
      
    def twos_comp(self, val, bits):
        if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)        # compute negative value
        return val 

    def spe(self):
        
        self.message=self.bus.recv()
        
        if self.message.arbitration_id==0x201:
            self.a=bytearray(self.message.data)
            self.he=self.a.hex() #converting bytearray to hex format
            self.avg_Stater_Crnt1=int(self.he[0:2],16)
            self.avg_Stater_Crnt2=int(self.he[2:4],16)
            self.avg_Stater_Crnt=self.avg_Stater_Crnt2+self.avg_Stater_Crnt1
            self.avg_Stater_Crnt= self.twos_comp(self.avg_Stater_Crnt,16)
            self.avgMtr_PhaseV1=int(self.he[4:6],16)
            self.avgMtr_PhaseV2=int(self.he[6:8],16)
            self.avgMtr_PhaseV=self.avgMtr_PhaseV2+self.avgMtr_PhaseV1
            self.avgMtr_PhaseV= self.twos_comp(self.avgMtr_PhaseV,16)*0.0625 
            self.tgt_torq1=int(self.he[8:10],16)
            self.tgt_torq2=int(self.he[10:12],16)
            self.tgt_torq=self.tgt_torq2+self.tgt_torq1
            self.tgt_torq= self.twos_comp(self.tgt_torq,16)*0.0625
            self.mtractl_torq1=int(self.he[12:14],16)
            self.mtractl_torq2=int(self.he[14:16],16)
            self.mtractl_torq=self.mtractl_torq2+self.mtractl_torq1
            self.mtractl_torq= self.twos_comp(self.mtractl_torq,16)*0.0625 

        elif self.message.arbitration_id==0x202:
            self.a=bytearray(self.message.data)
            self.he=self.a.hex() #converting bytearray to hex format
            self.propspeedlmt=int(self.he[0:8],32)
            self.propspeedlmt= self.twos_comp(self.propspeedlmt,32)
            self.MotorRPM=int(self.he[8:],32)
            self.MotorRPM= self.twos_comp(self.MotorRPM,32)

        elif self.message.arbitration_id==0x203:
            self.a=bytearray(self.message.data)
            self.he=self.a.hex() #converting bytearray to hex format
            self.calbattery_crnt=int(self.he[0:4],16)
            self.calbattery_crnt1=int(self.he[0:2],16)
            self.calbattery_crnt2=int(self.he[2:4],16)
            self.calbattery_crnt=self.calbattery_crnt2+self.calbattery_crnt1
            self.calbattery_crnt=self.twos_comp(self.calbattery_crnt,16)*0.0625
            self.ctrlcapctr_v1=int(self.he[4:6],16)
            self.ctrlcapctr_v2=int(self.he[6:8],16)
            self.ctrlcapctr_v=(self.ctrlcapctr_v2+self.ctrlcapctr_v1)*0.0625
            self.trottleip1=int(self.he[8:10],16)
            self.trottleip2=int(self.he[10:12],16)
            self.trottleip=self.trottleip2+self.trottleip1
            self.trottleip=self.twos_comp(self.trottleip,16)*0.00390625

        elif self.message.arbitration_id==0x204:
            self.a=bytearray(self.message.data)
            self.he=self.a.hex() #converting bytearray to hex format
            self.mtr_temp1=int(self.he[0:2],16)
            self.mtr_temp2=int(self.he[2:4],16)
            self.mtr_temp=self.mtr_temp2+self.mtr_temp1
            self.mtr_temp=self.twos_comp(self.mtr_temp,16)
            self.ctrlr_temp=int(self.he[4:6],16)
            # self.ctrlr_temp1=int(self.he[4],16)
            # self.ctrlr_temp2=int(self.he[5],16)
            # self.ctrlr_temp=self.ctrlr_temp2+self.ctrlr_temp1
            self.ctrlr_temp=self.twos_comp(self.ctrlr_temp,8)
            self.dis_traveld1=int(self.he[6:8],32)
            self.dis_traveld2=int(self.he[8:10],32)
            self.dis_traveld3=int(self.he[10:12],32)
            self.dis_traveld4=int(self.he[12:14],32)
            self.dis_traveld=self.dis_traveld4+self.dis_traveld3+self.dis_traveld2+self.dis_traveld1
            self.dis_traveld=self.dis_traveld*0.00390625
            self.drive_dirctn1=int(self.he[14],16)
            self.drive_dirctn2=int(self.he[15],16)
            self.drive_dirctn=self.drive_dirctn2+self.drive_dirctn1
            if self.drive_dirctn==0:
                self.forward=0
                self.reverse=0
                self.seat_s=0
            elif self.drive_dirctn==1:
                self.forward=1
                self.reverse=0
                self.seat_s=0
            elif self.drive_dirctn==2:
                self.forward=0
                self.reverse=1
                self.seat_s=0
            elif self.drive_dirctn==4:
                self.forward=0
                self.reverse=0
                self.seat_s=1
            elif self.drive_dirctn==5:
                self.forward=1
                self.reverse=0
                self.seat_s=1
            elif self.drive_dirctn==6:
                self.forward=0
                self.reverse=1
                self.seat_s=1
            else:
                pass

        else:
            print("Dont worry")

    def table1(self):
        while True:
            self.spe()
            file= open("mytext.txt","w")
            self.table=[["Name", "Value"],["AverageMotorStatorCurrent", self.avg_Stater_Crnt],["AverageMotorPhaseVoltage", self.avgMtr_PhaseV],["Target Trque", self.tgt_torq],["Motor Actual Torque", self.mtractl_torq],["Proportional Speed Limit", self.propspeedlmt],["Motor RPM", self.MotorRPM],["Calculated Battery Current",self.calbattery_crnt],["Controller Capacitor Voltage",self.ctrlcapctr_v],["Throttle input",self.trottleip],["Motor Temp",self.mtr_temp],["Controller Temperature", self.ctrlr_temp],["Distance travelled", self.dis_traveld],["Forward switch",self.forward],["Reverse Switch", self.reverse],["Seat Switch", self.seat_s]]
            a=tabulate(self.table, headers="firstrow", tablefmt="pretty")
            file.write(str(a))
            file.close()
            print(a)

    def valuess(self):
    #    while True:
        self.spe()
        self.values_to_add= (self.avg_Stater_Crnt,self.avgMtr_PhaseV,self.tgt_torq, self.mtractl_torq,self.propspeedlmt, self.MotorRPM,self.calbattery_crnt,self.ctrlcapctr_v, self.trottleip,self.mtr_temp, self.ctrlr_temp,self.dis_traveld,self.forward,self.reverse,self.seat_s)
        # for i in self.values_to_add:
        return self.values_to_add


A= Dataa()  
# A.valuess()
# A.spe()   
A.table1()
