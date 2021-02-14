# File: addressbook.py
# Author: Michael Thomas
# Date: 10/6/20
# Description: Clock project

import math 
import datetime
import tkinter as tk
from datetime import datetime
from enum import Enum

class State(Enum):
    Running = 1
    Stopped = 2

class Display_Clock:
    def __init__(self):
        self.window = tk.Tk() # Create a window
        self.window.title("Current Time") # Set a title
        self.text_offset = 12
        self.canvas_size = 300
        self.radius = int(self.canvas_size*0.8/2)
        self.time_between_updates = 1000
        self.canvas = tk.Canvas(
            self.window, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()
        # clock face
        self.canvas.create_oval(self.canvas_size * 0.1, self.canvas_size * 0.1,
                                self.canvas_size*0.9, self.canvas_size*0.9, )
        # clock face numbers
        self.canvas.create_text(self.canvas_size/2,
                                self.canvas_size * 0.17 - self.text_offset, text='12')
        self.canvas.create_text(self.canvas_size * 0.87, self.canvas_size/2, text='3')
        self.canvas.create_text(self.canvas_size/2,
                                self.canvas_size - (self.canvas_size * 0.13), text='6')    
        self.canvas.create_text(self.canvas_size * 0.13, self.canvas_size/2, text='9')                                            
        self.second_hand_length = self.radius*0.8
        self.minute_hand_length = self.radius*0.65
        self.hour_hand_length = self.radius * 0.5

        # time label under clock
        self.time_var = tk.StringVar()
        self.time_frame = tk.Frame(self.window)
        self.time_frame.pack()
        self.time_label = tk.Label(self.time_frame, textvariable=self.time_var, borderwidth=1)
        self.time_label.grid(row=1, column=1, pady="10")

        # button frame and buttons
        self.btn_frame = tk.Frame(self.window)
        self.btn_frame.pack()
        self.start_stop_btn = tk.Button(self.btn_frame, text="Start", command=self.start_stop)
        self.start_stop_btn.grid(row=1, column=1, padx="5")
        self.quit_btn = tk.Button(self.btn_frame, text="Quit", command=self.quit)
        self.quit_btn.grid(row=1, column=3, padx="5")
        
        # state of program
        self.state = State.Stopped

        # set initial time
        self.update_time()
        # start clock upon initialization
        self.start()
        # start loop
        self.window.mainloop()

    def update_time(self):
        second = datetime.now().second
        minute = datetime.now().minute
        hour = datetime.now().hour

        self.time_var.set(f"{hour:02}:{minute:02}:{second:02}")

        # draw second hand
        xSecond = self.canvas_size//2 + self.second_hand_length * \
            math.sin(second/60 * (2 * math.pi))
        ySecond = self.canvas_size//2 - self.second_hand_length * \
            math.cos(second/60 * (2 * math.pi))
        self.sec_id = self.canvas.create_line(self.canvas_size//2, self.canvas_size//2, xSecond, ySecond,
                                fill="red", tags="hands")
        # draw minute hand
        xMinute = self.canvas_size//2 + self.minute_hand_length * \
            math.sin(minute/60 * (2 * math.pi))
        yMinute = self.canvas_size//2 - self.minute_hand_length * \
            math.cos(minute/60 * (2 * math.pi))  
        self.min_id = self.canvas.create_line(self.canvas_size//2, self.canvas_size//2, xMinute, yMinute,
                                fill="blue", tags="hands")
        # draw hour hand
        xHour = self.canvas_size//2 + self.hour_hand_length * \
            math.sin(hour/12 * (2 * math.pi))
        yHour = self.canvas_size//2 - self.hour_hand_length * \
            math.cos(hour/12 * (2 * math.pi))
        self.hour_id = self.canvas.create_line(self.canvas_size//2, self.canvas_size//2, xHour, yHour, 
                                fill="green", tags="hands")    

    def time_handler(self):
        self.canvas.delete("hands")
        self.update_time()
        self.timer_event = self.canvas.after(self.time_between_updates, self.time_handler)
   
   # helper function to link to button start/stop
    def start_stop(self):
        if self.state == State.Running:
            self.stop()
        else:
            self.start()    
        
    def quit(self):
        self.window.destroy()
    # change button text, state, and start time handler
    def start(self):
        self.start_stop_btn["text"] = "Stop"
        self.time_handler()
        self.state = State.Running
    # change button text, state, and stop time handler   
    def stop(self):
        self.start_stop_btn["text"] = "Start"
        self.canvas.after_cancel(self.timer_event)
        self.state = State.Stopped
           
        
        
if __name__ == "__main__":
    Display_Clock()
