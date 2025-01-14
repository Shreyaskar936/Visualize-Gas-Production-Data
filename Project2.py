from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from PIL import Image, ImageTk, ImageOps

data = pd.read_csv(r"Project2\Monthly_Production_Volume_Students.csv")
data['PRODUCTION_DATE'] = pd.to_datetime(data['PRODUCTION_DATE'], format='%d-%b-%y')
data['QUARTER'] = data['PRODUCTION_DATE'].dt.quarter

data_years = ["All"] + sorted(data['PRODUCTION_DATE'].dt.year.unique(), reverse=True)
fields = ["All"] + sorted(data['FIELD'].unique())
layers = ["All"] + sorted(data['LAYER_NAME'].unique())

root = Tk()
root.title("GAS PRODUCTION (Quarterly)")
root.geometry("1100x860")
root.config(bg="#AF8260")

def plot():
    selected_year = year.get()
    selected_quarter = quarter.get()
    selected_field = field.get()
    selected_layer = layer.get()
    selected_option = select.get()

    if selected_year == "All":
        filtered_data = data.copy()
    else:
        selected_year = int(selected_year)
        filtered_data = data[data['PRODUCTION_DATE'].dt.year == selected_year]

    if selected_quarter != "All":
        selected_quarter_num = int(selected_quarter[1])
        filtered_data = filtered_data[filtered_data['QUARTER'] == selected_quarter_num]

    if selected_option == 0 and selected_field != 'All':
        filtered_data = filtered_data[filtered_data['FIELD'] == selected_field]
    elif selected_option == 1 and selected_layer != 'All':
        filtered_data = filtered_data[filtered_data['LAYER_NAME'] == selected_layer]

    for widget in f2.winfo_children():
        widget.destroy()

    if filtered_data.empty:
        fig, ax = plt.subplots(figsize=(13.8, 8.3))
        ax.text(
            0.5, 0.5, 'No Records\nAvailable', 
            fontsize=45, ha='center', va='center', 
            color='gray', fontname='Arial Rounded MT Bold'
        )
        ax.axis('off')
    else:
        gas_volume_by_well = filtered_data.groupby('WELL_NAME')['GAS_VOLUME'].sum()
        fig, ax = plt.subplots(figsize=(13.8, 8.3))
        plt.subplots_adjust(left=0.069, right=0.97, top=0.926, bottom=0.12)
        x = gas_volume_by_well.index  
        y = gas_volume_by_well.values 
        bw = 0.7
        if len(x) < 4:
           bw = 0.2
           ax.set_xlim(-0.5, len(x) - 0.5)
        ax.scatter(x, y, color="#ff1414", s=70, zorder=1) 
        ax.bar(x, y, color='#38070f', edgecolor='black', zorder=2, width=bw)      
        ax.plot(x, y, color='#d11f7b', linewidth=3, zorder=3)
        
        if selected_option == 0:
            ax.set_title(f'Quarterly Production for Field: {selected_field}, Year: {selected_year}, Quarter: {selected_quarter}', 
                         fontsize=20, fontname='Arial Rounded MT Bold')
        else:
            ax.set_title(f'Quarterly Production for Sand: {selected_layer}, Year: {selected_year}, Quarter: {selected_quarter}', 
                         fontsize=20, fontname='Arial Rounded MT Bold')
        ax.set_xlabel('Well Name', fontsize=16, fontname='Arial Rounded MT Bold')
        ax.set_ylabel('Gas Volume (units=SCM)', fontsize=16, fontname='Arial Rounded MT Bold')
        ax.tick_params(axis='x', rotation=45)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, which='both', linestyle='--', linewidth=0.7, color='gray')
        ax.set_axisbelow(True)
        y_min, y_max = ax.get_ylim()
        y_range = y_max - y_min
        if y_range > 0:
            tick_interval = y_range / 10
            ticks = [round(y_min + tick_interval * i, 2) for i in range(11)] 
            ax.set_yticks(ticks)

    canvas = FigureCanvasTkAgg(fig, master=f2)
    canvas.draw()

    toolbar_frame = Frame(f2)
    toolbar_frame.pack(side=TOP, fill=X)

    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()

    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

def clear():
    for widget in f2.winfo_children():
        widget.destroy()
    f2.config(bg="#AF8260")
    year.current(0)
    quarter.current(0)
    field.current(0)
    layer.current(0)

def state():
    if select.get() == 0:
        field.config(state=NORMAL)
        layer.config(state=DISABLED)
    else:
        field.config(state=DISABLED)
        layer.config(state=NORMAL)

f3 = Frame(root, bg="#38070f")
f3.pack(fill=X)
f3.grid_columnconfigure(0, weight=1)

Label(
    f3, 
    text="----------------------------   ONGC QUARTERLY GAS PRODUCTION TRIPURA ASSET   ----------------------------", 
    bg="#38070f", fg="white", font=("Cooper BT", 30, "bold")
).pack(padx=20, pady=20)

f1 = Frame(root, bg="#E4C59E", bd=4, relief=RAISED) 
f1.place(x=30, y=428, height=353, width=436)

select = IntVar()
Radiobutton(f1, variable=select, value=0, text="Field Wise:", 
bg="#e3d1d4",fg="#45191d",
      font=("Verdana", 14, "bold"), 
      relief=RAISED,
      padx=9, pady=7,
      command=state,
).grid(row=0, column=0,padx=(34,10), pady=(20,10))

Radiobutton(f1, variable=select, value=1, text="Sand Wise:", 
 bg="#e3d1d4",fg="#45191d",
      font=("Verdana", 14, "bold"), 
     relief=RAISED,
      padx=5, pady=6,
      command=state
).grid(row=0, column=1, padx=(25,30), pady=(25,10), sticky=W)

field = ttk.Combobox(f1, values=fields, font=("Verdana", 13, "bold"), state=NORMAL, width=10)
field.grid(row=1, column=0, pady=5, padx=(25,5))
field.current(0)

layer = ttk.Combobox(f1, values=layers, font=("Verdana", 13, "bold"), state=DISABLED, width=15)
layer.grid(row=1, column=1, pady=5, padx=(0,20))
layer.current(0)

Label(f1, text="Year:", 
 bg="#e3d1d4", fg="#45191d",
 font=("Verdana", 14, "bold"), 
 relief=RAISED,
).grid(row=2, column=0, padx=(28, 2), pady=17, ipadx=19, ipady=10)

year = ttk.Combobox(f1, values=data_years, font=("Verdana", 13, "bold"), width=15)
year.grid(row=2, column=1, pady=17, sticky=W)
year.current(0)

Label(f1, text="Quarter:", 
 bg="#e3d1d4", fg="#45191d",
 font=("Verdana", 14, "bold"), 
 relief=RAISED,
).grid(row=3, column=0, pady=7, padx=(30, 2), ipadx=10, ipady=10)

quarter_values = ["All", "Q1 (Jan-Mar)", "Q2 (Apr-Jun)", "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"]

quarter = ttk.Combobox(f1, values=quarter_values, font=("Verdana", 13, "bold"), width=15)
quarter.grid(row=3, column=1, pady=7, sticky=W)
quarter.current(0)

Button(f1, text="SUBMIT", command=plot, font=("Verdana", 14, "bold"), bg="#820314",fg="#ffffff", activebackground="#7661ff",
    activeforeground="#ffffff", relief=RAISED, bd=3, overrelief=SUNKEN).grid(row=4, column=1,pady=7, ipadx=0,ipady=6,sticky=W)
Button(f1, text="CLEAR", command=clear, font=("Verdana", 14, "bold"), bg="#820314",fg="#ffffff", activebackground="#7661ff",
    activeforeground="#ffffff", relief=RAISED, bd=3, overrelief=SUNKEN).grid(row=4, column=1,pady=7,ipady=6, sticky=E, padx=19)

img = Image.open(r"Project2\ongc.png")
img = img.resize((421, 270))
img = ImageOps.expand(img, border=5, fill='#45191d')
p = ImageTk.PhotoImage(img)

Label(root, image=p).place(x=30, y=116)

f2 = Frame(root, relief=RIDGE, bd=5)
f2.pack(side=RIGHT, anchor=NE, padx=38, pady=24)

root.bind('<Return>', lambda event: plot())
root.mainloop()
