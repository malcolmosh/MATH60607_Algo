import pathlib, os, random, math
from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from sys import exit

class Application():
    def __init__(self):
        self.root = Tk()
        self.root.title("Chairs Optimization App")
        # self.root.iconbitmap(pathlib.Path(__file__).parents[1] / "Font_graphics/icon.png")
        print(self.root.winfo_geometry())
        self.root_width,self.root_height = 1030,620
        self.root_posx,self.root_posy = 20,20
        self.root.geometry(f"{self.root_width}x{self.root_height}+{self.root_posx}+{self.root_posy}")
        self.root.resizable(False,False)

        self.gui()
        self.root.mainloop()

    def gui(self):
        self.gui_build = {
            "canvas_chairs":{   "posx":10, "posy":10,  "width":700,    "height":600,   "color":"#f3bfbb"},
            "frame_settings":{  "posx":720,"posy":10,  "width":300,    "height":300,   "color":"#bbf3df"},
            "canvas_graph":{    "posx":720,"posy":320, "width":300,    "height":300,   "color":"#bbcff3"},
        }

        self.canvas_chairs = Canvas(self.root,width=self.gui_build["canvas_chairs"]["width"],height=self.gui_build["canvas_chairs"]["height"],bg=self.gui_build["canvas_chairs"]["color"])
        self.canvas_chairs.place(x=self.gui_build["canvas_chairs"]["posx"], y=self.gui_build["canvas_chairs"]["posy"])

        self.frame_settings = LabelFrame(self.root,text="Settings",width=self.gui_build["frame_settings"]["width"],height=self.gui_build["frame_settings"]["height"],bg=self.gui_build["frame_settings"]["color"])
        self.frame_settings.place(x=self.gui_build["frame_settings"]["posx"], y=self.gui_build["frame_settings"]["posy"])

        self.canvas_graph = Canvas(self.root,width=self.gui_build["canvas_graph"]["width"],height=self.gui_build["canvas_graph"]["height"],bg=self.gui_build["canvas_graph"]["color"])
        self.canvas_graph.place(x=self.gui_build["canvas_graph"]["posx"], y=self.gui_build["canvas_graph"]["posy"])

        self.algorithm_list = ["Voisins exclus", "Optimization random"]

        self.label_data = Label(self.frame_settings, text="Data",width=15,height=1,anchor="w")
        self.label_data.grid(row=0,column=0)
        self.label_data_actual = Label(self.frame_settings, text="a",width=26,height=1,anchor="w",bg="#ffffff")
        self.label_data_actual.grid(row=0,column=1)
        self.button_data = Button(self.frame_settings, text="Choisir un jeu de données", width=41,command=self.pick_file, fg="#000000")
        self.button_data.grid(row=1, column=0, columnspan=2,pady=(0,10))

        self.label_algorithm = Label(self.frame_settings, text="Algorithme",width=15,height=1,anchor="w")
        self.label_algorithm.grid(row=2,column=0)
        self.label_algorithm_actual = Label(self.frame_settings, text="b",width=26,height=1,anchor="w",bg="#ffffff")
        self.label_algorithm_actual.grid(row=2,column=1)
        self.combobox_algorithm = ttk.Combobox(self.frame_settings, values=self.algorithm_list, state="readonly")
        self.combobox_algorithm.set("Choisir un algorithme")
        self.combobox_algorithm.grid(row=3, column=0,columnspan=2,pady=(0,10))


        self.iteration_var = IntVar(value=100)
        self.label_iteration = Label(self.frame_settings, text="Nombre d'itération",width=15,height=1,anchor="w")
        self.label_iteration.grid(row=4,column=0)
        self.label_iteration_actual = Label(self.frame_settings, text="c",width=26,height=1,anchor="w",bg="#ffffff")
        self.label_iteration_actual.grid(row=4,column=1)
        self.entry_iteration = Entry(self.frame_settings,width=15, textvariable=self.iteration_var)
        self.entry_iteration.grid(row=5, column=0,pady=(0,10))
        self.scale_iteration = Scale(self.frame_settings, from_=1, to=1000, orient=HORIZONTAL,width=15,length=180,showvalue=0, variable=self.iteration_var)
        self.scale_iteration.grid(row=5, column=1,pady=(0,10))

        self.maximum_time_var = IntVar(value=5)
        self.label_maximum_time = Label(self.frame_settings, text="Durée maximale",width=15,height=1,anchor="w")
        self.label_maximum_time.grid(row=6,column=0)
        self.label_maximum_time_actual = Label(self.frame_settings, text="d",width=26,height=1,anchor="w",bg="#ffffff")
        self.label_maximum_time_actual.grid(row=6,column=1)
        self.entry_maximum_time = Entry(self.frame_settings,width=15, textvariable=self.maximum_time_var)
        self.entry_maximum_time.grid(row=7, column=0,pady=(0,10))
        self.scale_maximum_time = Scale(self.frame_settings, from_=1, to=1000, orient=HORIZONTAL,width=15,length=180,showvalue=0, variable=self.maximum_time_var)
        self.scale_maximum_time.grid(row=7, column=1,pady=(0,10))

        self.button_save = Button(self.frame_settings, text="Changer les paramètres", width=30,height=1,command=self.change_settings, fg="#000000")
        self.button_save.grid(row=8, column=0, columnspan=2,pady=(0,10))

        self.show_radius = IntVar()
        self.button_show_radius = Checkbutton(self.frame_settings,text="Afficher les rayons de distanciation", width = 30, variable = self.show_radius)
        self.button_show_radius.grid(row=9, column=0, columnspan=2,pady=(0,10))

        coordinates = 20,20,220,220
        arc = self.canvas_graph.create_arc(coordinates, start=0, extent=250, fill="blue")
        arc = self.canvas_graph.create_arc(coordinates, start=250, extent=50, fill="red")
        arc = self.canvas_graph.create_arc(coordinates, start=300, extent=60, fill="yellow")
        # self.canvas_graph.pack()

    def change_settings(self):
        self.label_algorithm_actual.configure(text=self.combobox_algorithm.get())
        self.combobox_algorithm.set("Choisir un algorithme")
        self.combobox_algorithm.selection_clear()

        self.label_iteration_actual.configure(text=self.scale_iteration.get())
        self.label_maximum_time_actual.configure(text=self.scale_maximum_time.get())

    def pick_file(self):
        self.file_path = tkinter.filedialog.askopenfilename(
            parent=self.root, initialdir=pathlib.Path(__file__).parent.parent,
            title='Choose file',
            filetypes=[('txt files', '.txt')]
            )
        file_name = os.path.basename(os.path.normpath(self.file_path))
        self.label_data_actual.configure(text=file_name)

app = Application()