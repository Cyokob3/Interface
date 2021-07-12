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

        # テキスト
        self.helptext = []
        self.helptext += ['これは簡単な形態素解析を行うシステムです']
        self.helptext += ['テキストデータはアノテーションツールであるELANで作成してください']
        self.helptext += ['Openfileボタンを押してテキストファイルを選択してください']
        self.helptext += ['Tree deleteボタンで表示されているテキストを消すことができます']
        self.helptext += ['MeCabボタンで形態素解析の結果を表示します']
        self.helptext += ['helpボタンを押すことでいつでもこのテキストを見ることができます']    

        root.title("MorphologicalAnalysis")
        root.geometry("1200x800+100+100")
        self.fname = ''
        self.stats = 'default'
        self.corpus = []
        self.data = []
        self.extrction_data = []
        self.menber = []
        self.wclass = ['名詞','動詞','形容詞','助詞','助動詞','フィラー'] 
        self.target_wclass = 'oll'
        self.target_menber = 'oll'
        # ウィンドウ表示方法の設定
        self.columnconfigure(0,weight=1)
        self.rowconfigure(1,weight=1) 
        self.pack(fill='both',expand=True)
        self.sub_menuber()
        self.main_helptext()
        self.main_treeview()
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
        self.button_MeCab = ttk.Button(frame_menuber, text="MeCab",command=self.getText,state='disabled')
        self.button_CSV = ttk.Button(frame_menuber, text="CSV",command=self.csv_file_save,state='disabled')
        self.button_extraction = ttk.Button(frame_menuber, text="Extraction",command=self.extraction,state='disabled')
        button_help = ttk.Button(frame_menuber, text="help",command=self.sub_help_text)
        button_open.pack(side='left')
        button_delete.pack(side='left')
        self.button_MeCab.pack(side='left')
        self.button_CSV.pack(side='left')
        self.button_extraction.pack(side='left')
        button_help.pack(side='right')

    def main_treeview(self):
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
        #フレームを用意
        self.frame_help = tk.Frame(self, bg='white')
        self.frame_help.grid(column=0,row=1,padx=5,sticky='NSEW')
        # ラベルでテキストを表示
        for text_id in range(len(self.helptext)):
            label_help = tk.Label(self.frame_help, text=self.helptext[text_id],bg='white',font=("MSゴシック", "20", "bold"))
            label_help.pack(side='top',pady=10)

    def subTreeview(self):
        self.subWindow = tk.Toplevel()
        self.subWindow.title('MeCab')
        self.sub_treeview = ttk.Treeview(self.subWindow)
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

    def subTreeview_count(self):
        # サブウィンドウの作成
        self.sub_count_window = tk.Toplevel()
        self.sub_count_window.title("Count words")
        self.sub_count_window.geometry("300x300+100+100")
        self.sub_count_window.columnconfigure(0,weight=1)
        self.sub_count_window.rowconfigure(1,weight=1) 
        # メニューバー用のフレーム作成
        self.frame_count_menuber = ttk.Frame(self.sub_count_window)
        self.frame_count_menuber.grid(column=0,row=0,padx=5,sticky='NEW')
        # メニューバーのボタンを作成
        self.button_count_CSV = ttk.Button(self.frame_count_menuber, text="CSV",command=self.csv_file_save)
        self.button_count_CSV.pack(side='left')
        # ツリービュー用のフレーム作成
        self.frame_count_view = ttk.Frame(self.sub_count_window)
        self.frame_count_view.grid(column=0,row=1,padx=5,sticky='NSEW')
        # ツリービューの作成
        self.sub_treeview_count = ttk.Treeview(self.frame_count_view)
        self.sub_treeview_count['columns'] = ('単語','出現数')
        #column
        self.sub_treeview_count.column('#0',width=0, stretch='no')
        self.sub_treeview_count.column('単語', anchor='w',width=100,stretch=False)
        self.sub_treeview_count.column('出現数',width=100, anchor='w')
        #heading
        self.sub_treeview_count.heading('#0',text='Label',anchor='w')
        self.sub_treeview_count.heading('単語',text='単語',anchor='w')
        self.sub_treeview_count.heading('出現数',text='出現数',anchor='w')
        #pack   
        self.sub_treeview_count.pack(fill='both',expand=True)

    def sub_help_text(self):
        # サブウィンドウ表示
        sub_help_window = tk.Toplevel()
        sub_help_window.title('helps')
        # フレームを用意
        self.sub_help_frame = tk.Frame(sub_help_window, bg='white')
        self.sub_help_frame.pack(fill='both',expand=True)
        # ラベルでテキストを表示
        for text_id in range(len(self.helptext)):
            sub_label_help = tk.Label(self.sub_help_frame, text=self.helptext[text_id],bg='white',font=("MSゴシック", "20", "bold"))
            sub_label_help.pack(side='top',pady=10)

    def textDelete(self):
        # 変数初期化
        self.data = []
        self.corpus = []
        self.menber = []
        if self.stats != 'default': self.frame_help.tkraise()
        self.stats = 'default'
        root.title("MorphologicalAnalysis")
        self.target_menber == 'oll'
        # サブウィンドウを削除
        if self.stats != 'default':
            self.subWindow.destroy()
            self.sub_count_window.destroy()
        # ツリービューのアイテムを削除
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        # MeCabボタンとCSVボタンの状態をdisabledに変更
        self.button_MeCab['state']='disabled'
        self.button_CSV['state']='disabled'
        self.button_extraction['state']='disabled'
    
    def sorted_text(self):
        sorted(self.data, key=lambda x:float(x[self.sort_target]))

    def extraction(self):
        # 初期化
        menber = []
        self.extraction_front = 'menber'
        # ウィンドウ作成
        self.extraction_hopup_main = tk.Toplevel()
        self.extraction_hopup_main.title("抽出する要素を選んでください")
        self.extraction_hopup_main.geometry("300x200+500+200")
        self.extraction_hopup_main.columnconfigure(0,weight=1)
        self.extraction_hopup_main.rowconfigure(1,weight=1) 
        self.frame_extraction_menber = ttk.Frame(self.extraction_hopup_main)
        self.frame_extraction_word = ttk.Frame(self.extraction_hopup_main)
        self.frame_extraction_word.grid(column=0,row=0,padx=5,sticky='NSEW')
        self.frame_extraction_menber.grid(column=0,row=0,padx=5,sticky='NSEW')
        self.frame_extraction_menber.tkraise()
        # 人物選択リストボックス
        self.listbox_extraction_menber = tk.Listbox(self.frame_extraction_menber)
        self.listbox_extraction_menber.pack(side='top')
        for i in range(len(self.menber)):
            self.listbox_extraction_menber.insert(i, self.menber[i])
        self.listbox_extraction_menber.insert('end','oll')
        # 品詞選択リストボックス
        self.listbox_extraction_word = tk.Listbox(self.frame_extraction_word)
        self.listbox_extraction_word.pack(side='top')
        for i in range(len(self.wclass)):
            self.listbox_extraction_word.insert(i, self.wclass[i])
        self.listbox_extraction_word.insert('end','oll')
        # 選択ボタン
        self.button_choice = ttk.Button(self.extraction_hopup_main,text='選択',command=self.selected)
        self.button_choice.grid(column=0,row=1,padx=5,sticky='NSEW')      

    # 選択されたリストボックスを取得   
    def selected(self):
        if self.extraction_front == 'menber':
            itemID = self.listbox_extraction_menber.curselection()
            self.target_menber = self.listbox_extraction_menber.get(itemID)
            self.frame_extraction_word.tkraise()
            print(self.target_menber)
        elif self.extraction_front == 'word':
            itemID = self.listbox_extraction_word.curselection()
            self.target_wclass = self.listbox_extraction_word.get(itemID)
            self.extraction_hopup_main.destroy()
            print(self.target_wclass)
        self.extraction_front = 'word'

    def getText(self):
        # 状態
        self.stats = 'get'
        # ウィンドウを作成
        self.subTreeview()
        #変数初期化
        index_id = 0
        self.corpus = []
        # user.dicは同じディレクトリにあるユーザ辞書
        # 辞書に登録したい場合はこの辞書に入れる必要がある
        m = MeCab.Tagger("-Osimple -u user.dic") 
        # 形態素解析を行う箇所
        for x in self.data:
            if self.target_menber in 'oll':
                convert = m.parse(x[5]).splitlines()
            elif self.target_menber in x[1]:
                convert = m.parse(x[5]).splitlines()
            else : continue
            line_id = x[0]
            for y in convert:
                convert_split = y.split('\t')
                convert_split.insert(0, line_id)
                #print(convert_split)
                self.corpus.append(convert_split)
        #結果を表示する
        for z in self.corpus:
            index_id += 1
            if z[1] == 'EOS': continue
            self.sub_treeview.insert(parent='', index='end', iid=index_id ,values=(z))
        self.textCount()

    
    def textCount(self):
        # 状態
        self.stats = 'Count'
        # 初期化
        count_collection = []
        self.count = []
        i = 0
        # ウィンドウ作成
        self.subTreeview_count()
        #コーパスのリストから単語を取り出す
        for corpus_element in self.corpus:
            if 'EOS' in corpus_element[1]: continue
            if '-' in corpus_element[2]:
                w = corpus_element[2].split("-")
            else : w = [corpus_element[2]]
            if self.target_wclass in 'oll': 
                count_collection.append(corpus_element[1])
            elif self.target_wclass in w:
                count_collection.append(corpus_element[1])
        # 単語のカウントを行う
        count_collection = collections.Counter(count_collection)
        # 結果を表示する
        for turn in range(len(set(count_collection))):
            self.count.append(count_collection.most_common()[turn])
        for insert_data in self.count:
            i += 1
            self.sub_treeview_count.insert(parent='', index='end', iid=i ,values=(insert_data))


    def fileOpen(self):
        # 初期化
        self.textDelete()
        # ファイルダイアログで開くファイルを探す
        self.fname = filedialog.askopenfilename()
        self.data = []
        i = 0
        self.sort_target = 2 #２は開始時間になる
        if self.fname == '': return
        # MeCabボタンとCSVボタン,extractionボタンの状態をnormalに変更
        self.button_MeCab['state']='normal'
        self.button_CSV['state']='normal'
        self.button_extraction['state']='normal'
        # ツリービューのフレームを全面にする
        self.frame_main.tkraise()
        # 状態の確認
        self.stats = 'Open'
        f = open(self.fname,'r')
        lines = f.readlines()
        f.close()
        for line in lines:
            l = line.split("\t")
            i += 1
            l.pop(1)
            l.insert(0, i)
            self.menber.append(l[1])
            self.data.append(l)
        self.menber = sorted(set(self.menber))
        self.data = sorted(self.data, key=lambda x:float(x[self.sort_target]))
        self.extraction()
        i = 0
        for x in self.data:
            i += 1
            self.treeview.insert(parent='', index='end', iid=i ,values=(x))
        root.title('editor - '+self.fname)

    def csv_file_save(self):
        # print(self.data)
        self.seve_fname = filedialog.asksaveasfilename(
            title='CSVファイルの保存',
            initialdir='./',
            initialfile='Unfiled',
            defaultextension='csv'
            )
        if self.seve_fname == '': return
        with open(self.seve_fname,encoding="cp932",mode='w') as f:
            writer = csv.writer(f)
            if self.stats == 'Count':
                writer.writerows(self.count)
            elif self.stats == 'Open':
                writer.writerows(self.data)


root = tk.Tk()
app = Application(master=root)   
app.mainloop()