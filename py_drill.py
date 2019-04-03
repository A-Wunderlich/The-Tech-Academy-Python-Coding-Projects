import sqlite3
import tkinter
from tkinter import *
from tkinter import filedialog
import os
import shutil

conn = sqlite3.connect('pydrill.db')

with conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS txt_files( \
        ID INTEGER PRIMARY KEY AUTOINCREMENT, \
        fname TEXT \
        mdate TEXT \
        )")
    conn.commit()
conn.close()

def txtdate(sDir):
        for file in os.listdir(sDir):  # searches files in dir
            if file.endswith('.txt'):  # makes sure they are .txt files
                txtList = os.path.join(sDir, file)  # concatenates for absolute path
                txtTime = os.path.getctime(sDir)  # gets mdate for txt files
                print("\n{} | {}".format(txtList, txtTime))
                move(file)

def move(file,dDir):
    shutil.move(file,dDir)

            


class ParentWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self)

        self.master = master
        self.master.resizable(width=False, height=False)
        self.master.geometry('{}x{}'.format(650, 150))
        self.master.title("Check Files")

        self.btnBrowse1 = Button(self.master, text="Source Dir", width=12, height=1, command=self.getSourceDir)
        self.btnBrowse1.grid(row=0, column=0, padx=(10, 0), pady=(30, 0), sticky=W)
        self.btnBrowse2 = Button(self.master, text="Destination Dir", width=12, height=1, command=self.getDesDir)
        self.btnBrowse2.grid(row=1, column=0, padx=(10, 0), pady=(10, 0), sticky=W)
        self.btnCheck = Button(self.master, text="Move .txt Files", width=12, height=2, command=self.move)
        self.btnCheck.grid(row=2, column=0, padx=(10, 0), pady=(10, 0), sticky=W)
        self.btnClose = Button(self.master, text="Close Program", width=12, height=2)
        self.btnClose.grid(row=2, column=2, sticky=E)
        self.txtBox1 = Entry(self.master, text="", font=12, width=40)
        self.txtBox1.grid(row=0, column=1, columnspan=2, padx=(25, 0), pady=(30, 0))
        self.txtBox2 = Entry(self.master, text="", font=12, width=40)
        self.txtBox2.grid(row=1, column=1, columnspan=2, padx=(25, 0), pady=(10, 0))


    

    def getSourceDir(self):
        sDir = filedialog.askdirectory()
        self.txtBox1.insert(END, sDir)
        txtdate(sDir)

    def getDesDir(self):
        dDir = filedialog.askdirectory()
        self.txtBox2.insert(END, dDir)
        move(dDir)

    def move(file,dDir):
        shutil.move(file,dDir)

    
    





if __name__ == '__main__':
    root = Tk()
    App = ParentWindow(root)
    root.mainloop()

