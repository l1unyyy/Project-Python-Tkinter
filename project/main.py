import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Scrollbar, Listbox , Scale
import qrcode
from PIL import Image, ImageTk, ImageDraw
import requests
from datetime import datetime
import os
import csv
import pyshorteners
import colorsys



def history_open():
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

def open_vCard():
    win = tk.Toplevel()
    win.title("QR-visit")
    win.geometry("500x700")
    label_n = ttk.Label(win, text = "Name and Surname")
    label_n.pack(pady = 2)

    entry_n = ttk.Entry(win, width = 40)
    entry_n.pack()

    label_num = ttk.Label(win, text = "Phone : ")
    label_num.pack(pady = 2)

    entry_num = ttk.Entry(win, width = 40)
    entry_num.pack()

    label_em = ttk.Label(win, text = "Email : ")
    label_em.pack(pady = 2)

    entry_em = ttk.Entry(win, width = 40)
    entry_em.pack()

    label_comp = ttk.Label(win, text = "Company : ")
    label_comp.pack(pady = 2)
    
    entry_comp = ttk.Entry(win, width = 40)
    entry_comp.pack()


    lbl_qr = ttk.Label(win)
    lbl_qr.pack(pady = 10)

    def generate_card():
        name = entry_n.get().strip()
        phone = entry_num.get().strip()
        email = entry_em.get().strip()
        company = entry_comp.get().strip()
    
        if not name or not phone:
            messagebox.showerror("Error", "Name and phone number are required")
            return
        
        qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
        )
    
        name_clean = name.replace(',', '').replace(';', '')
        phone_clean = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        email_clean = email.replace(',', '').replace(';', '')
        company_clean = company.replace(',', '').replace(';', '')

        fullbase = f"{name_clean}, {phone_clean}"
        mecard = f"MECARD:N:{name_clean};TEL:{phone_clean};EMAIL:{email_clean};ORG:{company_clean};"
        qr.add_data(mecard)
        qr.make(fit=True)
    
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save("vcard.png")
    
        qr_image_tk = ImageTk.PhotoImage(Image.open("vcard.png"))
        lbl_qr.config(image=qr_image_tk)
        lbl_qr.image = qr_image_tk

        messagebox.showinfo("Success", "QR code generated! Scan with iPhone camera.")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("data.csv", "a", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([now, fullbase , "vCard generated"])

        
    btn_gen = ttk.Button(win, text = "Generate vCard", command = generate_card )
    btn_gen.pack(pady = 10)


    win.mainloop()




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




def settings():
    win = tk.Toplevel()
    win.title("Settings")
    win.geometry("400x500")

    button_clear = tk.Button(win, text = "Clear History", borderwidth = 0, command = clear_history)
    button_clear.pack(padx = 0, pady = 200)
    



    win.mainloop()
    


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
win.configure(bg="#FFFEFE")

label_url = tk.Label(win , text = "Enter URL :",bg = "#FFFEFE" ,font = ("Arial 14 bold") , borderwidth = 0, fg = "black")
label_url.pack(padx = 20,pady = 50)

entry_url = ttk.Entry(win , font = ("Arial 14") , width = 40)
entry_url.pack(padx = 20,pady = 10)



button_generate = ttk.Button(win, text = "Generate QR Code",command = generate_qrcode, width = 20)
button_generate.pack(padx = 20,pady = 10)

button_parsing = ttk.Button(win, text = "Parsing URL", command = parsing , width = 20)
button_parsing.pack(padx = 20,pady = 10)

button_history = ttk.Button(win, text = "History", command = history_open, width = 7)
button_history.place(x = 470,y = 50)

button_short = ttk.Button(win, text = "Shorter URL" , command = short_url, width = 20)
button_short.pack(padx = 20,pady = 10)

button_vcard = ttk.Button(win, text = "Generate vCard", command = open_vCard, width = 20)
button_vcard.pack(padx = 20, pady = 10)

button_exit = ttk.Button(win, text = "Exit", command = win.destroy, width = 20)
button_exit.pack(padx = 20,pady = 10)

button_settings = ttk.Button(win, text = "Settings ⚙️", command = settings)
button_settings.place(x = 20,y = 50)




label_qr = tk.Label(win, bg = "#000000")
label_qr.pack(padx = 20,pady = 10)


label_time = tk.Label(win, font=("Arial", 14), fg="black", bg="#FFFEFE", borderwidth = 0)
label_time.place( x = 265 , y = 650)




update_time()
win.mainloop()