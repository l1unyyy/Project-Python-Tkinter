import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Scrollbar, Listbox
import qrcode
from PIL import Image, ImageTk
import requests
from datetime import datetime
import os
import csv
import pyshorteners


def toplevel_open():
    root = tk.Toplevel()
    root.title("History")
    root.geometry("800x600")
    root.resizable(False, False)

    tree = ttk.Treeview(root, columns=("time", "url", "title"), show="headings", height=20)
    
    tree.heading("time", text="Time")
    tree.heading("url", text="URL")
    tree.heading("title", text="Title")
    
    tree.column("time", width=150, anchor="w")
    tree.column("url", width=300, anchor="w")
    tree.column("title", width=300, anchor="w")
    
    
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y", pady=10)
    


    if os.path.exists("data.csv"):
        with open("data.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3:
                    tree.insert("", "end", values=(row[0], row[1], row[2]))
        
    root.mainloop()

def short_url():
    url = entry_url.get()
    if not url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return
    try:
        s = pyshorteners.Shortener()
        short_url = s.tinyurl.short(url)  
        entry_url.delete(0, tk.END) 
        entry_url.insert(0, short_url)  
        messagebox.showinfo("Success", "URL shortened successfully!")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("data.csv", "a", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([now, url, f"Short URL  -  {short_url}"])
    except:
        messagebox.showerror("Error", "Failed to connect to the server")
        return

def clear_history():
    if messagebox.askyesno("Confirm", "Are you sure you want to clear all history?"):
        with open("data.csv", "w", encoding="utf-8") as f:
            pass
        messagebox.showinfo("Success", "History cleared!")


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


        title = "No title"
        try:
            html = r.text
            start = html.find("<title>")
            if start != -1:
                end = html.find("</title>", start)
                if end != -1:
                    title = html[start+7:end].strip()
        except:
            pass


        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("data.csv", "a", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([now, text1, f"Title  -  {title}"])

        messagebox.showinfo("Success", f"Page parsed!\nTitle: {title}")


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
        box_size=8,
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

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("data.csv", "a", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([now, url, "QR Code generated"])
    
    


win = tk.Tk()
win.title("QR Code Generator")
win.geometry("600x700")
win.resizable(False , False)
win.configure(bg="#000000")


label_url = tk.Label(win , text = "Enter URL :", font = ("Arial 14 bold") , borderwidth = 0, bg = "#000000")
label_url.pack(padx = 20,pady = 50)

entry_url = ttk.Entry(win , font = ("Arial 14") , width = 40)
entry_url.pack(padx = 20,pady = 10)



button_generate = ttk.Button(win, text = "Generate QR Code",command = generate_qrcode, width = 20)
button_generate.pack(padx = 20,pady = 10)

button_parsing = ttk.Button(win, text = "Parsing URL", command = parsing , width = 20)
button_parsing.pack(padx = 20,pady = 10)

button_history = ttk.Button(win, text = "History", command = toplevel_open, width = 7)
button_history.place(x = 470,y = 50)

button_short = ttk.Button(win, text = "Shorter URL" , command = short_url, width = 20)
button_short.pack(padx = 20,pady = 10)

button_exit = ttk.Button(win, text = "Exit", command = win.destroy, width = 20)
button_exit.pack(padx = 20,pady = 10)


label_qr = tk.Label(win, bg = "#000000")
label_qr.pack(padx = 20,pady = 10)


label_time = tk.Label(win, font=("Arial", 14), fg="white", bg="black", borderwidth = 0)
label_time.place( x = 265 , y = 650)




update_time()
win.mainloop()