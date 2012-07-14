import tkinter as tk;
root = tk.Tk();

def getImage(jury_state):
    ### This is a game, where JS-es are bare strings with names of the pictures.
    return tk.PhotoImage(file="images/"+jury_state);

class FrameVisualiser(tk.Frame):
    """ This class is used for the development tools. It simply displays frames from author's painter, drawn according a 
    certain log. It allows scrolling between them and also has scrollbars in case frames are bigger, than the canvas.
    Be careful, because we use Tk graphics, which doesn't wish to paint other images, but GIF or PPM/PGM data, or X11 
    bitmap."""
    class ControlPanel(tk.Frame):
        """ This kind of frame contains control buttons and frame number indicator. """
        def __init__(self, master=None):
            tk.Frame.__init__(self, master, width=300);
            self.back_button = tk.Button(master=self, text="back", command=master.back);
            self.back_button.pack(anchor="w", side="left");
            self.forward_button = tk.Button(master=self, text="forward", command=master.forward);
            self.forward_button.pack(anchor="e", side="right");
            self.num_label = tk.Label(self, width=50);
            self.num_label.pack(anchor="center");
    
    def __init__(self, jury_states, master=None, **kw):
        """ Builds up a window, that will visualise a game by reading a jury_state list or tuple. """
        tk.Frame.__init__(self, master);
        self.jury_state_list = jury_states;
        self.frame_num = 0;
        self.control_panel = self.ControlPanel(master=self);
        self.control_panel.pack(side="bottom");
        self.frame_label = tk.Button(self, borderwidth=0, command=self.forward, width=kw["width"], height=kw["height"]);
        self.frame_label.pack(side="top");
        self.pack();
        self.draw_frame(0);
               
    def back(self):
        """ Switches to the previous frame. """
        if (self.frame_num > 0):
            self.draw_frame(self.frame_num - 1);
    
    def forward(self):
        """ Switches to the next frame """
        if (self.frame_num < len(self.jury_state_list) - 1):
            self.draw_frame(self.frame_num + 1);
    
    def get_frame_num(self):
        """ Returns the number of current frame. """
        return self.frame_num;
    
    def draw_frame(self, new_frame_number):
        """ Draws a new frame instead of the old one. new_frame_number is a number of a jury_state, which the frame will 
        be painted by. """
        self.frame_num = new_frame_number;
        self.img = getImage(self.jury_state_list[self.frame_num]);
        self.frame_label["image"] = self.img;
        self.control_panel.num_label["text"] = "Frame number " + str(self.frame_num + 1);
import os;
vis = FrameVisualiser(sorted(os.listdir("images")), master=root, width=640, height=320);
vis.mainloop();
