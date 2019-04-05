import sqlite3
import tkinter
from tkinter import *
from tkinter import filedialog
import os
import shutil

conn = sqlite3.connect('pydrill.db') #creates a table to store the file names and mtimes

with conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS txt_files( \
        ID INTEGER PRIMARY KEY AUTOINCREMENT, \
        fname TEXT, \
        mdate TEXT \
        )")
    conn.commit()
conn.close()


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
        self.btnCheck.grid(row=2, column=0, padx=(10, 0), pady=(10, 0), sticky=E)
        self.btnClose = Button(self.master, text="Close Program", width=12, height=2, command=self.close)
        self.btnClose.grid(row=2, column=2, sticky=E)
        self.txtBox1 = Entry(self.master, text="", font=12, width=40)
        self.txtBox1.grid(row=0, column=1, columnspan=2, padx=(25, 0), pady=(30, 0))
        self.txtBox2 = Entry(self.master, text="", font=12, width=40)
        self.txtBox2.grid(row=1, column=1, columnspan=2, padx=(25, 0), pady=(10, 0))


    

    def getSourceDir(self):
        #this gets the first file path for the source directory and inserts it in the first text box when the first button is pressed
        self.txtBox1.delete(0,END)
        sDir = filedialog.askdirectory()
        self.txtBox1.insert(END, sDir)
        print(sDir)

    def getDesDir(self):
        #this gets the second file path for the destination directory and inserts it in the second text box when the second button is pressed
        self.txtBox2.delete(0,END)
        dDir = filedialog.askdirectory()
        self.txtBox2.insert(END, dDir)
        print(dDir)
        
    def move(self):
        sDir = self.txtBox1.get() #gets source directory
        srcFiles = os.listdir(sDir) #gets list of all files in source directory
        dst = self.txtBox2.get() #gets destination directory
        for files in srcFiles:
            if files.endswith(".txt"): #gets .txt files
                txtListPath = os.path.join(sDir, files) #joins path and file for absolute path so they can be used in shutil.move()
                txtListTime = os.path.getmtime(txtListPath) #gets mtime of .txt files in source dir that are going to be moved
                print("\n{} | {}".format(txtListPath,txtListTime)) #prints "absolute path| mtime"
                shutil.move(txtListPath,dst) #moves .txt files from source directory to destination directory
                conn = sqlite3.connect('pydrill.db') #adds the name of the .txt files and their respective mtime to the pydrill table
                with conn:
                    cur = conn.cursor()
                    cur.execute  ("INSERT INTO txt_files (fname, mdate) VALUES (?,?) ",(files, txtListTime,))
                    conn.commit()
                conn.close()
                
    def close(self):
        #closes script
        self.master.destroy()
        os._exit(0)
                    

    
    





if __name__ == '__main__':
    root = Tk()
    App = ParentWindow(root)
    root.mainloop()
