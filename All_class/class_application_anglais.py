import pathlib, os, random, math, json, threading
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.font import Font
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
        self.root_width,self.root_height = 1230,640
        self.root_posx,self.root_posy = 5,5
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
        #Dictionnary of the general settings of each sections of the GUI
        self.gui_build = {
            "status_bar":{          "posx":0,  "posy":595,  "width":1230,    "height":20,   "color":"#ffffff"},
            "frame_settings":{      "posx":5,  "posy":5,  "width":500,    "height":340,   "color":"#4A6572"},
            "frame_buttons":{       "posx":5,  "posy":297, "width":500,     "height":70,     "color":"#4A6572"}, #Pas le même système de width-height
            "canvas_graph":{        "posx":5,  "posy":372, "width":503,    "height":218,   "color":"#4A6572"},
            "canvas_chairs":{       "posx":510, "posy":3,  "width":710,    "height":587,   "color":"#4A6572"}}


        #Set up the 5 GUI sections
        self.frame_settings = Frame(self.root,width=self.gui_build["frame_settings"]["width"],height=self.gui_build["frame_settings"]["height"],bg=self.gui_build["frame_settings"]["color"])
        self.frame_settings.place(x=self.gui_build["frame_settings"]["posx"], y=self.gui_build["frame_settings"]["posy"])
        self.frame_buttons = Frame(self.root,width=self.gui_build["frame_buttons"]["width"],height=self.gui_build["frame_buttons"]["height"],bg=self.gui_build["frame_buttons"]["color"])
        self.frame_buttons.place(x=self.gui_build["frame_buttons"]["posx"], y=self.gui_build["frame_buttons"]["posy"])
        self.canvas_graph = Canvas(self.root,width=self.gui_build["canvas_graph"]["width"],height=self.gui_build["canvas_graph"]["height"],bg=self.gui_build["canvas_graph"]["color"])
        self.canvas_graph.place(x=self.gui_build["canvas_graph"]["posx"], y=self.gui_build["canvas_graph"]["posy"])
        self.canvas_chairs = Canvas(self.root,width=self.gui_build["canvas_chairs"]["width"],height=self.gui_build["canvas_chairs"]["height"],bg=self.gui_build["canvas_chairs"]["color"])
        self.canvas_chairs.place(x=self.gui_build["canvas_chairs"]["posx"], y=self.gui_build["canvas_chairs"]["posy"])
        self.status_bar = Label(self.root, text="Choose your settings        ", anchor="e")
        self.status_bar.place(x=self.gui_build["status_bar"]["posx"], y=self.gui_build["status_bar"]["posy"],width=self.gui_build["status_bar"]["width"],height=self.gui_build["status_bar"]["height"])

        #Dictionnary of the actual settings chose by the user
        self.gui_settings = {
                "Data_name":"",
                "Data_path":"",
                "Algorithm":"",
                "Iterations":100,
                "Time":10,
                "Distance":2.0,
                "Group_approach":0}

        #Settings - Settings
        self.label_data = Label(self.frame_settings, text="Settings",width=45,bg="#4A6572",fg="#ffffff",font=20)
        self.label_data.grid(row=0,column=0,columnspan=3)
        
        #Settings - Data
        self.label_data = Label(self.frame_settings, text="Data",anchor="w",bg="#4A6572",fg="#ffffff", width=10)
        self.label_data_actual = Label(self.frame_settings,text=self.gui_settings["Data_name"],anchor="w",bg="#4A6572",fg="#ffffff",width=20)
        self.button_data = Button(self.frame_settings, text="Choose a data set",command=self.pick_file, fg="#000000",width=25, height=1)

        self.label_data.grid(       row=1,  column=0,   columnspan=1, sticky="w",   padx=(10,10),   pady=(10,0))
        self.label_data_actual.grid(row=1,  column=1,   columnspan=1, sticky="w",   padx=(10,10),   pady=(10,0))
        self.button_data.grid(      row=1,  column=2,   columnspan=1, sticky="e",   padx=(0,10),    pady=(10,10))

        #Settings - Algorithm
        #List of the available algorithm
        self.algorithm_list = ["Au hasard","Plus proche voisin","Plus proche voisin pondéré", "Plus loin voisin pondéré"]
        self.label_algorithm = Label(self.frame_settings, text="Algorithm",anchor="w",bg="#4A6572",fg="#ffffff")
        self.label_algorithm_actual = Label(self.frame_settings,text=self.gui_settings["Algorithm"],anchor="w",bg="#4A6572",fg="#ffffff")
        self.combobox_algorithm = ttk.Combobox(self.frame_settings, values=self.algorithm_list, state="readonly",width=27, height=1)
        self.combobox_algorithm.set("Choose an algorithm")
        self.combobox_algorithm.bind("<<ComboboxSelected>>",self.comboclick)
        
        self.label_algorithm.grid(          row=2,  column=0,   columnspan=1, sticky="w",   padx=(10,10),   pady=(10,0))
        self.label_algorithm_actual.grid(   row=2,  column=1,   columnspan=1, sticky="w",   padx=(10,10),   pady=(10,0))
        self.combobox_algorithm.grid(       row=2,  column=2,   columnspan=1, sticky="e",   padx=(0,10),    pady=(10,10))

        #Settings - Iteration
        self.iteration_var = IntVar(value=int(self.gui_settings["Iterations"]))
        self.label_iteration = Label(self.frame_settings, text="Number of iterations",width=20,height=1,anchor="w",bg="#4A6572",fg="#ffffff")
        self.label_scale_iteration_actual = Label(self.frame_settings,width=10, textvariable=self.iteration_var,anchor="w",bg="#4A6572",fg="#ffffff")
        self.scale_iteration = Scale(self.frame_settings, from_=50, to=10000,resolution=50, orient=HORIZONTAL,width=15,length=100,showvalue=0, variable=self.iteration_var,command=self.scale_iteration,state=DISABLED)
        
        self.label_iteration.grid(                  row=3,  column=0,   columnspan=1, sticky="w",   padx=(10,10),   pady=(10,0))
        self.label_scale_iteration_actual.grid(     row=3,  column=1,   columnspan=1, sticky="w",   padx=(10,10),   pady=(10,0))
        self.scale_iteration.grid(                  row=3,  column=2,   columnspan=1, sticky="e",   padx=(10,30),    pady=(10,10))

        #Settings - Maximum time
        self.maximum_time_var = IntVar(value=int(self.gui_settings["Time"]))
        self.label_maximum_time = Label(self.frame_settings, text="Maximum time (minutes)",width=20,height=1,anchor="w",bg="#4A6572",fg="#ffffff")
        self.label_maximum_time_actual = Label(self.frame_settings,width=10,textvariable=self.maximum_time_var,anchor="w",bg="#4A6572",fg="#ffffff")
        self.scale_maximum_time = Scale(self.frame_settings, from_=5, to=120,resolution=5, orient=HORIZONTAL,width=15,length=100,showvalue=0, variable=self.maximum_time_var,command=self.scale_time, state=DISABLED)
        
        self.label_maximum_time.grid(       row=4,  column=0,   columnspan=1, sticky="w",   padx=(10,10),    pady=(10,0))
        self.label_maximum_time_actual.grid(row=4,  column=1,   columnspan=1, sticky="w",   padx=(10,10),    pady=(10,0))
        self.scale_maximum_time.grid(       row=4,  column=2,   columnspan=1, sticky="e",   padx=(10,30),    pady=(10,10))

        #Settings - Distance
        self.distance_var = DoubleVar(value=float(self.gui_settings["Distance"]))
        self.label_distance = Label(self.frame_settings, text="Distance (meters)",width=20,height=1,anchor="w",bg="#4A6572",fg="#ffffff")
        self.label_distance_actual = Label(self.frame_settings,width=10,textvariable=self.distance_var,anchor="w",bg="#4A6572",fg="#ffffff")
        self.scale_distance = Scale(self.frame_settings, from_=0.1, to=5.00,resolution=0.1, orient=HORIZONTAL,width=15,length=100,showvalue=0, variable=self.distance_var,command=self.scale_distance, state=DISABLED)
        
        self.label_distance.grid(       row=5,  column=0,   columnspan=1, sticky="w",   padx=(10,10),    pady=(10,0))
        self.label_distance_actual.grid(row=5,  column=1,   columnspan=1, sticky="w",   padx=(10,10),    pady=(10,0))
        self.scale_distance.grid(       row=5,  column=2,   columnspan=1, sticky="e",   padx=(10,30),    pady=(10,10))

        #Settings - Group_approach
        self.group_approach = BooleanVar()
        self.label_group_approach = Label(self.frame_settings, text="Use the group approach",width=20,height=1,anchor="w",bg="#4A6572",fg="#ffffff")
        self.button_group_approach = Checkbutton(self.frame_settings,text="", variable = self.group_approach,state=DISABLED, width=20, height=1, command=self.use_group)
        
        #self.group_approach.set(False)
        self.label_group_approach.grid(         row=6,  column=0,   columnspan=1, sticky="w",   padx=(10,10),    pady=(10,0))
        self.button_group_approach.grid(        row=6,  column=2,   columnspan=1, sticky="e",   padx=(10,20),    pady=(10,10))

        #Button - Optimization
        self.button_optimisation = Button(self.frame_buttons,text="Optimize the room!",command=self.optimization,bg="#F9AA33",fg="#000000",state=DISABLED, width=41, height=3)
        self.button_optimisation.grid(  row=0,  column=0,   columnspan=2,   rowspan=2,  sticky="w",   padx=(10,10),    pady=(10,10))
        
        #Button - Show Radius button
        self.show_radius = BooleanVar()
        self.show_radius.set(False)

        self.button_show_radius = Checkbutton(self.frame_buttons,text="Display the radius",command=self.radius_group, variable = self.show_radius,state=DISABLED, width=20, height=1)
        self.button_show_radius.grid(  row=0,  column=2,   columnspan=1, sticky="e",   padx=(10,10),    pady=(10,0))

        #Button - Show groups
        self.show_groups = BooleanVar()
        self.show_groups.set(False)

        self.button_show_groups = Checkbutton(self.frame_buttons,text="Display the groups",command=self.radius_group, variable = self.show_groups,state=DISABLED, width=20, height=1) 
        self.button_show_groups.grid(  row=1,  column=2,   columnspan=1, sticky="e",   padx=(10,10),    pady=(10,10))
    
        #Default variable
        self.duree = 0
        self.nb_group = 1

    def draw_graph(self):
        #Variables to count the number of sit and unsit chairs
        self.count_use = 0
        self.count_notuse = 0
        for each in self.chairs:
            if each[4] == True: self.count_use += 1
            else: self.count_notuse += 1
        self.count_total = self.count_use + self.count_notuse
         #"width":503,    "height":258
        #Draw the new graph after deleting the old one
        self.canvas_graph.delete("all")
        coordinates_arc = 10,20,200,200
        coordinates_rect_use = 220,20,250,50
        coordinates_rect_notuse = 220,60,250,90
        coordinates_text_use = 260,35
        coordinates_text_notuse = 260,75
        coordinates_count_use = 410,35
        coordinates_count_notuse = 410,75
        coordinates_time = 490,170
        coordinates_group = 490,200
        use_end = 360*(float(self.count_use) / float(self.count_total))
        arc = self.canvas_graph.create_arc(coordinates_arc, start=0, extent=use_end, fill="green")
        arc = self.canvas_graph.create_arc(coordinates_arc, start=use_end, extent=(359.9999-use_end), fill="gray")
        rect = self.canvas_graph.create_rectangle(coordinates_rect_use,fill="green")
        rect = self.canvas_graph.create_rectangle(coordinates_rect_notuse, fill="gray")
        text = self.canvas_graph.create_text(coordinates_text_use, text = "Used chairs", anchor="w",font=20)
        text = self.canvas_graph.create_text(coordinates_text_notuse, text = "Unused chairs", anchor="w",font=20)
        text = self.canvas_graph.create_text(coordinates_count_use, text = str(self.count_use), anchor="w",font=20)
        text = self.canvas_graph.create_text(coordinates_count_notuse, text = str(self.count_notuse), anchor="w",font=20)

        text = self.canvas_graph.create_text(coordinates_time, text = f"{round(self.duree,2)} secondes", anchor="e")
        text = self.canvas_graph.create_text(coordinates_group, text = f"{int(self.nb_group)} groups", anchor="e")
    def comboclick(self,event):
        self.button_show_radius.configure(state=DISABLED)
        self.button_show_groups.configure(state=DISABLED)
        self.gui_settings["Algorithm"] = str(self.combobox_algorithm.get())
        self.label_algorithm_actual.configure(text = self.gui_settings["Algorithm"])
        self.combobox_algorithm.set("Choose an algorithm")

    def scale_iteration(self,value):
        self.button_show_radius.configure(state=DISABLED)
        self.button_show_groups.configure(state=DISABLED)
        self.gui_settings["Iterations"] = int(value)
    
    def scale_time(self,value):
        self.button_show_radius.configure(state=DISABLED)
        self.button_show_groups.configure(state=DISABLED)
        self.gui_settings["Time"] = int(value)

    def scale_distance(self,value):
        self.button_show_radius.configure(state=DISABLED)
        self.button_show_groups.configure(state=DISABLED)
        self.gui_settings["Distance"] = float(value)
    def use_group(self):
        self.button_show_radius.configure(state=DISABLED)
        self.button_show_groups.configure(state=DISABLED)
        group = self.group_approach.get()
        self.gui_settings["Group_approach"] = bool(group)

    def radius_group(self):
        radius = self.show_radius.get()
        groups = self.show_groups.get()
        self.draw_chairs(state="after",radius=radius,groups=groups)
    def pick_file(self,reoptimize=False):
        self.button_show_radius.configure(state=DISABLED)
        self.button_show_groups.configure(state=DISABLED)
        self.button_optimisation.configure(state=DISABLED)
        #Choose a data file in the browser
        file_path = filedialog.askopenfilename(
            parent=self.root, initialdir=pathlib.Path(__file__).parent.parent / "Data",
            title='Choose file',
            filetypes=[('txt files', '.txt')]
            )
        file_name = os.path.basename(os.path.normpath(file_path))
        try:
            self.gui_settings["Data_path"] = file_path
            self.gui_settings["Data_name"] = file_name
            self.label_data_actual.configure(text=self.gui_settings["Data_name"])
            self.data = Salles(app=True)
            self.room, self.chairs = self.data.chairs_list(self.gui_settings["Data_path"])
            #Draw all the chairs as empty (before)
            self.duree = 0
            self.nb_group = 1
            self.draw_graph()
            self.draw_chairs("before")
            
            
            #Activate the scales and the button
            self.scale_iteration.configure(state=NORMAL)
            self.scale_maximum_time.configure(state=NORMAL)
            self.scale_distance.configure(state=NORMAL)
            self.button_group_approach.configure(state=NORMAL)
            self.button_optimisation.configure(state=NORMAL)
        except:
            print("Fichier non valide")

    def optimization(self):
        
        for chair in range(0,len(self.chairs)):
            self.chairs[chair][4] = bool(0)
            while len(self.chairs[chair])>=6:
                self.chairs[chair].pop(-1)
        #optimisation
        if self.gui_settings["Algorithm"] == "Au hasard": methode = 1
        elif self.gui_settings["Algorithm"] == "Plus proche voisin": methode = 2
        elif self.gui_settings["Algorithm"] == "Plus loin voisin": methode = 3
        elif self.gui_settings["Algorithm"] == "Plus proche voisin pondéré": methode = 4
        elif self.gui_settings["Algorithm"] == "Plus loin voisin pondéré": methode = 5

        opti = Voisins_exclus(self.chairs,
            float(self.gui_settings["Distance"]),
            int(self.gui_settings["Iterations"]),
            int(self.gui_settings["Time"]),
            int(methode), #methode
            int(self.gui_settings["Group_approach"])) #division
        self.chairs, self.duree = opti.optimize()

        self.nb_group = 1
        for chair in self.chairs:
            if chair[5] > self.nb_group:
                self.nb_group = chair[5]
        self.draw_graph()
        self.draw_chairs("after")
        
        
        self.button_show_radius.configure(state=NORMAL)
        self.button_show_groups.configure(state=NORMAL)
        self.status_bar.configure(text="Optimization done        ")

    def draw_chairs(self,state,radius=False,groups=False):
        #Scale the room to fit all the desk proportionally
        width_height = self.gui_build["canvas_chairs"]["width"] / self.gui_build["canvas_chairs"]["height"]
        canvas_chairs_meter_width = self.gui_build["canvas_chairs"]["width"] * (60/6400) #1 desk is 64x64 pixel and 60 cm in real transform in meter
        canvas_chairs_meter_height = self.gui_build["canvas_chairs"]["height"] * (60/6400)
        #If the size of width of the room is the dominant size (if the width fit, the heigher will fit)
        if self.room["width"] >= (width_height)*self.room["height"]:
            scale = self.gui_build["canvas_chairs"]["width"] / self.room["width"]
            scale_size = 1 + (canvas_chairs_meter_width - self.room["width"])/self.room["width"]
            pos_x_buffer = 0
            pos_y_buffer = 0.5 * (self.gui_build["canvas_chairs"]["height"] - ( self.room["height"] * scale ))
        #If the size of height of the room is the dominant size (if the height fit, the width will fit)
        else:
            scale = self.gui_build["canvas_chairs"]["height"] / self.room["height"]
            scale_size = 1 + (canvas_chairs_meter_height - self.room["width"])/self.room["width"]
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

        #64 pixel = 60 cm    espace = 700x600 pixel 6,56 x 5,62 metres

        #Draw the chairs
        self.canvas_chairs.delete("all")
        self.list_color = []
        for chair in self.chairs: 
            pos_x = (chair[2]*scale) + pos_x_buffer
            pos_y = self.gui_build["canvas_chairs"]["height"] - ((chair[3] * scale) + pos_y_buffer)
            orientation = chair[1]
            if state == "before":
                self.canvas_chairs.create_image(pos_x, pos_y, image=self.desk[orientation]["brown"])
            elif state == "after":
                if chair[4] == True:
                    self.canvas_chairs.create_image(pos_x, pos_y, image=self.desk[orientation]["green"])
                    if radius == True: 
                        circle_radius = int(float(self.gui_settings["Distance"])*scale)
                        self.canvas_chairs.create_oval((pos_x - circle_radius),(pos_y - circle_radius),(pos_x + circle_radius),(pos_y + circle_radius),width=2,outline="#00ff0d")
                else:
                    self.canvas_chairs.create_image(pos_x, pos_y, image=self.desk[orientation]["brown"])
                if groups == True:
                    while len(self.list_color) <= int(chair[5]): #create a new color for each group
                        pick_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                        if pick_color not in self.list_color:
                            self.list_color.append(pick_color)
                    side = int(new_desk_size/2)
                    self.canvas_chairs.create_rectangle((pos_x - side),(pos_y - side),(pos_x + side),(pos_y + side),width=2,outline=self.list_color[int(chair[5])])