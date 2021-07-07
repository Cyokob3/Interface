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
        self.stats = 'default'
        self.corpus = []
        self.data = []
        # ウィンドウ表示方法の設定
        self.columnconfigure(0,weight=1)
        self.rowconfigure(1,weight=1) 
        self.pack(fill='both',expand=True)
        self.sub_menuber()
        self.main_helptext()
        self.main_textbox()
        # style
        self.s = ttk.Style(self)
        self.s.configure('Treeview',background='aliceblue')
        self.s.configure('TFrame',background='aliceblue')
        self.frame_help.tkraise()

    def sub_menuber(self):
        frame_menuber = ttk.Frame(self, height=40)
        frame_menuber.grid(column=0,row=0,padx=5,pady=5,sticky='NEW')
        button_open = ttk.Button(frame_menuber, text="Open file",command=self.fileOpen)
        button_delete = ttk.Button(frame_menuber, text="Tree delete",command=self.textDelete)
        button_MeCab = ttk.Button(frame_menuber, text="MeCab",command=self.getText)
        button_open.pack(side='left')
        button_delete.pack(side='left')
        button_MeCab.pack(side='left')

    def main_textbox(self):
        self.frame_main = ttk.Frame(self)
        self.frame_main.grid(column=0,row=1,padx=5,sticky='NSEW')
        self.treeview = ttk.Treeview(self.frame_main)
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
        self.treeview.heading('id',text='ID',anchor='w',command=self.sorted_text)
        self.treeview.heading('名前',text='名前',anchor='w',command=self.sorted_text)
        self.treeview.heading('開始時間',text='開始時間',anchor='w',command=self.sorted_text)  
        self.treeview.heading('終了時間',text='終了時間',anchor='w',command=self.sorted_text)  
        self.treeview.heading('経過時間',text='経過時間',anchor='w',command=self.sorted_text)
        self.treeview.heading('テキスト',text='テキスト',anchor='w',command=self.sorted_text)    
        self.treeview.pack(fill='both',expand=True)

    def main_helptext(self):
        helptext_1 = 'Openfileボタンを押してテキストファイルを選択してください'
        helptext_2 = 'Tree deleteボタンで表示されているテキストを消すことができます'
        helptext_3 = 'MeCabボタンで形態素解析の結果を表示します'
        self.frame_help = tk.Frame(self, bg='white')
        self.frame_help.grid(column=0,row=1,padx=5,sticky='NSEW')
        label1_frame = tk.Label(self.frame_help, text=helptext_1,bg='white',font=("MSゴシック", "20", "bold"))
        label2_frame = tk.Label(self.frame_help, text=helptext_2,bg='white',font=("MSゴシック", "20", "bold"))
        label3_frame = tk.Label(self.frame_help, text=helptext_3,bg='white',font=("MSゴシック", "20", "bold"))
        label1_frame.pack(side='top',pady=10)
        label2_frame.pack(side='top')
        label3_frame.pack(side='top',pady=10)


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
        # 変数初期化
        self.data = []
        self.corpus = []
        if self.stats != 'default': self.frame_help.tkraise()
        self.stats = 'default'
        root.title("MorphologicalAnalysis")
        # ツリービューのアイテムを削除
        for i in self.treeview.get_children():
            self.treeview.delete(i)
    
    def sorted_text(self):
        sorted(self.data, key=lambda x:float(x[sort_target]))


    def getText(self):
        # 状態
        self.stats = 'get'
        # ウィンドウを作成
        self.subTreeview()

        #変数初期化
        index_id = 0
        self.corpus = []
        m = MeCab.Tagger("-Osimple")
        # 形態素解析を行う箇所
        for x in self.data:
            convert = m.parse(x[5]).splitlines()
            line_id = x[0]
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
        # ツリービューのフレームを全面にする
        self.frame_main.tkraise()
        # 状態の確認
        self.stats = 'open'
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