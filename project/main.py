import tkinter as tk
from tkinter import ttk, messagebox
import qrcode
from PIL import Image, ImageTk
import requests


def parsing():
    text1 = entry_url.get()
    r = requests.get(f"{text1}")
    if not text1:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return
    else:
        if r.status_code == 200:
            print(r.ok)
    
    

def generate_qrcode():
    url = entry_url.get()
    if not url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return
    
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,        
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image.save("qrcode.png")

    qr_image_tk = ImageTk.PhotoImage(Image.open("qrcode.png"))
    label_qr.config(image=qr_image_tk)
    label_qr.image = qr_image_tk
    messagebox.showinfo("Success", "QR Code generated successfully!")






win = tk.Tk()
win.title("QR Code Generator")
win.geometry("600x700")
win.resizable(False , False)
win.configure(bg="#ffffff")


label_url = ttk.Label(win , text = "Enter URL:", font = ("Arial 14 bold") )
label_url.pack(padx = 20,pady = 50)

entry_url = ttk.Entry(win , font = ("Arial 14") , width = 40)
entry_url.pack(padx = 20,pady = 10)



button_generate = ttk.Button(win, text = "Generate QR Code",command = generate_qrcode, width = 20)
button_generate.pack(padx = 20,pady = 10)

button_parsing = ttk.Button(win, text = "Parsing url", command = parsing , width = 20)
button_parsing.pack(padx = 20,pady = 20)

button_exit = ttk.Button(win, text = "Exit", command = win.destroy, width = 20)
button_exit.pack(padx = 20,pady = 10)

label_qr = ttk.Label(win)
label_qr.pack(padx = 20,pady = 10)


win.mainloop()