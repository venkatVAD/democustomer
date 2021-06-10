#!/usr/bin/env python

import curses
import subprocess
import time
import datetime
import can
from can_messages import*
from curseXcel import Table

class Terminal():

    def data(self):
        obj= Dataa()
        
        self.screen = curses.initscr()
        self.screen.addstr("Boson Zekrom Data in 2'sec")
        self.screen.refresh()
        curses.napms(2000)

        while True:
            self.screen.clear()
            self.a=obj.table1()
        # self.outputl = self.a.splitlines(',')
            # while True:
            self.screen.addstr(str(self.a))
            self.screen.addstr("\n")
        # self.screen.addstr("%s\n"%())
            self.screen.refresh()
            # now = datetime.datetime.now()
            # self.screen.addstr("Current date and time : %s\n"%(now.strftime("%Y-%m-%d %H:%M:%S")))

        curses.napms(1)
        curses.endwin() 

'''
        # cmd="python can_msg_recv_1.py"
        while True:
            self.screen.clear()
            self.a=obj.valuess()

        # self.outputl = self.a.splitlines(',')
            for i in range(len(self.a)):
                self.screen.addstr(str(self.a[i]))
                self.screen.addstr("\n")
                # self.screen.addstr("%s\n"%())
                self.screen.refresh()
            # now = datetime.datetime.now()
            # self.screen.addstr("Current date and time : %s\n"%(now.strftime("%Y-%m-%d %H:%M:%S")))

            curses.napms(1)
        curses.endwin() 
'''

A= Terminal()
A.data()
