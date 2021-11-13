import pathlib, os, random, math, json, threading
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image,ImageTk,ImageGrab
from sys import exit
from All_class.class_dataset import Salles
from All_class.class_optimization_random import Optimization_random
from All_class.class_optimization_des_sections import Optimization_des_sections
from All_class.class_voisins_exclus import Voisins_exclus

class Application():
    def __init__(self):
        #Global settings of the main window
        self.root = Tk()
        self.root.title("Optimisation de chaises App")
        self.root.iconbitmap(pathlib.Path(__file__).parents[1] / "Font_graphics/icon.ico")
        self.root_width,self.root_height = 1030,620
        self.root_posx,self.root_posy = 20,20
        self.root.geometry(f"{self.root_width}x{self.root_height}+{self.root_posx}+{self.root_posy}")
        self.root.resizable(False,False)
        #Function menu and gui to set up the menu bar and the gui interface
        self.menu()
        self.gui()
        self.root.mainloop()
    def menu(self):
        #Global menu
        self.root_menu = Menu(self.root)
        self.root.config(menu=self.root_menu)
        #File menu
        self.file_menu = Menu(self.root_menu)
        self.root_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New file", command=self.gui)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        #Export menu
        self.export_menu = Menu(self.root_menu)
        self.root_menu.add_cascade(label="Export", menu=self.export_menu)
        self.export_menu.add_command(label="Export the results as .txt", command=self.export_results)
        #Help menu
        self.help_menu = Menu(self.root_menu)
        self.root_menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.about)

    def export_results(self):
        # try:
        path_file= filedialog.asksaveasfilename(
            defaultextension='.txt', filetypes=[("Txt files", '*.txt')],
            initialdir=pathlib.Path(__file__).parent.parent / "Export_files",
            title="Save As")
        with open(path_file, 'w') as f:
            f.write(f"num\torient\tpos_x\tpos_y\tuse\n")
            for chair in self.chairs:
                line = f"{chair[0]}\t{chair[1]}\t{chair[2]}\t{chair[3]}\t{True if int(chair[4]) == 1 else False}\n"
                f.write(line)
            f.write(
                f"\nUse chairs:\t{self.count_use}\t-> {round(100*(float(self.count_use)/float(self.count_total)),2)}%\n"
                f"Unused chairs:\t{self.count_notuse}\t-> {round(100*(float(self.count_notuse)/float(self.count_total)),2)}%\n"
                f"Total chairs:\t{self.count_total}\t-> {100.00}%\n")

    def about(self):
        root_about = Tk()
        root_about.title("About")
        root_about.iconbitmap(pathlib.Path(__file__).parents[1] / "Font_graphics/about.ico")
        root_about_width,root_about_height = 200,200
        root_about_posx,root_about_posy = 20,20
        root_about.geometry(f"{root_about_width}x{root_about_height}+{root_about_posx}+{root_about_posy}")
        root_about.resizable(False,False)
        about_text = Label(root_about, text=
            "Build by:\n\tEmanuel Senay-Lussier\n\tOlivier Simard-Hanley\n\tMahnaz Golshan", anchor="nw")
        about_text.pack(fill="both")
        root_about.mainloop()
    def gui(self):
        #Parameters of the gui_build
        self.gui_build = {
            "status_bar":{          "posx":0,  "posy":580,  "width":1030,    "height":20,   "color":"#ffffff"},
            "frame_settings":{      "posx":10,  "posy":10,  "width":300,    "height":330,   "color":"#bbf3df"},
            "button_optimisation":{ "posx":10,  "posy":340, "width":42,     "height":1,     "color":"yellow"}, #Pas le même système de width-height
            "canvas_graph":{        "posx":10,  "posy":370, "width":300,    "height":210,   "color":"#bbcff3"},
            "canvas_chairs":{       "posx":320, "posy":10,  "width":700,    "height":570,   "color":"#f3bfbb"}}

        #Set up the 5 gui sectors
        self.frame_settings = LabelFrame(self.root,text="Settings",width=self.gui_build["frame_settings"]["width"],height=self.gui_build["frame_settings"]["height"],bg=self.gui_build["frame_settings"]["color"])
        self.frame_settings.place(x=self.gui_build["frame_settings"]["posx"], y=self.gui_build["frame_settings"]["posy"])
        self.button_optimisation = Button(self.root,text="Optimize the room!",width=self.gui_build["button_optimisation"]["width"],height=self.gui_build["button_optimisation"]["height"],command=self.optimization,bg=self.gui_build["button_optimisation"]["color"],state=DISABLED)
        self.button_optimisation.place(x=self.gui_build["button_optimisation"]["posx"], y=self.gui_build["button_optimisation"]["posy"])
        self.canvas_graph = Canvas(self.root,width=self.gui_build["canvas_graph"]["width"],height=self.gui_build["canvas_graph"]["height"],bg=self.gui_build["canvas_graph"]["color"])
        self.canvas_graph.place(x=self.gui_build["canvas_graph"]["posx"], y=self.gui_build["canvas_graph"]["posy"])
        self.canvas_chairs = Canvas(self.root,width=self.gui_build["canvas_chairs"]["width"],height=self.gui_build["canvas_chairs"]["height"],bg=self.gui_build["canvas_chairs"]["color"])
        self.canvas_chairs.place(x=self.gui_build["canvas_chairs"]["posx"], y=self.gui_build["canvas_chairs"]["posy"])
        self.status_bar = Label(self.root, text="Choose your settings        ", anchor="e")
        self.status_bar.place(x=self.gui_build["status_bar"]["posx"], y=self.gui_build["status_bar"]["posy"],width=self.gui_build["status_bar"]["width"],height=self.gui_build["status_bar"]["height"])

        self.gui_settings = {
                "Data_name":"",
                "Data_path":"",
                "Algorithm":"",
                "Iterations":100,
                "Time":10,
                "Distance":2}

        #Settings - Data
        self.label_data = Label(self.frame_settings, text="Data",width=20,height=1,anchor="w")
        self.label_data.grid(row=0,column=0)
        self.label_data_actual = Label(self.frame_settings,text=self.gui_settings["Data_name"],width=21,height=1,anchor="w",bg="#ffffff")
        self.label_data_actual.grid(row=0,column=1)
        self.button_data = Button(self.frame_settings, text="Choose a data set", width=37,command=self.pick_file, fg="#000000")
        self.button_data.grid(row=1, column=0, columnspan=2,pady=(0,10))

        #Settings - Algorithm
        #List of the available algorithm
        self.algorithm_list = ["Voisins exclus", "Optimization_des_sections"]
        self.label_algorithm = Label(self.frame_settings, text="Algorithm",width=20,height=1,anchor="w")
        self.label_algorithm.grid(row=2,column=0)
        self.label_algorithm_actual = Label(self.frame_settings,text=self.gui_settings["Algorithm"],width=21,height=1,anchor="w",bg="#ffffff")
        self.label_algorithm_actual.grid(row=2,column=1)
        self.combobox_algorithm = ttk.Combobox(self.frame_settings, values=self.algorithm_list, state="readonly", width=41)
        self.combobox_algorithm.set("Choose an algorithm")
        self.combobox_algorithm.grid(row=3, column=0,columnspan=2,pady=(0,10))

        #Settings - Iteration
        self.iteration_var = IntVar(value=int(self.gui_settings["Iterations"]))
        self.label_iteration = Label(self.frame_settings, text="Number of iterations",width=20,height=1,anchor="w")
        self.label_iteration.grid(row=4,column=0)
        self.label_iteration_actual = Label(self.frame_settings,text=str(self.gui_settings["Iterations"]),width=21,height=1,anchor="w",bg="#ffffff")
        self.label_iteration_actual.grid(row=4,column=1)
        self.label_scale_iteration = Label(self.frame_settings,width=10, textvariable=self.iteration_var)
        self.label_scale_iteration.grid(row=5, column=0,pady=(0,10))
        self.scale_iteration = Scale(self.frame_settings, from_=50, to=10000,resolution=50, orient=HORIZONTAL,width=15,length=147,showvalue=0, variable=self.iteration_var,state=DISABLED)
        self.scale_iteration.grid(row=5, column=1,pady=(0,10))

        #Settings - Maximum time
        self.maximum_time_var = IntVar(value=int(self.gui_settings["Time"]))
        self.label_maximum_time = Label(self.frame_settings, text="Maximum time (minutes)",width=20,height=1,anchor="w")
        self.label_maximum_time.grid(row=6,column=0)
        self.label_maximum_time_actual = Label(self.frame_settings,text=str(self.gui_settings["Time"]),width=21,height=1,anchor="w",bg="#ffffff")
        self.label_maximum_time_actual.grid(row=6,column=1)
        self.label_maximum_time = Label(self.frame_settings,width=10, textvariable=self.maximum_time_var)
        self.label_maximum_time.grid(row=7, column=0,pady=(0,10))
        self.scale_maximum_time = Scale(self.frame_settings, from_=5, to=120,resolution=5, orient=HORIZONTAL,width=15,length=147,showvalue=0, variable=self.maximum_time_var, state=DISABLED)
        self.scale_maximum_time.grid(row=7, column=1,pady=(0,10))

        #Settings - Distance
        self.distance_var = DoubleVar(value=float(self.gui_settings["Distance"]))
        self.label_distance = Label(self.frame_settings, text="Distancing (meters)",width=20,height=1,anchor="w")
        self.label_distance.grid(row=8,column=0)
        self.label_distance_actual = Label(self.frame_settings,text=str(self.gui_settings["Distance"]),width=21,height=1,anchor="w",bg="#ffffff")
        self.label_distance_actual.grid(row=8,column=1)
        self.label_distance = Label(self.frame_settings,width=10, textvariable=self.distance_var)
        self.label_distance.grid(row=9, column=0,pady=(0,10))
        self.scale_distance = Scale(self.frame_settings, from_=0.1, to=5.00,resolution=0.1, orient=HORIZONTAL,width=15,length=147,showvalue=0, variable=self.distance_var,state=DISABLED)
        self.scale_distance.grid(row=9, column=1,pady=(0,10))

        #Settings - Show distance zone
        self.show_radius = BooleanVar()
        self.show_radius.set(False)

        #Settings - Optimization button
        self.button_show_radius = Checkbutton(self.frame_settings,text="Display the distance areas", width = 35,command=self.circle, variable = self.show_radius,state=DISABLED)
        self.button_show_radius.grid(row=10, column=0, columnspan=2,pady=(0,10))
    

    def draw_graph(self):
        #Variables to count the number of sit and unsit chairs
        self.count_use = 0
        self.count_notuse = 0
        for each in self.chairs:
            if each[4] == True: self.count_use += 1
            else: self.count_notuse += 1
        self.count_total = self.count_use + self.count_notuse
        
        #Draw the new graph after deleting the old one
        self.canvas_graph.delete("all")
        coordinates_arc = 20,20,130,130
        coordinates_rect_use = 20,140,40,160
        coordinates_rect_notuse = 20,170,40,190
        coordinates_text_use = 50, 150
        coordinates_text_notuse = 50, 180
        coordinates_count_use = 180, 150
        coordinates_count_notuse = 180, 180
        use_end = 360*(float(self.count_use) / float(self.count_total))
        arc = self.canvas_graph.create_arc(coordinates_arc, start=0, extent=use_end, fill="green")
        arc = self.canvas_graph.create_arc(coordinates_arc, start=use_end, extent=(359.9999-use_end), fill="gray")
        rect = self.canvas_graph.create_rectangle(coordinates_rect_use,fill="green")
        rect = self.canvas_graph.create_rectangle(coordinates_rect_notuse, fill="gray")
        text = self.canvas_graph.create_text(coordinates_text_use, text = "Used chairs", anchor="w")
        text = self.canvas_graph.create_text(coordinates_text_notuse, text = "Unused chairs", anchor="w")
        text = self.canvas_graph.create_text(coordinates_count_use, text = str(self.count_use), anchor="w")
        text = self.canvas_graph.create_text(coordinates_count_notuse, text = str(self.count_notuse), anchor="w")

    def pick_file(self):

        #Choose a data file in the browser
        file_path = filedialog.askopenfilename(
            parent=self.root, initialdir=pathlib.Path(__file__).parent.parent / "Data",
            title='Choose file',
            filetypes=[('txt files', '.txt')]
            )
        file_name = os.path.basename(os.path.normpath(file_path))
        # try:
        self.gui_settings["Data_path"] = file_path
        self.gui_settings["Data_name"] = file_name
        self.label_data_actual.configure(text=self.gui_settings["Data_name"])
        self.data = Salles(app=True)
        self.room, self.chairs = self.data.chairs_list(self.gui_settings["Data_path"])
        #Draw all the chairs as empty (before)
        self.draw_graph()
        self.draw_chairs("before")
        #Activate the scales and the button
        self.scale_iteration.configure(state=NORMAL)
        self.scale_maximum_time.configure(state=NORMAL)
        self.scale_distance.configure(state=NORMAL)
        self.button_optimisation.configure(state=NORMAL)
        # except:
        #     print("Fichier non valide")
    def optimization(self):
        #save settings
        if self.combobox_algorithm.get() != "Choose an algorithm":
            self.gui_settings["Algorithm"] = self.combobox_algorithm.get()
            self.label_algorithm_actual.configure(text=self.gui_settings["Algorithm"])
            self.combobox_algorithm.set("Choose an algorithm")
            self.combobox_algorithm.selection_clear()
        
        self.gui_settings["Iterations"] = self.scale_iteration.get()
        self.gui_settings["Time"] = self.scale_maximum_time.get()
        self.gui_settings["Distance"] = self.scale_distance.get()
        self.label_iteration_actual.configure(text=self.gui_settings["Iterations"])
        self.label_maximum_time_actual.configure(text=self.gui_settings["Time"])
        self.label_distance_actual.configure(text=self.gui_settings["Distance"])
        for chair in range(0,len(self.chairs)):
            print("opti",chair,self.chairs[chair],self.chairs[chair][4])
            self.chairs[chair][4] = bool(0)
        print("done")
        print(self.chairs)
        #optimisation
        if self.label_algorithm_actual.cget("text") == "Voisins exclus":
            opti = Voisins_exclus(self.chairs,
                float(self.gui_settings["Distance"]),
                int(self.gui_settings["Iterations"]),
                int(self.gui_settings["Time"]))
            self.chairs, self.duree = opti.optimize()
        elif self.label_algorithm_actual.cget("text") == "Optimization_des_sections":
            opti = Optimization_des_sections(self.chairs,
                float(self.gui_settings["Distance"]),
                int(self.gui_settings["Time"]))
            self.chairs, self.time_total = opti.optimize()
        self.draw_graph()
        self.draw_chairs("after")
        self.button_show_radius.configure(state=NORMAL)
        self.status_bar.configure(text="Optimization done        ")
    def circle(self):
        #circle = distance radius
        wantcircle = self.show_radius.get()
        if wantcircle == True:
            self.draw_chairs(state="after",circle=True)
        else:
            self.draw_chairs(state="after",circle=False)

    def draw_chairs(self,state,circle=False):  
        #Scale the room to fit all the desk proportionally
        #If the size of width of the room is the dominant size (if the width fit, the heigher will fit)
        if self.room["width"] >= (7/6)*self.room["height"]:
            scale = self.gui_build["canvas_chairs"]["width"] / self.room["width"]
            scale_size = 1 + (8.203125 - self.room["width"])/self.room["width"]
            pos_x_buffer = 0
            pos_y_buffer = 0.5 * (self.gui_build["canvas_chairs"]["height"] - ( self.room["height"] * scale ))
        #If the size of height of the room is the dominant size (if the height fit, the width will fit)
        else:
            scale = self.gui_build["canvas_chairs"]["height"] / self.room["height"]
            scale_size = 1 + (7.03125 - self.room["width"])/self.room["width"]
            pos_x_buffer = 0.5 * (self.gui_build["canvas_chairs"]["width"] - ( self.room["width"] * scale ))
            pos_y_buffer = 0

        #Scale the size of 1 desk proportionally and import all the desks resized
        self.desk = {}
        new_desk_size = int(64*scale_size)
        path = f"{pathlib.Path(__file__).parents[1]}/Font_graphics/"
        desk_brown = (Image.open(f"{path}desk_brown.png")).resize((new_desk_size,new_desk_size), Image.ANTIALIAS)
        desk_green = (Image.open(f"{path}desk_green.png")).resize((new_desk_size,new_desk_size), Image.ANTIALIAS)
        desk_red = (Image.open(f"{path}desk_red.png")).resize((new_desk_size,new_desk_size), Image.ANTIALIAS)
        desk_yellow = (Image.open(f"{path}desk_yellow.png")).resize((new_desk_size,new_desk_size), Image.ANTIALIAS)
        
        for each in [["south",0],["east",90],["north",180],["west",270]]:
            self.desk_brown_rot = ImageTk.PhotoImage(desk_brown.rotate(each[1]))
            self.desk_green_rot = ImageTk.PhotoImage(desk_green.rotate(each[1]))
            self.desk_red_rot = ImageTk.PhotoImage(desk_red.rotate(each[1]))
            self.desk_yellow_rot = ImageTk.PhotoImage(desk_yellow.rotate(each[1]))

            self.desk[each[0]]  = { "brown":self.desk_brown_rot,
                                    "green":self.desk_green_rot,
                                    "red":self.desk_red_rot,
                                    "yellow":self.desk_yellow_rot}

        #64 pixel = 75 cm    espace = 700x600 pixel 8.203125 metres x 7.03125 metres

        #Draw the chairs
        self.canvas_chairs.delete("all") 
        for chair in self.chairs: 
            pos_x = (chair[2]*scale) + pos_x_buffer
            pos_y = self.gui_build["canvas_chairs"]["height"] - ((chair[3] * scale) + pos_y_buffer)
            orientation = chair[1]
            if state == "before":
                self.canvas_chairs.create_image(pos_x, pos_y, image=self.desk[orientation]["brown"])
            elif state == "after":
                if chair[4] == True:
                    self.canvas_chairs.create_image(pos_x, pos_y, image=self.desk[orientation]["green"])
                    if circle == True: #64 pixel = 75 cm --> donc distance (m) * 85.33 = nb pixel
                        radius = int(self.label_distance_actual.cget("text"))*scale
                        self.canvas_chairs.create_oval((pos_x - radius),(pos_y - radius),(pos_x + radius),(pos_y + radius),width=2,outline="#00ff0d")
                else:
                    self.canvas_chairs.create_image(pos_x, pos_y, image=self.desk[orientation]["brown"])