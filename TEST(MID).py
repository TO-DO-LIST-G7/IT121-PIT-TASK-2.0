import tkinter as tk
from tkinter import ttk, messagebox
import os

FILE = "tasks.txt"
tasks = []

# ── File Handling ──────────────────────────────

def load():
    try:
        with open(FILE, "r") as f:
            for line in f:
                line = line.strip()
                if "|" in line:
                    parts = line.split("|", 2)
                    if len(parts) == 3:
                        tasks.append({"name": parts[0], "status": parts[1], "desc": parts[2]})
    except FileNotFoundError:
        pass
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not load tasks:\n{e}")

def save():
    try:
        with open(FILE, "w") as f:
            for t in tasks:
                f.write(f"{t['name']}|{t['status']}|{t['desc']}\n")
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save tasks:\n{e}")

def append_to_file(task):
    try:
        with open(FILE, "a") as f:
            f.write(f"{task['name']}|{task['status']}|{task['desc']}\n")
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not append task:\n{e}")

# ── Task Actions ───────────────────────────────

def add_task():
    name = entry_name.get().strip()
    desc = entry_desc.get().strip()

    if not name:
        messagebox.showwarning("Validation", "Task name cannot be empty!")
        return
    if not desc:
        messagebox.showwarning("Validation", "Description cannot be empty!")
        return

    task = {"name": name, "status": "Pending", "desc": desc}
    tasks.append(task)
    append_to_file(task)   # append only — no full rewrite needed
    refresh_table()
    entry_name.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    entry_name.focus()

def mark_done():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Please select a task first.")
        return
    i = tree.index(selected[0])
    if tasks[i]["status"] == "Done":
        messagebox.showinfo("Info", "Task is already done.")
        return
    tasks[i]["status"] = "Done"
    save()
    refresh_table()

def delete_task():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Please select a task first.")
        return
    i = tree.index(selected[0])
    if messagebox.askyesno("Confirm", f"Delete \"{tasks[i]['name']}\"?"):
        tasks.pop(i)
        save()
        refresh_table()

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for idx, t in enumerate(tasks, start=1):
        tag = "done" if t["status"] == "Done" else "pending"
        tree.insert("", tk.END, values=(idx, t["name"], t["status"], t["desc"]), tags=(tag,))
    # Update status bar
    total = len(tasks)
    done  = sum(1 for t in tasks if t["status"] == "Done")
    status_var.set(f"Total: {total}   Done: {done}   Pending: {total - done}")

# ── GUI ────────────────────────────────────────

load()

root = tk.Tk()
root.title("To-Do List Manager")
root.geometry("640x460")
root.resizable(False, False)

# ── Input Section ──
frame_input = tk.LabelFrame(root, text=" Add New Task ", padx=10, pady=8)
frame_input.pack(fill="x", padx=12, pady=(10, 4))

tk.Label(frame_input, text="Task Name:").grid(row=0, column=0, sticky="w", pady=3)
entry_name = tk.Entry(frame_input, width=35)
entry_name.grid(row=0, column=1, padx=8, pady=3, sticky="w")

tk.Label(frame_input, text="Description:").grid(row=1, column=0, sticky="w", pady=3)
entry_desc = tk.Entry(frame_input, width=35)
entry_desc.grid(row=1, column=1, padx=8, pady=3, sticky="w")

tk.Button(frame_input, text="＋ Add Task", bg="#28a745", fg="white",
          width=12, command=add_task).grid(row=0, column=2, rowspan=2, padx=10)

# ── Buttons ──
frame_btn = tk.Frame(root)
frame_btn.pack(fill="x", padx=12, pady=4)

tk.Button(frame_btn, text="✔ Mark as Done", bg="#007bff", fg="white",
          width=16, command=mark_done).pack(side="left", padx=4)
tk.Button(frame_btn, text="🗑 Delete Task", bg="#dc3545", fg="white",
          width=16, command=delete_task).pack(side="left", padx=4)

# ── Task Table ──
frame_table = tk.LabelFrame(root, text=" Task Records ", padx=6, pady=6)
frame_table.pack(fill="both", expand=True, padx=12, pady=4)

cols = ("#", "Task Name", "Status", "Description")
tree = ttk.Treeview(frame_table, columns=cols, show="headings", height=10)

tree.heading("#",           text="#")
tree.heading("Task Name",   text="Task Name")
tree.heading("Status",      text="Status")
tree.heading("Description", text="Description")

tree.column("#",           width=35,  anchor="center")
tree.column("Task Name",   width=140, anchor="w")
tree.column("Status",      width=80,  anchor="center")
tree.column("Description", width=330, anchor="w")

tree.tag_configure("done",    foreground="gray")
tree.tag_configure("pending", foreground="black")

scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

# ── Status Bar ──
status_var = tk.StringVar()
tk.Label(root, textvariable=status_var, anchor="w",
         relief="sunken", font=("Segoe UI", 9)).pack(fill="x", side="bottom")

refresh_table()
entry_name.focus()
root.mainloop()
