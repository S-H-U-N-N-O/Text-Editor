from tkinter import *
from tkinter.ttk import *
from tkinter import font
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox
import os
import tempfile


#function
def changebg(bg_color, fg_color):
    textarea.config(bg=bg_color, fg=fg_color)

def toolbarFunc():
    if show_toolbar.get() == False:
        tool_bar.pack_forget()
    if show_toolbar.get() == True:
        textarea.pack_forget()
        tool_bar.pack(fill=X)
        textarea.pack(fill=BOTH, expand=1)

def statusbarFunc():
    if show_statusbar.get() == False:
        status_bar.pack_forget()
    else:
        status_bar.pack()




def Find():

    #functions
    def find_words():
        textarea.tag_remove('match', 1.0, END)
        start_pos = '1.0'
        word = entryField.get()
        if word:
            while True:
                start_pos = textarea.search(word, start_pos, stopindex=END)
                if not start_pos:
                    break
                end_pos = f'{start_pos}+{len(word)}c'
                textarea.tag_add('match', start_pos, end_pos)

                textarea.tag_config('match', foreground='red', background='yellow')
                start_pos=end_pos

    def replace_word():
        word =entryField.get()
        replace = replace_entryField.get()
        content = textarea.get(1.0, END)
        new_content = content.replace(word, replace)
        textarea.delete(1.0, END)
        textarea.insert(1.0, new_content)


        
    root1 = Toplevel()
    root1.title('Find')
    root1.geometry('450x250+500+200')
    root1.resizable(0, 0)

    labelFrame = LabelFrame(root1, text='Find/Replace')
    labelFrame.pack(pady=20)

    findlabel = Label(labelFrame, text='Find')
    findlabel.grid(row=0, column=0)
    entryField = Entry(labelFrame)
    entryField.grid(row=0, column=1, padx=5, pady=5)

    replacelabel = Label(labelFrame, text='Replace')
    replacelabel.grid(row=1, column=0)
    replace_entryField = Entry(labelFrame)
    replace_entryField.grid(row=1, column=1, padx=5, pady=5)

    findbutton = Button(labelFrame, text='Find', command=find_words)
    findbutton.grid(row=2, column=1, padx=5, pady=5)

    replacebutton = Button(labelFrame, text='Replace', command=replace_word)
    replacebutton.grid(row=2, column=0, padx=5, pady=5)

    def doSomething():
        textarea.tag_remove('match', 1.0, END)
        root1.destroy()

    root1.protocol('WM_DELETE_WINDOW', doSomething)
    root1.mainloop()


def statusbar_function(self):
    if textarea.edit_modified():
        words= len(textarea.get(0.0, END).split())
        characters = len(textarea.get(0.0, 'end-1c').replace(' ', ''))
        status_bar.config(text=f'Characters: {characters} Words : {words}')

    textarea.edit_modified(False)

url = ''
def new_file(self=None):
    global url
    url =''
    textarea.delete(0.0, END)

def open_file(self=None):
    global url
    url = filedialog.askopenfilename(initialdir=os.getcwd, title='Select File', filetypes=(('Text Files', 'txt'), ('All Files', '*.*')))
    if url != '':
        data = open(url, 'r')
        textarea.insert(0.0, data.read())
    root.title(os.path.basename(url))

def save_file(self=None):
    if url == '':
        save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text Files', 'txt'), ('All Files', '*.*')))
        if save_url is None:
            pass
        else:
            content = textarea.get(0.0, END)
            save_url.write(content)
            save_url.close()
    else:
        content = textarea.get(0.0, END)
        file = open(url, 'w')
        file.write(content)

def saveas_file(self=None):
    save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text Files', 'txt'), ('All Files', '*.*')))

    content = textarea(0.0, END)
    save_url.write(content)
    save_url.close()
    if url != '':
        os.remove(url)

def iexit(self=None):
    if textarea.edit_modified():
        result = messagebox.askyesnocancel('Warning', 'Do you want to save the file?')
        if result is True:
            if url != '':
                content = textarea.get(0.0, END)
                file = open(url, 'w')
                file.write(content)
                root.destroy()
            else:
                content = textarea.get(0.0, END)
                save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text Files', 'txt'), ('All Files', '*.*')))


                save_url.write(content)
                save_url.close()
                root.destroy()

        elif result is False:
            root.destroy()
        else:
            pass
    else:
        root.destroy()

def printout(self=None):
    file = tempfile.mktemp('.txt')
    open(file, 'w').write(textarea.get(1.0, END))
    os.startfile(file, 'print')
            



fontSize=12
fontStyle = 'arial'
def font_style(self):
    global fontStyle
    fontStyle = font_family_variable.get()
    textarea.config(font=(fontStyle, fontSize))

def font_size(self):
    global fontSize
    fontSize=sizevariable.get()
    textarea.config(font=(fontStyle, fontSize))

def bold_text():
    text_property = font.Font(font=textarea['font']).actual()
    if text_property['weight'] == 'normal':
        textarea.config(font=(fontStyle, fontSize, 'bold'))
    if text_property['weight'] == 'bold':
        textarea.config(font=(fontStyle, fontSize, 'normal'))


def italic_text():
    text_property = font.Font(font=textarea['font']).actual()
    if text_property['slant'] == 'roman':
        textarea.config(font=(fontStyle, fontSize, 'italic'))
    if text_property['slant'] == 'italic':
        textarea.config(font=(fontStyle, fontSize, 'roman'))


def underline_text():
    text_property = font.Font(font=textarea['font']).actual()
    if text_property['underline'] == 0:
        textarea.config(font=(fontStyle, fontSize, 'underline'))
    if text_property['underline'] == 1:
        textarea.config(font=(fontStyle, fontSize))


def color_select():
    color = colorchooser.askcolor()
    textarea.config(fg=color[1])

def align_right():
    data = textarea.get(0.0, END)
    textarea.tag_config('right', justify=RIGHT)
    textarea.delete(0.0, END)
    textarea.insert(INSERT, data, 'right')

def align_left():
    data = textarea.get(0.0, END)
    textarea.tag_config('left', justify=LEFT)
    textarea.delete(0.0, END)
    textarea.insert(INSERT, data, 'left')

def align_center():
    data = textarea.get(0.0, END)
    textarea.tag_config('center', justify=CENTER)
    textarea.delete(0.0, END)
    textarea.insert(INSERT, data, 'center')

def clear_all(self=None):
    textarea.delete(0.0, END)

#setup
root = Tk()
root.title('Text Editor')
root.geometry('1200x628+10+10')

menubar = Menu()
root.config(menu=menubar)

#filemenu
filemenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label='File', menu=filemenu)
newImage = PhotoImage(file='new.png')
openImage = PhotoImage(file='open.png')
saveImage = PhotoImage(file='save.png')
saveasImage = PhotoImage(file='save_as.png')
exitImage = PhotoImage(file='exit.png')
printImage = PhotoImage(file='print.png')

filemenu.add_command(label='New', accelerator='Ctrl+N', image=newImage, compound=LEFT, command=new_file)
filemenu.add_command(label='Open', accelerator='Ctrl+O', image=openImage, compound=LEFT, command=open_file)
filemenu.add_command(label='Save', accelerator='Ctrl+S', image=saveImage, compound=LEFT, command=save_file)
filemenu.add_command(label='Save As', accelerator='Ctrl+Alt+S', image=saveasImage, compound=LEFT, command=saveas_file)
filemenu.add_command(label='Print', accelerator='Ctrl+P', image=printImage, compound=LEFT, command=printout)
filemenu.add_separator()
filemenu.add_command(label='Exit', accelerator='Ctrl+Q', image=exitImage, compound=LEFT, command=iexit)


#editmenu
undoImage = PhotoImage(file='undo.png')
redoImage = PhotoImage(file='redo.png')
cutImage = PhotoImage(file='cut.png')
copyImage = PhotoImage(file='copy.png')
pasteImage = PhotoImage(file='paste.png')
selectImage = PhotoImage(file='select-all.png')
clearImage = PhotoImage(file='clear_all.png')
findImage = PhotoImage(file='find.png')




#toolbar selection

tool_bar = Label(root)
tool_bar.pack(side=TOP, fill=X)
font_family_variable = StringVar()
font_families = font.families()
fontfamily_combobox = Combobox(tool_bar, width=30, values=font_families, state='readonly', textvariable=font_family_variable)
fontfamily_combobox.current(font_families.index('Arial'))
fontfamily_combobox.grid(row=0, column=0, padx=5)

fontfamily_combobox.bind('<<ComboboxSelected>>', font_style)

#fontsize

sizevariable = IntVar()
font_size_combobox = Combobox(tool_bar, width=14, textvariable=sizevariable, state='readonly', value=tuple(range(8, 81)))
font_size_combobox.current(4)
font_size_combobox.grid(row=0, column=1, padx=5)
font_size_combobox.bind('<<ComboboxSelected>>',font_size)

#buttonselection
boldImage = PhotoImage(file='bold.png')
boldButton = Button(tool_bar, image=boldImage, command=bold_text)
boldButton.grid(row=0, column=2, padx=5)


italicImage = PhotoImage(file='italic.png')
italicButton = Button(tool_bar, image=italicImage, command=italic_text)
italicButton.grid(row=0, column=3, padx=5)

underlineImage = PhotoImage(file='underline.png')
underlineButton = Button(tool_bar, image=underlineImage, command=underline_text)
underlineButton.grid(row=0, column=4, padx=5)

fontcolorImage = PhotoImage(file='font_color.png')
fontcolorButton = Button(tool_bar, image=fontcolorImage, command=color_select)
fontcolorButton.grid(row=0, column=5, padx=5)

leftAllignImage = PhotoImage(file='left.png')
leftAllignButton = Button(tool_bar, image=leftAllignImage, command=align_left)
leftAllignButton.grid(row=0, column=6, padx=5)

centerAllignImage = PhotoImage(file='center.png')
centerAllignButton = Button(tool_bar, image=centerAllignImage, command=align_center)
centerAllignButton.grid(row=0, column=8, padx=5)

rightAllignImage = PhotoImage(file='right.png')
rightAllignButton = Button(tool_bar, image=rightAllignImage, command=align_right)
rightAllignButton.grid(row=0, column=7, padx=5)


#textarea
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
textarea = Text(root, yscrollcommand=scrollbar.set, font=('arial', '12'), undo=True)
textarea.pack(expand=True, fill=BOTH)
scrollbar.config(command=textarea.yview)

status_bar = Label(root, text='Status Bar')
status_bar.pack(side=BOTTOM)

textarea.bind('<<Modified>>', statusbar_function)

editmenu = Menu(menubar, tearoff=False)
editmenu.add_command(label='Undo', accelerator='Ctrl+Z', image=undoImage, compound=LEFT, command=lambda : textarea.event_generate('<Control z>'))
editmenu.add_command(label='Redo', accelerator='Ctrl+Y', image=redoImage, compound=LEFT, command=lambda : textarea.event_generate('<Control y>'))
editmenu.add_command(label='Cut', accelerator='Ctrl+X', image=cutImage, compound=LEFT, command=lambda : textarea.event_generate('<Control x>'))
editmenu.add_command(label='Copy', accelerator='Ctrl+C', image=copyImage, compound=LEFT, command=lambda : textarea.event_generate('<Control c>'))
editmenu.add_command(label='Paste', accelerator='Ctrl+V', image=pasteImage, compound=LEFT, command=lambda : textarea.event_generate('<Control v>'))
editmenu.add_command(label='Select All', accelerator='Ctrl+A', image=selectImage, compound=LEFT, command=lambda : textarea.event_generate('<Control a>'))
editmenu.add_command(label='Clear', image=clearImage, compound=LEFT, command=clear_all)
editmenu.add_command(label='Find', accelerator='Ctrl+F', image=findImage, compound=LEFT, command=Find)
menubar.add_cascade(label='Edit', menu=editmenu)


#viewmenu
show_toolbar = BooleanVar()
show_statusbar = BooleanVar()

imgtoolbar = PhotoImage(file='tool_bar.png')
imgstatusbar = PhotoImage(file = 'status_bar.png')

viewmenu = Menu(menubar, tearoff=False)
viewmenu.add_checkbutton(label='Tool Bar', variable=show_toolbar, onvalue=True, offvalue=False, image=imgtoolbar, compound=LEFT, command = toolbarFunc)
show_toolbar.set(True)
viewmenu.add_checkbutton(label='Status Bar', variable=show_statusbar, onvalue=True, offvalue=False, image=imgstatusbar, compound=LEFT, command = statusbarFunc)
show_statusbar.set(True)
menubar.add_cascade(label='View', menu=viewmenu)

#themesmenu

themesmenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label='Themes', menu=themesmenu)

theme_choice = StringVar()

lightimage=PhotoImage(file = 'light_default.png')
darkimage=PhotoImage(file = 'dark.png')
redimage=PhotoImage(file = 'red.png')
monokaiimage=PhotoImage(file = 'monokai.png')

themesmenu.add_radiobutton(label='Light Default', image=lightimage, variable=theme_choice, compound=LEFT, command=lambda :changebg('white', 'black'))
themesmenu.add_radiobutton(label='Dark', image=darkimage, variable=theme_choice, compound=LEFT, command=lambda: changebg('gray28','white'))
themesmenu.add_radiobutton(label='Pink', image=redimage, variable=theme_choice, compound=LEFT, command=lambda: changebg('pink', 'blue'))
themesmenu.add_radiobutton(label='Monokai', image=monokaiimage, variable=theme_choice, compound=LEFT, command=lambda :changebg('orange', 'white'))

root.bind('<Control-o>', open_file)
root.bind('<Control-n>', new_file)
root.bind('<Control-s>', save_file)
root.bind('<Control-Alt-s>', saveas_file)
root.bind('<Control-q>', iexit)
root.bind('<Control-p>', printout)


root.mainloop()
