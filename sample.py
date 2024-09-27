import os
import pygame
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import json
import struct
import numpy as np
import sys
import csv
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

        self.convert_button = tk.Button(self.root,text="Преобразовать в .dat файл", command=self.convert)
        self.convert_button.pack(anchor="nw", side=LEFT)

        self.revert_button = tk.Button(self.root,  text="Достать из .dat файла",  )
        self.revert_button.pack(anchor="se",  side=BOTTOM)

        self.opendat_button = tk.Button(self.root, text='Открыть .dat файл', )
        self.opendat_button.pack(anchor="ne", side=RIGHT)

        self.file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_directory)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

    def start_converting(self):
        global dir
        self.convert(self, dir)
    def open_directory(self):
        directory = filedialog.askdirectory()
        global dir
        dir = directory
        #d = directory
        #a = list(d)
        #dir = ''
        #for i in range (0,len(a)):
        #    if a[i] == '/':
        #            dir = dir + '\\'
        #            dir = dir + '\\'
        #    else:
         #       dir = dir + a[i]

        if directory:
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

    def convert(self):
        global dir
        print(dir)

        #my_list = []
        #for root, dirs, files in os.walk(dir):
            #my_list.extend([os.path.join(root, file) for file in files ])
        #print(my_list)
        #result = pd.DataFrame()
        #for file in my_list:
            #df = pd.read_excel(file)
            #result = result.append(df)
        selected_file = self.file_list.get(self.file_list.curselection())
        if selected_file.endswith('.mp3'):
            self.convert_mp3(selected_file)
        elif selected_file.endswith(('.png', '.jpg', '.jpeg')):
            self.convert_image(selected_file)
        elif selected_file.endswith('.json'):
            self.convert_json(selected_file)
        elif selected_file.endswith('.dat'):
            pass


    def convert_image(self, file):
        global dir
        image = Image.open(file)
        data = np.asarray(image)
        print(data.shape)
        np.savetxt('image_array.csv', dir, data)

    def convert_json(self, dir):
        print(1)


    def play_mp3(self, file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        self.word_editor.delete("1.0", END)

    def show_image(self, file_path):
        print(file_path)
        image = Image.open(file_path)
        image.show()
        self.word_editor.delete("1.0", END)
        data = np.asarray(image)
        print(data.shape)
        image1 = Image.fromarray(data)
        image1.show()

    def show_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            print(data)
            self.word_editor.delete("1.0", END)
            self.word_editor.insert("1.0", data)

    def extract_data(self, file_path):
        with open(file_path, 'rb') as file:
            data = file.read()
            self.word_editor.delete("1.0", END)
            data_mod = struct.unpack('i' * (len(data) // 4), data)
            self.word_editor.insert("1.0", data_mod)


if __name__ == "__main__":
    root = Tk()
    app = FileManager(root)
    root.mainloop()
