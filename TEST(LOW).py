import tkinter as tk
from tkinter import messagebox

FILE = "tasks.txt"
tasks = []

def load():
    try:
        with open(FILE, "r") as f:
            for line in f:
                if "|" in line:
                    name, status, desc = line.strip().split("|", 2)
                    tasks.append([name, status, desc])
    except FileNotFoundError:
        pass

def save():
    with open(FILE, "w") as f:
        for t in tasks:
            f.write(f"{t[0]}|{t[1]}|{t[2]}\n")

def refresh():
    listbox.delete(0, tk.END)
    for t in tasks:
        mark = "[DONE]" if t[1] == "Done" else "[    ]"
        listbox.insert(tk.END, f"{mark} {t[0]} - {t[2]}")

def add():
    name = e_name.get().strip()
    desc = e_desc.get().strip()
    if not name or not desc:
        messagebox.showwarning("Warning", "Fill in all fields!")
        return
    tasks.append([name, "Pending", desc])
    save()
    refresh()
    e_name.delete(0, tk.END)
    e_desc.delete(0, tk.END)

def done():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Warning", "Select a task!")
        return
    tasks[sel[0]][1] = "Done"
    save()
    refresh()

def delete():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Warning", "Select a task!")
        return
    tasks.pop(sel[0])
    save()
    refresh()

# --- Window ---
load()
root = tk.Tk()
root.title("To-Do List")
root.geometry("480x380")

tk.Label(root, text="Task Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
e_name = tk.Entry(root, width=30)
e_name.grid(row=0, column=1, pady=5)

tk.Label(root, text="Description:").grid(row=1, column=0, padx=10, sticky="w")
e_desc = tk.Entry(root, width=30)
e_desc.grid(row=1, column=1)

tk.Button(root, text="Add",    bg="green",  fg="white", width=12, command=add).grid(row=2, column=0, pady=8)
tk.Button(root, text="Done",   bg="blue",   fg="white", width=12, command=done).grid(row=2, column=1, pady=8)

listbox = tk.Listbox(root, width=60, height=10)
listbox.grid(row=3, column=0, columnspan=2, padx=10)

tk.Button(root, text="Delete", bg="red", fg="white", width=12, command=delete).grid(row=4, column=0, columnspan=2, pady=8)

refresh()
root.mainloop()