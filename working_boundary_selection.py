from Tkinter import *
from time import sleep
import cv2

def nothing():
    pass
def p():
    print "yooo!"

class Window():
    def __init__(self):
        self.root = Tk()
        self.window_width  = "500"
        self.window_height = "200"
        
        self.root.geometry(self.window_width +
                           "x" +
                           self.window_height)

        self.prompt = "Please provide a boundary to consider"
        self.l = Label(self.root, text=self.prompt)
        self.l.pack(side=TOP)

        self.b = Button(self.root,
                   text="next",
                        command=self.next_button)
        self.b.pack(side=BOTTOM)
        #remove this counter
        self.bound_count = 0

        self.root.mainloop()
        
    def nothing(self):
        pass
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
        elif self.bound_count == 2:
            #top
            self.top_bound = (new_x, new_y)
            print "top    bound: {}".format(self.top_bound)
        elif self.bound_count == 3:
            #right
            self.right_bound = (new_x, new_y)
            print "right  bound: {}".format(self.right_bound)
        elif self.bound_count == 4:
            #bottom
            self.bottom_bound = (new_x, new_y)
            print "bottom bound: {}".format(self.bottom_bound)
        self.root.deiconify()
            
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




            
win = Window()
