from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog, tkMessageBox
import cv2
import os

#TODO:
#see line

class Window():
    def __init__(self):
        """Set up start of program"""
        
        self.root = Tk()
        self.root.title("simple structured light")
        self.window_width  = "500"
        self.window_height = "200"

        #create main Frame 
        self.main_frame = Frame(self.root,
                                width = self.window_width,
                                height = self.window_height)
        #force size
        self.main_frame.pack_propagate(0)

        return
        #cut off for setup function

    def setup(self):
        """Starts the set up process for a scan"""
        #populate main_frame
        self.direction = "Left"
        self._show_boundary_frame_prompt()
        #used to determine which boundary we are setting
        self.bound_count = 0
                
        self.root.mainloop()
        return
    
    def _nothing(self):
        """Empty function"""
        pass
    
    def _restart_boundary_selection(self):
        """Reset state for obtaining boundaries"""

        self.direction = "Left"
        self._show_boundary_frame_prompt()
        self.bound_count = 0
        return
    
    def _setup_with_opencv(self):
        """Generaic function to use opencv stuff for setup"""
        
        #hide tkinter window
        self.root.withdraw()
        #get webcam
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
        
        cv2.namedWindow(self.window_name,cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(self.window_name, mouse_callback)
        
        while(self.cont):
            ret, frame = cap.read()
            
            if self.bound_count <= 4:
                #first 4 times this will choose a boundary
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
            else:
                #boundaries are done, do the verification
                #always show boundaries after they are selected

                cv2.rectangle(frame,
                              (self.left_bound[0],
                               self.top_bound[1]),
                              (self.right_bound[0],
                               self.bottom_bound[1]),
                              black, 3)
                
                cv2.rectangle(frame,
                              (self.left_bound[0],
                               self.top_bound[1]),
                              (self.right_bound[0],
                               self.bottom_bound[1]),
                              white, 1)
                if self.window_name == "rotational axis selection":
                    #draw axis selection line
                    cv2.line(frame,
                             (self.curr_x, self.top_bound[1]),
                             (self.curr_x, self.bottom_bound[1]),
                             black, 3)
                    cv2.line(frame,
                             (self.curr_x, self.top_bound[1]),
                             (self.curr_x, self.bottom_bound[1]),
                             white, 1)
                    
                
            #draw modified frame
            cv2.imshow(self.window_name, frame)
            k = cv2.waitKey(1) & 0xFF
            
        #done with while(cont)
        cap.release()
        cv2.destroyAllWindows()
        
        return (self.curr_x, self.curr_y)
        
    def _boundary_selection_next_button(self):
        """Event handler for the 'next' button"""
        
        self.bound_count += 1
        #get x and y from opencv window click
        self.window_name = "boundary selection"
        new_x, new_y = self._setup_with_opencv()

        #store coordinates appropriately
        if self.bound_count == 1:
            #left
            self.left_bound = (new_x, new_y)
            self.direction = "Top"
            self._show_boundary_frame_prompt()

        elif self.bound_count == 2:
            #top
            self.top_bound = (new_x, new_y)
            self.direction = "Right"
            self._show_boundary_frame_prompt()

        elif self.bound_count == 3:
            #right
            self.right_bound = (new_x, new_y)
            self.direction = "Bottom"
            self._show_boundary_frame_prompt()
            
        elif self.bound_count == 4:
            #bottom
            self.bottom_bound = (new_x, new_y)
            #done with this stage... moving on...
            self.bound_count += 1
            self._show_boundary_verification_frame()

                    
        self.root.deiconify()
        return

    def _clear_main_frame(self):
        """Remove all children from the main Frame widget"""
        
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        return

    def _show_boundary_frame_prompt(self):
        """Prompt user for the next boundary"""

        self._clear_main_frame()

        self.prompt = "Please provide a boundary for the following edge:\n"
        self.l = Label(self.main_frame,
                       text = "%s\n%s"%(self.prompt, self.direction) )
        self.l.pack(side = TOP, pady = (15, 10))

        self.b = Button(self.main_frame,
                        text = "next",
                        command = self._boundary_selection_next_button)

        self.b.pack(side = BOTTOM, pady = (5, 15) )

        self.main_frame.pack()
        return

    def _show_boundary_verification_frame(self):
        """Verify boundaries provided were valid and confirm with user"""
        
        self._clear_main_frame()

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
            l = Label(self.main_frame, text = bounds_err_msg)
            l.pack(side = TOP, pady = (15, 10))

            self.b = Button(self.main_frame,
                            text = "okay",
                            command = self._show_boundary_frame_prompt)
        
            self.b.pack(side = BOTTOM, pady = (5, 15) )

            self.main_frame.pack()
            
        else:
            #boundaries were valid, verify with user
            self.window_name = "boundary verification"
            self._setup_with_opencv()

            l = Label(self.main_frame, text = "were the chosen boundaries acceptable?")
            l.pack(side = TOP, pady = (15, 10))

            self.temp_button_frame = Frame(self.main_frame)

            #preemptively name opencv window
            self.window_name = "rotational axis selection"
            self.b1 = Button(self.temp_button_frame,
                             text = "yes",
                             command = self._show_rotational_axis_prompt)
            #the above line determines what happens once the user
            #accepts the boundaries

            self.b1.pack(side = LEFT, pady = (5, 15), padx = (0, 10) )
            
            self.b2 = Button(self.temp_button_frame,
                             text = "no",
                             command = self._restart_boundary_selection)
        
            self.b2.pack(side = LEFT, pady = (5, 15) )
            self.temp_button_frame.pack(side = BOTTOM)
            self.main_frame.pack()

        return

    def _show_rotational_axis_prompt(self):
        """Prompt user to provide x coordinate 
        on which the subject will rotate"""

        self._clear_main_frame()

        prompt = "select the axis on which the subject will rotate"
        
        l = Label(self.main_frame, text = prompt)
        l.pack(side = TOP, pady = (15, 10))
        
        self.b = Button(self.main_frame,
                        text = "next",
                        command = self._get_rotational_axis)
        self.b.pack(side = BOTTOM, pady = (5, 15))
        
        self.main_frame.pack()

        return

    def _get_rotational_axis(self):
        """Obtain the rotational axis from user input
        Move to the next step"""

        valid_axis = False
        while not valid_axis:
            #verify the x given was valid            
            self.rot_axis = self._setup_with_opencv()

            if (self.rot_axis[0] > self.left_bound[0]
              and self.rot_axis[0] < self.right_bound[0]):
                valid_axis = True


        #create the new layout for the next parts of info
        self._clear_main_frame()
        prompt1 = "time in milliseconds of a full rotation"
        prompt2 = "number of samples per rotation"
        self.l1 = Label(self.main_frame,
                        text = prompt1)
        self.l1.pack(side = TOP, pady = (15, 10))

        self.full_rot_entry = Entry(self.main_frame, width = "20")
        self.full_rot_entry.pack(side = TOP)
        
        self.l2 = Label(self.main_frame,
                        text = prompt2)
        self.l2.pack(side = TOP, pady = (15, 10))

        self.num_samples_entry = Entry(self.main_frame, width = "20")
        self.num_samples_entry.pack(side = TOP)
        
        self.b = Button(self.main_frame,
                        text = "next",
                        command = self._validate_timings)
        self.b.pack(side = BOTTOM, pady = (5, 15))
        
        self.main_frame.pack()
        self.root.deiconify()
        return


    def _validate_timings(self):
        """Verify inputs before altering window"""

        in1_is_float = True
        in2_is_float = True
        spaces = "    "
        in1 = self.full_rot_entry.get()
        #print "in1: %s"%in1
        in2 = self.num_samples_entry.get()
        #print "in2: %s"%in2
        
        err_msg = "invalid input:%s\n" % spaces
        
        try:
            self.full_rot_time = float(in1)
        except ValueError:
            in1_is_float = False
            err_msg += "%s\n" % (spaces + in1 + spaces + spaces)
            
        try:
            self.num_samples = float(in2)
        except ValueError:
            in2_is_float = False
            err_msg += "%s\n" % (spaces + in2 + spaces + spaces)

            
        if not in1_is_float or not in2_is_float:
            tkMessageBox.showerror("Error",err_msg)
        else:
            self._select_scanning_dir_prompt()
        return

    def _select_scanning_dir_prompt(self):
        """Verify validity of inputs, choose dir to save images
        Inform user set up is done"""

        self._clear_main_frame()

        prompt = "select empty directory to put everything"
        self.l = Label(self.main_frame, text = prompt)
        self.l.pack(side = TOP, pady = (15, 10))

        self.b = Button(self.main_frame,
                        text = "select",
                        command = self._select_scanning_dir)
        self.b.pack(side = BOTTOM, pady = (5, 15))

        self.main_frame.pack()
        #ask for dir to put everything
        #make sure the program can write to and read from the given dir
        #invalid dir -> IOError 2
        #cannot read from dir -> IOError 13
        #cannot write to dir -> IOError 13


        #print(filename)

    def _select_scanning_dir(self):
        #filename = tkFileDialog.askopenfilename(initialdir = "/")
        title = "Save Directory"
        
        #verify directory is usable
        bad_dir, write_ok, read_ok = True, False, False
        test_file_name = "test_dir.tmp"
        write_string = "13243546576879809"
        err_msg = "bad directory    "
        while bad_dir:

            self.save_dir = tkFileDialog.askdirectory(title = title)
            #print "dir: %s" % self.save_dir

            #write to
            try:
                w = open(self.save_dir + test_file_name, 'w')
                w.write(write_string)
                w.close()
                write_ok = True
            except IOError:
                write_ok = False
            #read from
            try:
                r = open(self.save_dir + test_file_name, 'r')
                line = r.read()
                r.close()
                read_ok = True
            except IOError:
                read_ok = False

            if write_ok and read_ok:
                bad_dir = False
            else:
                tkMessageBox.showerror("Error",err_msg)
                bad_dir = True

            try:
                os.remove(self.save_dir + test_file_name)
            except:
                pass
        #end of while bad_dir
        print "project dir: %s" % self.save_dir
        #write important stuff to the given dir and wrap up set up
        self.root.quit()
            
win = Window()

win.setup()
    #win.set_boundaries()
    #win.set_rotational_axis()
    #win.get_scan_info() - img capture freq or stats to calc it
    #win.setup_wait() - sit idle with video feed and overlay
    ## of boundaries waiting for user to begin scanning

#win.scan()
