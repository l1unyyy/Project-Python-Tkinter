import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Scrollbar, Listbox
import qrcode
from PIL import Image, ImageTk
import requests
from datetime import datetime

def toplevel_open():
    root = tk.Toplevel()
    root.title("History")
    root.geometry("600x500")

    scrollbar = tk.Scrollbar(root, width = 5, length = 20)
    scrollbar.pack()
    listbox = tk.Listbox(root, width = 50, height = 20)
    listbox.pack()
    
    root.mainloop()



def save_in_csv():
    pass

def parsing():
    text1 = entry_url.get()
    if not text1:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return
    try:
        r = requests.get(text1)
        if r.status_code != 200:
            messagebox.showerror("Error", f"Status code: {r.status_code}")
            return
        print(r.content)
    except:
        messagebox.showerror("Error", "Failed to connect to the server")
        return

def update_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")  
    label_time.config(text=current_time)
    win.after(1000, update_time)  

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
win.configure(bg="#000000")


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

button_history = ttk.Button(win, text = "History", command = toplevel_open, width = 7)
button_history.place(x = 470,y = 50)


label_qr = ttk.Label(win)
label_qr.pack(padx = 20,pady = 10)

label_time = tk.Label(win, font=("Arial", 14), fg="white", bg="black")
label_time.pack()


update_time()
win.mainloop()