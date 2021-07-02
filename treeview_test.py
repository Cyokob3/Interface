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
        self.data = []
        # ウィンドウ表示方法の設定
        self.columnconfigure(1,weight=1)
        self.rowconfigure(3,weight=1) 
        self.pack(fill='both',expand=True)
        self.sub_menuber()
        self.main_textbox()
        # style
        self.s = ttk.Style(self)
        self.s.configure('Treeview',background='aliceblue')

    def sub_menuber(self):
        frame_menuber = ttk.Frame(self, height=40)
        frame_menuber.grid(column=0,row=0,columnspan=2,padx=5,pady=5,sticky='NEW')
        button_open = ttk.Button(frame_menuber, text="Open file",command=self.fileOpen)
        button_delete = ttk.Button(frame_menuber, text="Tree delete",command=self.textDelete)
        button_MeCab = ttk.Button(frame_menuber, text="MeCab",command=self.getText)
        button_open.pack(side='left')
        button_delete.pack(side='left')
        button_MeCab.pack(side='left')

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

    def subTreeview(self):
        subWindow = tk.Toplevel()
        self.sub_treeview = ttk.Treeview(subWindow)
        self.sub_treeview['columns'] = ('id','テキスト','品詞')
        #column
        self.sub_treeview.column('#0',width=0, stretch='no')
        self.sub_treeview.column('id', anchor='w',width=50,stretch=False)
        self.sub_treeview.column('テキスト', anchor='w',width=200,stretch=False)
        self.sub_treeview.column('品詞',anchor='w')
        #heading
        self.sub_treeview.heading('#0',text='Label',anchor='w')
        self.sub_treeview.heading('id',text='ID',anchor='w')
        self.sub_treeview.heading('テキスト',text='テキスト',anchor='w')
        self.sub_treeview.heading('品詞',text='品詞',anchor='w')
        #grid    
        self.sub_treeview.pack(fill='both',expand=True)

    def textDelete(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)

    def getText(self):
        # ウィンドウを作成
        self.subTreeview()

        #変数初期化
        line_id = 0
        index_id = 0
        self.corpus = []
        m = MeCab.Tagger("-Osimple")

        # 形態素解析を行う箇所
        for x in self.data:
            convert = m.parse(x[5]).splitlines()
            line_id += 1
            for y in convert:
                convert_split = y.split('\t')
                convert_split.insert(0, line_id)
                self.corpus.append(convert_split)
        #結果を表示する
        for z in self.corpus:
            index_id += 1
            if z[1] == 'EOS': continue
            self.sub_treeview.insert(parent='', index='end', iid=index_id ,values=(z))

    def fileOpen(self):
        self.fname = filedialog.askopenfilename()
        self.data = []
        i = 0
        sort_target = 2 #２は開始時間になる
        if self.fname == '': return
        f = open(self.fname,'r')
        lines = f.readlines()
        f.close()
        for line in lines:
            l = line.split("\t")
            i += 1
            l.pop(1)
            l.insert(0, i)
            self.data.append(l)
        self.data = sorted(self.data, key=lambda x:float(x[sort_target]))
        i = 0
        for x in self.data:
            i += 1
            self.treeview.insert(parent='', index='end', iid=i ,values=(x))
        root.title('editor - '+self.fname)
        print(self.data[0])

 
root = tk.Tk()
app = Application(master=root)   
app.mainloop()