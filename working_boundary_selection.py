from Tkinter import *
from time import sleep
import cv2
#TODO:
#see line 220

def nothing():
    pass
def p():
    print "yooo!"

class Window():
    def __init__(self):
        self.root = Tk()
        self.window_width  = "500"
        self.window_height = "200"

        #create main Frame 
        self.main_frame = Frame(self.root,
                                width = self.window_width,
                                height = self.window_height)
        #force size
        self.main_frame.pack_propagate(0)

        #populate main_frame
        self.direction = "Left"
        self.set_boundary_frame()
        #used to determine which boundary we are setting
        self.bound_count = 0
                
        self.root.mainloop()
        return
    
    def nothing(self):
        pass
    
    def restart(self):
        self.direction = "Left"
        self.set_boundary_frame()
        self.bound_count = 0
        print "--restarting--"
        return
    
    def next_button(self):
        #print "next_button"
        self.bound_count += 1
        self.root.withdraw()
        #self.b.configure(text=str(self.button_counter))
        new_x, new_y = self.get_next_boundary()
        if self.bound_count == 1:
            #left
            self.left_bound = (new_x, new_y)
            print "left   bound: {}".format(self.left_bound)
            self.direction = "Top"
            self.set_boundary_frame()

        elif self.bound_count == 2:
            #top
            self.top_bound = (new_x, new_y)
            print "top    bound: {}".format(self.top_bound)
            self.direction = "Right"
            self.set_boundary_frame()

        elif self.bound_count == 3:
            #right
            self.right_bound = (new_x, new_y)
            print "right  bound: {}".format(self.right_bound)
            self.direction = "Bottom"
            self.set_boundary_frame()
            
        elif self.bound_count == 4:
            #bottom
            self.bottom_bound = (new_x, new_y)
            print "bottom bound: {}".format(self.bottom_bound)
            #done with this stage... moving on...
            #call function to create boundary verification screen
            self.set_boundary_verification_frame()
            return
        self.root.deiconify()
        return
    def get_next_boundary(self):
        #start opencv video with crosshairs
        #return x, y coordinates from user input
        cap = cv2.VideoCapture(0)
        self.cont = True
        self.curr_x, self.curr_y = -1, -1

        window_name = "boundary selection"
        cv2.namedWindow(window_name,cv2.WINDOW_AUTOSIZE)

        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.curr_x = x
                self.curr_y = y
                self.cont = False
                sleep(0.5)
            if event == cv2.EVENT_MOUSEMOVE:
                self.curr_x = x
                self.curr_y = y
        
        cv2.setMouseCallback(window_name, mouse_callback)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) )
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) )
        white = (255, 255, 255)
        black = (0, 0, 0)

        while(self.cont):
            ret, frame = cap.read()

            if self.bound_count % 2 == 1:
            #vertical
                cv2.line(frame,
                         (self.curr_x - 1, 0),
                         (self.curr_x - 1, height),
                         black, 1)
                cv2.line(frame,
                         (self.curr_x, 0),
                         (self.curr_x, height),
                         white, 1)
                cv2.line(frame,
                         (self.curr_x + 1, 0),
                         (self.curr_x + 1, height),
                         black, 1)
            else:
            #horizontal
                cv2.line(frame,
                         (0, self.curr_y - 1),
                         (width, self.curr_y - 1),
                         black, 1)
                cv2.line(frame,
                         (0, self.curr_y),
                         (width, self.curr_y),
                         white, 1)
                cv2.line(frame,
                         (0, self.curr_y + 1),
                         (width, self.curr_y + 1),
                         black, 1)


            cv2.imshow(window_name, frame)

            k = cv2.waitKey(1) & 0xFF

        cap.release()
        cv2.destroyAllWindows()

        return (self.curr_x, self.curr_y)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            #remove all children from main_frame
            widget.destroy()

    
    def set_boundary_frame(self):

        self.clear_main_frame()
        
        self.prompt = "Please provide a boundary for the following edge:\n"
#        self.direction = direction
        self.l = Label(self.main_frame,
                       text = "%s\n%s"%(self.prompt, self.direction) )
        self.l.pack(side = TOP, pady = (15, 10))

        self.b = Button(self.main_frame,
                        text = "next",
                        command = self.next_button)
        
        self.b.pack(side = BOTTOM, pady = (5, 15) )

        self.main_frame.pack()
        return

    def set_boundary_verification_frame(self):
        
        self.clear_main_frame()

        #check that we were given valid boundaries
        valid_bounds = True
        bounds_err_msg = "There was a conflict between the following boundaries provided:\n"
        if self.left_bound[0] >= self.right_bound[0]:
            #left and right bounds are not valid
            valid_bounds = False
            bounds_err_msg += "Left and Right\n"
        if self.top_bound[1] >= self.bottom_bound[1]:
            #top and bottom bounds are not valid
            valid_bounds = False
            bounds_err_msg += "Top and Bottom"

        if not valid_bounds:
            self.direction = "Left"
            self.bound_count = 0
            #tell user they gave bogus bounds and ask for a redo
            l = Label(self.main_frame, text= bounds_err_msg)
            l.pack(side = TOP)

            self.b = Button(self.main_frame,
                            text = "okay",
                            command = self.set_boundary_frame)
        
            self.b.pack(side = BOTTOM, pady = (5, 15) )
        else:
            #boundaries were valid, verify with user

            self.verify_boundaries()
            
            #ask if the presented boundaries were acceptable
            l = Label(self.main_frame, text = "were the chosen boundaries acceptable?")
            l.pack(side = TOP)

            self.temp_button_frame = Frame(self.main_frame,
                                      width = self.window_width)
            
            self.b1 = Button(self.temp_button_frame,
                             text = "yes",
                             command = self.main_frame.quit)
            #the above line determines what happens once the user
            #accepts the boundaries
            #TODO / next steps:
            #make user chose the rotational axis
            #keep the boundary box on screen when scanning?
            #ask user how often to capture an image
            #calc based on some stats?
            self.b1.pack(side = LEFT, pady = (5, 15), padx = (0, 10) )
            
            self.b2 = Button(self.temp_button_frame,
                            text = "no",
                             command = self.restart)
        
            self.b2.pack(side = LEFT, pady = (5, 15) )

            self.temp_button_frame.pack(side = BOTTOM)

            self.root.deiconify()

    def verify_boundaries(self):
        #start opencv video with crosshairs
        #return x, y coordinates from user input
        cap = cv2.VideoCapture(0)
        self.cont = True
        self.curr_x, self.curr_y = -1, -1
        
        window_name = "boundary selection"
        cv2.namedWindow(window_name,cv2.WINDOW_AUTOSIZE)
        
        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.cont = False
                sleep(0.5)
        
        cv2.setMouseCallback(window_name, mouse_callback)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) )
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) )
        white = (255, 255, 255)
        black = (0, 0, 0)

        while(self.cont):
            ret, frame = cap.read()
            
            #place boundary rectangle over video feed
            cv2.rectangle(frame,
                          (self.left_bound[0], self.top_bound[1]),
                          (self.right_bound[0], self.bottom_bound[1]),
                          black, 3)
            
            cv2.rectangle(frame,
                          (self.left_bound[0], self.top_bound[1]),
                          (self.right_bound[0], self.bottom_bound[1]),
                          white, 1)
            
            cv2.imshow(window_name, frame)

            k = cv2.waitKey(1) & 0xFF

        cap.release()
        cv2.destroyAllWindows()
        return


            
win = Window()
