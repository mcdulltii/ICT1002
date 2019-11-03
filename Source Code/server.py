#!python3
import runfunction
#import "custom_function"
import pandas as pd
import chardet
import os
import http.server
import sys
from subprocess import Popen
import re
import threading
import time
from tkinter import filedialog, Tk, messagebox, Button, Label, PhotoImage, Listbox, StringVar, Toplevel


'''Initialise Tkinter GUI'''
root = Tk()
root.withdraw()
gui = Toplevel()
gui.title('PythonGUI') #Title
gui.iconbitmap('resources/snake.ico') #GUI Icon
gui.minsize(500,540) #Size of GUI
gui.attributes('-topmost', True) #Set GUI to always be the topmost window

opened = [0, 0]
httpd = ()

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    '''HTTP Server Class'''

    def do_AUTHHEAD(self):
        '''Redundant'''
        print('send header')
        self.send_response(100)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        '''Header for HTTP Server'''
        print('send header')
        self.send_response(300)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        '''GET Request to the HTTP Server'''
        root = os.getcwd()+'/resources' #Retrieve file root
        if self.path == "/":
            filename = root + '/index.html' #Retrieve index.html
        else:
            filename = root + self.path

        self.send_response(200)
        if filename[-4:] == ".css":
            self.send_header("Content-type", "text/css") #Retrieve stylesheets
        elif filename[-3:] == ".js":
            self.send_header("Content-type", "application/javascript") #Retrieve javascripts
        elif filename[-5:] == ".json":
            self.send_header("Content-type", "application/javascript") #Retrieve json
        elif filename[-4:] == ".ico":
            self.send_header("Content-type", "image/x-icon") #Retrieve webpage icon
        else:
            self.send_header("Content-type", "text/html") #Retrieve html
        self.end_headers()
        with open(filename, 'rb') as fh:
            html = fh.read()
            self.wfile.write(html) #Return index.html from GET Request

    def do_POST(self):
        '''POST Request to the HTTP Server'''
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length) #Read POST Data
        decode_data = post_data.decode('ASCII') #Decode ASCII
        read_data = re.findall("(\w+)=([+\w+]*)", decode_data) #REGEX to find POST input
        resetted = False
        with open("resources/import.txt", "w") as files: #Export to import.txt under resource folder
            for data in read_data:
                if data[0].lower() == 'reset':
                    reset_server()
                    resetted = True
                    break
                # if data[1] == '':
                #     resetted = True
                #     break
                files.write(data[0]+', ')
                files.write(data[1]+'\n')
        self.send_response(300)
        self.end_headers()
        if not resetted:
            runfunction.main() #Runs runfunction.py


def open_file(num):
    '''Opens only comma-delimited files (eg. CSV)'''
    global tempdir, tempdir2, opened
    try:
        if num=='1': #First Selection
            tempdir = filedialog.askopenfilename(filetypes = (("Template files", "*.csv"), ("All files", "*")))
            if tempdir[-3:].lower() not in ['csv', 'prn', 'xls', 'ods'] and tempdir[-4:].lower() not in ['xlsx', 'xltx', 'xlsm', 'xlsb']:
                messagebox.showerror("Warning", "Choose a CSV file!") #Error messagebox
                opened[0] = 0
            else:
                label_one = Label(gui, text="1st file: "+tempdir).grid()
                opened[0] = 1
        else: #Second Selection
            tempdir2 = filedialog.askopenfilename(filetypes = (("Template files", "*.csv"), ("All files", "*")))
            if tempdir2[-3:].lower() not in ['csv', 'prn', 'xls', 'ods'] and tempdir2[-4:].lower() not in ['xlsx', 'xltx', 'xlsm', 'xlsb']:
                messagebox.showerror("Warning", "Choose a CSV file!") #Error messagebox
                opened[1] = 0
            else:
                label_two = Label(gui, text="2nd file: "+tempdir2).grid()
                opened[1] = 1
    except:
        messagebox.showerror("Warning", "Error!") #Catch errors from opening files
        opened = [0, 0]

    if opened == [1,1]: # Prevent user from selecting the same *path* twice
        if tempdir == tempdir2:
            messagebox.showerror("Warning", "Choose different CSV file for the 2nd option!")
            opened = [1,0]

    # if tempdir2 == tempdir:
    #     messagebox.showerror("Warning", "Choose different CSV files!")  # Catch errors from opening files
    #     opened = [0, 0]


def selection(browse):
    '''Sets up HTTP Server, opens chosen browser'''
    global browsers, opened
    is_open = [1 for x in opened if x is 1]
    if len(is_open) != 2:
        messagebox.showerror("Warning", "Choose 2 valid files!")
    else:
        try:
            gui.destroy() #Close Tkinter GUI
            threading.Thread(target=write_csv, daemon=True).start()
            if sys.platform == 'win32': #Opens browser
                Popen(['start', browse+'.exe' , 'http://localhost:8000'], shell=True)
            elif sys.platform == 'darwin':
                if browse == 'chrome': browse = "'Google Chrome'"
                Popen('open -a '+browse+' http://localhost:8000',shell=True)
            else:
                try:
                    Popen(['xdg-open', 'http://localhost:8000'],shell=True)
                except:
                    messagebox.showerror("Warning", "Cannot open browser!")
            start() #Start HTTP server
        except:
            messagebox.showerror("Warning", "Error!")
            sys.exit()


def reset_server():
    '''Restarts Choosing of CSV Files'''
    global tempdir, tempdir2, opened, gui, httpd
    threading.Thread(target=httpd.shutdown, daemon=True).start()
    threading.Thread(target=httpd.server_close, daemon=True).start()
    gui = Toplevel()
    gui.title('PythonGUI') #Title
    gui.iconbitmap('resources/snake.ico') #GUI Icon
    gui.minsize(500,540) #Size of GUI
    gui.attributes('-topmost', True) #Set GUI to always be the topmost window
    opened = [0, 0]
    tempdir, tempdir2 = '', ''
    photo = PhotoImage(file="resources/gui.png") #Logo
    label_five = Label(gui, image=photo).grid(pady=10)
    btn_one = Button(gui, text="Choose 1st CSV file", command=lambda: open_file('1')).grid(pady=4) #CSV Selection
    btn_two = Button(gui, text="Choose 2nd CSV file", command=lambda: open_file('2')).grid(pady=4)
    browsers = {'Firefox':"firefox", 'Chrome':"chrome", 'Opera':"opera", 'Iexplore':"iexplore"}
    items = StringVar(value=tuple(sorted(browsers.keys())))
    listbox = Listbox(gui, listvariable=items, width=40, height=5) #Browser Selection
    listbox.grid(column=0, row=4, rowspan=6, pady=10)
    selectButton = Button(gui, text='Select Browser', underline=0, command=lambda: selection(listbox.selection_get()))
    selectButton.grid(pady=10)
    gui.mainloop()


def write_csv():
    '''Write headers to txt files'''
    global tempdir, tempdir2
    encode = chardet.detect(open(tempdir,'rb').read())['encoding'] #Detect CSV encodings
    encode2 = chardet.detect(open(tempdir2,'rb').read())['encoding']
    df = pd.read_csv(tempdir, delimiter=",", encoding=encode) #Reads CSV file
    df2 = pd.read_csv(tempdir2, delimiter=",", encoding=encode2)
    with open("resources/dir.txt", "w") as files:
        files.write(tempdir+','+encode+'\n')
        files.write(tempdir2+','+encode2)
    with open("resources/columns1.txt", "w") as files: #Export to columns1.txt
        for value in df.columns.values:
            files.write(value+', ')
    with open("resources/columns2.txt", "w") as files: #Export to columns2.txt
        for value in df2.columns.values:
            files.write(value+', ')
    with open("resources/columns0.txt", "w") as files: #Export to columns0.txt
        for value in df.columns.values:
            files.write(value+', ')
        for value in df2.columns.values:
            files.write(value+', ')


def start(HandlerClass = SimpleHTTPRequestHandler, ServerClass = http.server.HTTPServer, port=8000):
    '''Sets up HTTP Server'''
    global httpd
    server_address = ('', port) #Sets server to port 8000
    httpd = ServerClass(server_address, HandlerClass)
    print('\nStarting httpd on port {}'.format(port))
    time.sleep(5)
    httpd.serve_forever() #Hosts HTTP Server on localhost


if __name__ == "__main__":
    '''Styling of Tkinter GUI'''
    photo = PhotoImage(file="resources/gui.png") #Logo
    label_five = Label(gui, image=photo).grid(pady=10)
    btn_one = Button(gui, text="Choose 1st CSV file", command=lambda: open_file('1')).grid(pady=4) #CSV Selection
    btn_two = Button(gui, text="Choose 2nd CSV file", command=lambda: open_file('2')).grid(pady=4)
    browsers = {'Firefox':"firefox", 'Chrome':"chrome", 'Opera':"opera", 'Iexplore':"iexplore"}
    items = StringVar(value=tuple(sorted(browsers.keys())))
    listbox = Listbox(gui, listvariable=items, width=40, height=5) #Browser Selection
    listbox.grid(column=0, row=4, rowspan=6, pady=10)
    selectButton = Button(gui, text='Select Browser', underline=0, command=lambda: selection(listbox.selection_get()))
    selectButton.grid(pady=10)
    gui.mainloop()
