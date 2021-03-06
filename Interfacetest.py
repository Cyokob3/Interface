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
        self.test()
        self.main_textbox()
        self.file_open_button()
        self.file_seve_button()
        self.main_treeview()
        self.menubar_func()

    def test(self):
        frame_test = ttk.Frame(self, height=35,)
        frame_test.grid(column=0,row=0,columnspan=2,padx=5,pady=5,sticky='NEW')
        button_test = ttk.Button(frame_test, text="サブメニューバー開設中")
        button_sort = ttk.Button(frame_test, text="Sort", command=self.textSort)
        button_test.pack()

    def file_open_button(self):
        button_open = ttk.Button(self, text="Open file",command=self.fileOpen)
        button_open.grid(column=0,row=1,padx=5,sticky='N')

    def file_seve_button(self):
        button_seve = ttk.Button(self, text="Seve as",command=self.fileSave)
        button_seve.grid(column=0,row=2,pady=5,sticky='N')

    def main_textbox(self):
        text = tk.scrolledtext.ScrolledText(self,wrap='none',undo=True,bg='#e0ffff')
        text.configure(font=(18))
        text.grid(column=1,row=1,rowspan=3,padx=5,sticky='NSEW')
        self.text = text 
        self.text.insert('end',"形態素解析を行うファイルを選択")

    def textSort(self): 
        print("開設中")


    def main_treeview(self):
        treeview = ttk.Treeview(self)
        treeview['columns'] = ('file','開設中')
        treeview.column('#0',width=0, stretch='no')
        treeview.column('file', anchor='w', width=75)
        treeview.column('開設中',anchor='center', width=75)
        treeview.heading('#0',text='Label',anchor='w')
        treeview.heading('file', text='file',anchor='w')
        treeview.heading('開設中', text='開設中', anchor='center')
        treeview.grid(column=0,row=3,padx=5,pady=5,sticky='NS')

    def createNewWindow(self):
        newWindow = tk.Toplevel()
        labelExample = tk.Label(newWindow, text = "特定の品詞でソートを行う")
        textField = tk.Entry(newWindow, text = "品詞を選択")
        sortedButton = tk.Button(newWindow, text = "ソートを行う")
        labelExample.pack()
        textField.pack()
        sortedButton.pack()

    def menubar_func(self):
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar,tearoff=0)
        settingsmenu = tk.Menu(menubar,tearoff=0)
        filemenu.add_command(label='Open',command=self.fileOpen)
        filemenu.add_command(label='Get',command=self.getText)
        filemenu.add_command(label='Count',command=self.textCount)
        filemenu.add_command(label='Save',command=self.fileSave)
        filemenu.add_command(label='CSV',command=self.fileSaveCSV)
        filemenu.add_command(label='New',command=self.createNewWindow)
        filemenu.add_command(label='Delete',command=self.textDelete)
        filemenu.add_command(label='Exit',command=exit)
        menubar.add_cascade(label='File',menu=filemenu)
        menubar.add_cascade(label='Settings',menu=settingsmenu)
        root.config(menu=menubar)

                         

    def newCreate(self):
        print("開設中")

    def getText(self):
        status = 'Get'
        if self.fname == "":
            self.fname = filedialog.askopenfilename()
            if self.fname == '': return
        f = open(self.fname,'r')
        lines = f.readlines()
        f.close()
        m = MeCab.Tagger("-Ochasen")
        self.textDelete()
        for line in lines:
            l = [l.strip() for l in line.split("\t")]
            mline = m.parse(l[5])
            self.text.insert('end',mline)
    
    def textCount(self):
        status = 'Count'
        l1 = []
        s = (self.text.index("end"))
        wclass = ''
        for l in range(1,int(float(s))):
            s_l = str(float(l))
            e_l = str(l) + ".end"
            line = self.text.get(s_l,e_l)
            if 'EOS' in line:
                continue
            line = [line.strip() for line in line.split("\t")]
            if wclass in '':
                l1.append(line[0])
            elif wclass in line[3]:
                l1.append(line[0])
        l1 = collections.Counter(l1)
        self.textDelete()
        for i in range(len(set(l1))):
            self.text.insert('end',l1.most_common()[i])
            self.text.insert('end', "\n")
            
    def textDelete(self):
        self.text.configure(state='normal')
        self.text.delete('1.0','end')

    def fileOpen(self):
        self.fname = filedialog.askopenfilename()
        self.corpus = []
        if self.fname == '': return
        f = open(self.fname,'r')
        lines = f.readlines()
        f.close()
        self.text.delete('1.0','end')
        for line in lines:
            l = line.split("\t")
            l.pop(1)
            self.corpus.append(l)
        self.corpus = sorted(self.corpus, key=lambda x:float(x[1]))
        # self.textOrganize()
        for x in self.corpus:
            x = ('{:　<6}  {:　<9}  {:　<9}  {:　<9}  {}'.format(*x))
            self.text.insert('end', x)
        root.title('editor - '+self.fname)
        print(self.corpus[0])

    def fileSave(self):
        f_type = [('Text', '*.txt')]
        file_path = filedialog.asksaveasfilename(
            filetypes=f_type)
        if file_path != "":
            with open(file_path, "w") as f:
                f.write(self.text.get("1.0", "end-1c"))
        return

    def fileSaveCSV(self):
        f_type = [('CSV', '*.csv')]
        file_path = filedialog.asksaveasfilename(
            filetypes=f_type)
        if file_path != "":
           with open(file_path, "w", encoding="cp932") as f:
                for x in self.corpus:
                    w = csv.writer(f)
                    w.writerow(x)
        return
 
root = tk.Tk()
app = Application(master=root)   
app.mainloop()