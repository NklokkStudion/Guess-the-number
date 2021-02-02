from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image
import numpy as np
from sklearn.neural_network import MLPClassifier
import pickle
import numpy
import matplotlib.pyplot as plt

def predict_digit(img):
    # изменение рзмера изобржений на 28x28
    img = img.resize((28,28))
    # конвертируем rgb в grayscale
    img = img.convert('P')
    # изменение размерности для поддержки модели ввода и нормализации
    img = np.array(img)
    img = img.reshape(784)
    # предстказание цифры
    loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
    #return loaded_model.predict([img])

    # проценты
    pr = loaded_model.predict_proba([img])
    predictions = []
    for i in pr[0]:
        predictions.append(float(i))
    return predictions

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Guess the digit')
        self.x = self.y = 0
        
        # Создание элементов
        self.canvas = tk.Canvas(self, width=300, height=300, bg = "black", cursor="cross")
        self.label = tk.Label(self, text="Думаю..", font=("Helvetica", 17))
        self.classify_btn = tk.Button(self, text = "Распознать", command = self.classify_handwriting) 
        self.button_clear = tk.Button(self, text = "Очистить", command = self.clear_all)

        # Сетка окна
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)

        self.canvas.bind("<B1-Motion>", self.draw_lines)
        
    def clear_all(self):
        self.canvas.delete("all")
        
    def classify_handwriting(self):
        HWND = self.canvas.winfo_id() 
        rect = win32gui.GetWindowRect(HWND)
        im = ImageGrab.grab(rect)
        
        digit = predict_digit(im)

        line_new = '0: {:<12}\n1: {:<12}\n2: {:<12}\n3: {:<12}\n4: {:<12}\n5: {:<12}\n6: {:<12}\n7: {:<12}\n8: {:<12}\n9: {:<12}\n'.format('%.2f'% (digit[0]*100),'%.2f'% (digit[1]*100),'%.2f'% (digit[2]*100),'%.2f'% (digit[3]*100),'%.2f'% (digit[4]*100),'%.2f'% (digit[5]*100),'%.2f'% (digit[6]*100),'%.2f'% (digit[7]*100),'%.2f'% (digit[8]*100),'%.2f'% (digit[9]*100),) 
        self.label.configure(text= str(line_new))

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=8
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='white', outline='white')
        self.classify_handwriting()


app = App()
mainloop()