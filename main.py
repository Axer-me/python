import os
import shutil
import pygame
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image
import json
import numpy as np
from numpy import genfromtxt
from pandas import read_csv



#import wadpy

class FileManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Resource File Manager")
        self.root.geometry("600x400")
        self.frame = Frame(self.root)
        self.frame.pack(fill=BOTH, expand=True)
        self.file_list = Listbox(self.frame)
        self.file_list.pack(side=LEFT, fill=BOTH, expand=True)
        self.file_list.bind('<Double-1>', self.open_file)
        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL, command=self.file_list.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.file_list.config(yscrollcommand=self.scrollbar.set)
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        dir = '...'
        self.word_editor = Text(height=5, wrap="word")
        self.word_editor.pack(anchor=SW, fill=X)
        self.convert_button = tk.Button(self.root,text="Преобразовать файл",
                                        command=self.convert)
        self.convert_button.pack(anchor="nw", side=TOP)
        self.revert_button1 = tk.Button(self.root,  text="Достать из файла изображение",
                                       command=self.convert_back_image  )
        self.revert_button1.pack(anchor="se",  side=BOTTOM)
        self.revert_button2 = tk.Button(self.root, text="Достать из .dat файла csv",
                                       command=self.convert_back_csv)
        self.revert_button2.pack(anchor="se", side=BOTTOM)
        self.copy_button = tk.Button(self.root, text="Копировать",
                                        command=self.copy)
        self.copy_button.pack(anchor="sw", side=BOTTOM)
        self.move_button = tk.Button(self.root, text="Переместить",
                                     command=self.move)
        self.move_button.pack(anchor="sw", side=BOTTOM)
        self.delete_button = tk.Button(self.root, text="Удалить",
                                     command=self.delete)
        self.delete_button.pack(anchor="sw", side=BOTTOM)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_directory)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

    def open_directory(self):
        directory = filedialog.askdirectory()
        global dir
        dir = directory
        if directory:
            self.file_list.delete(0, END)
            for file in os.listdir(directory):
                self.file_list.insert(END, os.path.join(directory, file))

    def delete(self):
        selected_file = self.file_list.get(self.file_list.curselection())
        os.remove(selected_file)
        directory = selected_file[0:selected_file.find("\\")]
        self.file_list.delete(0, END)
        for file in os.listdir(directory):
            self.file_list.insert(END, os.path.join(directory, file))

    def copy(self):
        selected_file = self.file_list.get(self.file_list.curselection())
        directory = filedialog.askdirectory()
        if (directory == selected_file[0:selected_file.find("\\")] ):
            pass
        else:
            shutil.copy(selected_file, directory)
            self.file_list.delete(0, END)
            for file in os.listdir(directory):
                self.file_list.insert(END, os.path.join(directory, file))

    def move(self):
        selected_file = self.file_list.get(self.file_list.curselection())
        directory = filedialog.askdirectory()
        shutil.move(selected_file, directory)
        directory = selected_file[0:selected_file.find("\\")]
        self.file_list.delete(0, END)
        for file in os.listdir(directory):
            self.file_list.insert(END, os.path.join(directory, file))
    def open_file(self, event):
        selected_file = self.file_list.get(self.file_list.curselection())
        if selected_file.endswith('.mp3'):
            self.play_mp3(selected_file)
        elif selected_file.endswith(('.png', '.jpg', '.jpeg')):
            self.show_image(selected_file)
        elif selected_file.endswith('.json'):
            self.show_json(selected_file)
        elif selected_file.endswith('.dat'):
            self.extract_data(selected_file)
        elif selected_file.endswith('.csv'):
            self.show_csv(selected_file)
        elif selected_file.endswith('.txt'):
            self.show_txt(selected_file)
        elif selected_file.endswith('.py'):
            self.show_py(selected_file)
        else :
            self.show_random_file(selected_file)

    def convert(self):
        global dir
        print(dir)
        selected_file = self.file_list.get(self.file_list.curselection())
        if selected_file.endswith('.mp3'):
            pass
        elif selected_file.endswith(('.png', '.jpg', '.jpeg')):
            self.convert_image(selected_file)
        elif selected_file.endswith('.json'):
            self.convert_json(selected_file)
        elif selected_file.endswith('.dat'):
            pass
        elif selected_file.endswith('.csv'):
            self.convert_csv(selected_file)
        else: pass

    def show_random_file(self,file_path):
        os.startfile(file_path)

    #def convert_mp3(self, file):
    #    sound = AudioSegment.from_mp3(file)
    #    raw_data = sound._data
    #    print(raw_data)
    def convert_back_image(self):
        selected_file = self.file_list.get(self.file_list.curselection())
        data = genfromtxt(selected_file)
        image = Image.fromarray(data)
        image.show()
    def convert_image(self, file):
        global dir
        image = Image.open(file)
        data = np.asarray(image)
        print(data.shape)
        np.savetxt('image_array.csv', data)

    def convert_csv(self, file):
        data = read_csv(file)
        data.to_csv('converted_csv.dat')

    def convert_back_csv(self, ):
        selected_file = self.file_list.get(self.file_list.curselection())
        data = pd.read_table(selected_file)
        data.to_csv('converted_dat.csv', index = FALSE)
    def convert_json(self, dir):
        print("not ready")


    def play_mp3(self, file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        self.word_editor.delete("1.0", END)

    def show_py(self, file_path):
        with open (file_path, 'r', encoding='utf-8') as f:
            data = f.read()
            self.word_editor.delete("1.0", END)
            self.word_editor.insert("1.0", data)
    def show_txt(self, file_path):
        with open (file_path, 'r', encoding='utf-8') as f:
            data = f.read()
            self.word_editor.delete("1.0", END)
            self.word_editor.insert("1.0", data)


    def show_csv(self, file_path):
        data = pd.read_csv(file_path)
        self.word_editor.delete("1.0", END)
        self.word_editor.insert("1.0", data)
    def show_image(self, file_path):
        print(file_path)
        image = Image.open(file_path)
        image.show()
        self.word_editor.delete("1.0", END)
    #    data = np.asarray(image)
    #    print(data.shape)
    #    image1 = Image.fromarray(data)
    #    image1.show()

    def show_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.word_editor.delete("1.0", END)
            self.word_editor.insert("1.0", data)

    def extract_data(self, file_path):
        data= pd.read_table(file_path)
        self.word_editor.delete("1.0", END)
        self.word_editor.insert("1.0", data)
        #with open(file_path, 'rb') as file:
        #    data = file.read()
        #    self.word_editor.delete("1.0", END)
        #    data_mod = struct.unpack('i' * (len(data) // 4), data)
        #    self.word_editor.insert("1.0", data_mod)


if __name__ == "__main__":
    root = Tk()
    app = FileManager(root)
    root.mainloop()
