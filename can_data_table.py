from tksheet import Sheet
import tkinter as tk
import random
import time
from threading import *
from can_messages import Dataa

class demo(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.data=[["Average Motor Stator Current",0],
                ["Average Motor Phase Voltage",0],
                ["Target Torque",0],
                ["Motor Actual Torque    ",0], 
                ["Steering Angle",0],
                ["Proportional Speed Limit  ",0], 
                ["Motor RPM          ",0], 
                ["Calculated Battery Current ",0], 
                ["Controller Capacitor Voltage",0], 
                ["Throttle input       ",0], 
                ["Motor Temp         ",0], 
                ["Controller Temperature   ",0], 
                ["Distance travelled     ",0], 
                ["Forward switch       ",0], 
                ["Reverse Switch       ",0], 
                ["Seat Switch         ",0]
                ]
        
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(0, weight = 1)
        self.sheet = Sheet(self.frame,
                           page_up_down_select_row = True,
                           #empty_vertical = 0,
                           column_width = 150,
                           startup_select = (0,1,"rows"),
                            data = self.data,
                           theme = "black",
                            height = 400, #height and width arguments are optional
                            width = 360, #For full startup arguments see DOCUMENTATION.md
                            )
        self.sheet.enable_bindings(("single_select", #"single_select" or "toggle_select"
                                         "drag_select",   #enables shift click selection as well
                                         "column_drag_and_drop",
                                         "row_drag_and_drop",
                                         "column_select",
                                         "row_select",
                                         "column_width_resize",
                                         "double_click_column_resize",
                                        #  "row_width_resize",
                                        #  "column_height_resize",
                                         "arrowkeys",
                                         "row_height_resize",
                                         "double_click_row_resize",
                                         "right_click_popup_menu",
                                         "rc_select",
                                         "rc_insert_column",
                                         "rc_delete_column",
                                         "rc_insert_row",
                                         "rc_delete_row",
                                    "hide_columns",
                                         "copy",
                                         "cut",
                                         "paste",
                                         "delete",
                                         "undo",
                                         "edit_cell"))

        self.frame.grid(row = 0, column = 0, sticky = "nswe")
        self.sheet.grid(row = 0, column = 0, sticky = "nswe")

        self.sheet.headers((f"Header {c}" for c in range(2))) #any iterable works
        self.sheet.headers("CAN Data", 0)
        self.sheet.headers("CAN Values", 1)
        
    def all_extra_bindings(self, event):
        print (event)
    
    def begin_edit_cell(self, event):
        print (event)   # event[2] is keystroke
        return event[2] # return value is the text to be put into cell edit window

    def end_edit_cell(self, event):
        print (event)

    def window_resized(self, event):
        pass
        #print (event)

    def mouse_motion(self, event):
        region = self.sheet.identify_region(event)
        row = self.sheet.identify_row(event, allow_end = False)
        column = self.sheet.identify_column(event, allow_end = False)
        print (region, row, column)

    def deselect(self, event):
        print (event, self.sheet.get_selected_cells())

    def rc(self, event):
        print (event)
        
    def cell_select(self, response):
        #print (response)
        pass

    def shift_select_cells(self, response):
        print (response)

    def drag_select_cells(self, response):
        pass
        #print (response)

    def ctrl_a(self, response):
        print (response)

    def row_select(self, response):
        print (response)

    def shift_select_rows(self, response):
        print (response)

    def drag_select_rows(self, response):
        pass
        #print (response)
        
    def column_select(self, response):
        print (response)
        #for i in range(50):
        #    self.sheet.create_dropdown(i, response[1], values=[f"{i}" for i in range(200)], set_value="100",
        #                               destroy_on_select = False, destroy_on_leave = False, see = False)
        #print (self.sheet.get_cell_data(0, 0))
        #self.sheet.refresh()

    def shift_select_columns(self, response):
        print (response)

    def drag_select_columns(self, response):
        pass
        # print (response)

    def null_print(self):
        print("NULL Printing\n")

class App(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.demo=None
        self.start()

    def callback(self):
        self.demo.quit()

    def run(self):
        self.demo = demo()
        self.demo.title("BOSON Zekrom")
        self.demo.protocol("WM_DELETE_WINDOW", self.callback)
        self.demo.mainloop()


    # work function
    def work(self,val):
        if (self.demo is not None):
            self.demo.sheet.set_column_data(1, values = tuple(val),redraw = True)

# root=tk.Tk()
app = App()
obj= Dataa()
print('Now we can continue running code while mainloop runs!')
while True:
    val=obj.valuess1()
    app.work(val)

# root.mainloop()