from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import pandas as pd
import os
import shutil
import datetime
import zipfile

root = Tk()
root.title("unLabel")

# label
folder_path = StringVar()
csv_path = Label(root,textvariable=folder_path).place(x=140,y=25)

table = StringVar()
file_df = Label(root,textvariable=table,font=("Arial", 12)).place(x=20,y=220)

no_file = StringVar()
num_str = Label(root,text="number of unlabel pictures : ",font=("Arial", 12)).place(x=20,y=180)
num_file = Label(root,textvariable=no_file,font=("Arial", 12)).place(x=250,y=180)

source_path = StringVar()
source_dir = Label(root,textvariable=source_path).place(x=140,y=65)

dest_path = StringVar()
dest_dir = Label(root,textvariable=dest_path).place(x=140,y=105)

output = Label(root,text="Output Name : ").place(x=140,y=140)
zip = StringVar()
inputtxt = Entry(root,textvariable=zip).place(x=240,y=140)

# button
def browse_button():
    # daclare global variable
    global folder_path, table, no_file

    # import csv file
    filename = filedialog.askopenfilename()
    format = os.path.splitext(filename)[1]
    if format != ".csv":
        messagebox.showerror(title="Format Type",message="Please import csv file")
    else:
        folder_path.set(filename)
    # print(type(filename))

        # show unLabel pictures
        pd.set_option('display.max_colwidth', None)
        df = pd.read_csv(filename)
        df = df[df['region_count'] == 0]
        # print(len(df))

        # show number of unLabel pictures
        no_file.set(len(df))
        df = df['filename']
        df = df.to_string(index=False)
        table.set(df)

def source_dir_button():
    global source_path
    filename = filedialog.askdirectory()
    source_path.set(filename)

def dest_dir_button():
    global dest_path
    filename = filedialog.askdirectory()
    dest_path.set(filename)

import_button = Button(root,text="Import csv",command=browse_button).place(x=20,y=20)
source_button = Button(root,text="Source Path",command=source_dir_button).place(x=20,y=60)
dest_button = Button(root,text="Destination Path",command=dest_dir_button).place(x=20,y=100)

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), arcname=file)

def exec():
    # print(table.get().split("\n"))
    # print(source_path.get())
    # print(dest_path.get())
    file_list = table.get().split("\n")
    csv = folder_path.get()
    source = source_path.get()
    dest = dest_path.get()
    current_datetime = datetime.datetime.now()
    dest = dest + "/" + current_datetime.strftime("%Y-%m-%dT%H-%M-%S")
    os.makedirs(dest)
    zip_name = zip.get()

    if csv == "" or source == "" or dest == "":
        messagebox.showerror(title="Select path",message="Please select all path")
    elif len(file_list) == 0:
        messagebox.showinfo(title="Already Labal",message="All pictures have been label already!")
    else:
        for i in range (0,len(file_list)):
            # print(source + "/" + file_list[i])
            isExist = os.path.exists(source + "/" + file_list[i])
            if isExist == True:
                shutil.copy2(source + "/" + file_list[i],dest)
            else:
                messagebox.showerror(title="File Not Found",message=source + "/" + file_list[i] + " Not exists ")
                break

        zipf = zipfile.ZipFile(zip_name+".zip", 'w', zipfile.ZIP_DEFLATED)
        zipdir(dest, zipf)
        zipf.close()
        shutil.move(zip_name+".zip", dest, copy_function=shutil.copy2)
copy_n_zip = Button(root,text="Copy and zip file",command=exec).place(x=20,y=140)

# screen size & position 
root.geometry("800x600+300+50")
root.mainloop()