import tkinter as tk
from tkinter import scrolledtext
import tkinter.ttk as ttk
from tkinter import filedialog
import collections
import MeCab
import csv

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        root.title("MorphologicalAnalysis")
        root.geometry("1200x800+100+100")
        self.fname = ''
        status = 'default'
        self.corpus = []

        self.columnconfigure(1,weight=1)
        self.rowconfigure(3,weight=1) 
        self.pack(fill='both',expand=True)
        self.sub_menuber()
        self.main_textbox()
        self.menubar_func()

    def sub_menuber(self):
        frame_menuber = ttk.Frame(self, height=35,)
        frame_menuber.grid(column=0,row=0,columnspan=2,padx=5,pady=5,sticky='NEW')
        button_open = ttk.Button(frame_menuber, text="Open file",command=self.fileOpen)
        button_delete = ttk.Button(frame_menuber, text="Tree delete",command=self.textDelete)
        button_open.pack(side='left')
        button_delete.pack(side='left')



    def main_textbox(self):
        self.treeview = ttk.Treeview(self)
        self.treeview['columns'] = ('id','名前','開始時間','終了時間','経過時間','テキスト')
        #column
        self.treeview.column('#0',width=0, stretch='no')
        self.treeview.column('id', anchor='w',width=50,stretch=False)
        self.treeview.column('名前',anchor='w',width=100,stretch=False)
        self.treeview.column('開始時間', anchor='w',width=100,stretch=False)
        self.treeview.column('終了時間',anchor='w',width=100,stretch=False)
        self.treeview.column('経過時間', anchor='w',width=100,stretch=False)
        self.treeview.column('テキスト',anchor='w')
        #heading
        self.treeview.heading('#0',text='Label',anchor='w')
        self.treeview.heading('id',text='ID',anchor='w')
        self.treeview.heading('名前',text='名前',anchor='w')
        self.treeview.heading('開始時間',text='開始時間',anchor='w')  
        self.treeview.heading('終了時間',text='終了時間',anchor='w')  
        self.treeview.heading('経過時間',text='経過時間',anchor='w')
        self.treeview.heading('テキスト',text='テキスト',anchor='w')    
        self.treeview.grid(column=1,row=1,rowspan=3,padx=5,sticky='NSEW')

    def textSort(self): 
        print("開設中")

    def menubar_func(self):
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar,tearoff=0)
        settingsmenu = tk.Menu(menubar,tearoff=0)
        filemenu.add_command(label='Open',command=self.fileOpen)
        root.config(menu=menubar)

    def textDelete(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)

    def fileOpen(self):
        self.fname = filedialog.askopenfilename()
        self.corpus = []
        i = 0
        if self.fname == '': return
        f = open(self.fname,'r')
        lines = f.readlines()
        f.close()
        for line in lines:
            l = line.split("\t")
            i += 1
            l.pop(1)
            l.insert(0, i)
            self.corpus.append(l)
        self.corpus = sorted(self.corpus, key=lambda x:float(x[2]))
        # self.textOrganize()
        i = 0
        for x in self.corpus:
            i += 1
            self.treeview.insert(parent='', index='end', iid=i ,values=(x))
        root.title('editor - '+self.fname)
        print(self.corpus[0])

 
root = tk.Tk()
app = Application(master=root)   
app.mainloop()