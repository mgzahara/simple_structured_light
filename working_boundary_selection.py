from Tkinter import *
import cv2

#TODO:
#see line 221 and psuedo code at EOF

class Window():
    def __init__(self):
        """Set up start of program"""
        
        self.root = Tk()
        self.window_width  = "500"
        self.window_height = "200"

        #create main Frame 
        self.main_frame = Frame(self.root,
                                width = self.window_width,
                                height = self.window_height)
        #force size
        self.main_frame.pack_propagate(0)

        #return
        #cut off for setup function
        
        #populate main_frame
        self.direction = "Left"
        self.show_boundary_frame_prompt()
        #used to determine which boundary we are setting
        self.bound_count = 0
                
        self.root.mainloop()
        return
    
    def nothing(self):
        """Empty function"""
        pass
    
    def restart_boundary_selection(self):
        """Reset state for obtaining boundaries"""

        self.direction = "Left"
        self.show_boundary_frame_prompt()
        self.bound_count = 0
        return
    
    def boundary_selection_next_button(self):
        """Event handler for the 'next' button"""
        
        self.bound_count += 1
        #hide tkinter window
        self.root.withdraw()
        #get x and y from opencv window click
        new_x, new_y = self.get_next_boundary()

        #store coordinates appropriately
        if self.bound_count == 1:
            #left
            self.left_bound = (new_x, new_y)
            self.direction = "Top"
            self.show_boundary_frame_prompt()

        elif self.bound_count == 2:
            #top
            self.top_bound = (new_x, new_y)
            self.direction = "Right"
            self.show_boundary_frame_prompt()

        elif self.bound_count == 3:
            #right
            self.right_bound = (new_x, new_y)
            self.direction = "Bottom"
            self.show_boundary_frame_prompt()
            
        elif self.bound_count == 4:
            #bottom
            self.bottom_bound = (new_x, new_y)
            #done with this stage... moving on...
            self.show_boundary_verification_frame()

        self.root.deiconify()
        return

    def get_next_boundary(self):
        """Get input from user for a boundary"""
        
        cap = cv2.VideoCapture(0)
        self.cont = True
        self.curr_x, self.curr_y = -1, -1


        def mouse_callback(event, x, y, flags, param):
            """Local function to handle mouse events"""

            if event == cv2.EVENT_LBUTTONDOWN:
                self.curr_x = x
                self.curr_y = y
                self.cont = False
            if event == cv2.EVENT_MOUSEMOVE:
                self.curr_x = x
                self.curr_y = y
            return

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) )
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) )
        white = (255, 255, 255)
        black = (0, 0, 0)

        window_name = "boundary selection"
        cv2.namedWindow(window_name,cv2.WINDOW_AUTOSIZE)        
        cv2.setMouseCallback(window_name, mouse_callback)

        
        while(self.cont):

            ret, frame = cap.read()

            if self.bound_count % 2 == 1:
            #vertical
                cv2.line(frame,
                         (self.curr_x, 0),
                         (self.curr_x, height),
                         black, 3)
                cv2.line(frame,
                         (self.curr_x, 0),
                         (self.curr_x, height),
                         white, 1)

            else:
            #horizontal
                cv2.line(frame,
                         (0, self.curr_y),
                         (width, self.curr_y),
                         black, 3)
                cv2.line(frame,
                         (0, self.curr_y),
                         (width, self.curr_y),
                         white, 1)

            cv2.imshow(window_name, frame)

            k = cv2.waitKey(1) & 0xFF

        cap.release()
        cv2.destroyAllWindows()

        return (self.curr_x, self.curr_y)

    def clear_main_frame(self):
        """Remove all children from the main Frame widget"""
        
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        return

    def show_boundary_frame_prompt(self):
        """Prompt user for the next boundary"""

        self.clear_main_frame()

        self.prompt = "Please provide a boundary for the following edge:\n"
        self.l = Label(self.main_frame,
                       text = "%s\n%s"%(self.prompt, self.direction) )
        self.l.pack(side = TOP, pady = (25, 10))

        self.b = Button(self.main_frame,
                        text = "next",
                        command = self.boundary_selection_next_button)

        self.b.pack(side = BOTTOM, pady = (5, 15) )

        self.main_frame.pack()
        return

    def show_boundary_verification_frame(self):
        """Verify boundaries provided were valid and confirm with user"""
        
        self.clear_main_frame()

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
            l.pack(side = TOP, pady = (25, 10))

            self.b = Button(self.main_frame,
                            text = "okay",
                            command = self.show_boundary_frame_prompt)
        
            self.b.pack(side = BOTTOM, pady = (5, 15) )

            self.main_frame.pack()
            
        else:
            #boundaries were valid, verify with user
            self.show_final_boundaries()

            l = Label(self.main_frame, text = "were the chosen boundaries acceptable?")
            l.pack(side = TOP, pady = (25, 10))

            self.temp_button_frame = Frame(self.main_frame,
                                      width = self.window_width)
            
            self.b1 = Button(self.temp_button_frame,
                             text = "yes",
                             command = self.main_frame.quit)
            #the above line determines what happens once the user
            #accepts the boundaries

            self.b1.pack(side = LEFT, pady = (5, 15), padx = (0, 10) )
            
            self.b2 = Button(self.temp_button_frame,
                            text = "no",
                             command = self.restart_boundary_selection)
        
            self.b2.pack(side = LEFT, pady = (5, 15) )
            self.temp_button_frame.pack(side = BOTTOM)
            self.main_frame.pack()

        return

    def show_final_boundaries(self):
        """Show user their chosen boundaries"""
        
        cap = cv2.VideoCapture(0)
        self.cont = True
        self.curr_x, self.curr_y = -1, -1
        
        def mouse_callback(event, x, y, flags, param):
            """Local function to handle mouse events"""
            if event == cv2.EVENT_LBUTTONDOWN:
                self.cont = False
            return

        white = (255, 255, 255)
        black = (0, 0, 0)

        window_name = "boundary verification"
        cv2.namedWindow(window_name,cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(window_name, mouse_callback)

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

#win.setup()
    #win.set_boundaries()
    #win.set_rotational_axis()
    #win.get_scan_info() - img capture freq or stats to calc it
    #win.setup_wait() - sit idle with video feed and overlay
    ## of boundaries waiting for user to begin scanning

#win.scan()
