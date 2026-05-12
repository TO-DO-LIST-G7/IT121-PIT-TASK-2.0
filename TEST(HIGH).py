import tkinter as tk
from tkinter import ttk, messagebox
import os

# ─────────────────────────────────────────────
#  FILE HANDLING
# ─────────────────────────────────────────────
FILE_NAME = "tasks.txt"

def load_tasks():
    """Read all tasks from the text file."""
    tasks = []
    try:
        if not os.path.exists(FILE_NAME):
            return tasks                    # file doesn't exist yet → empty list
        with open(FILE_NAME, "r") as f:
            for line in f:
                line = line.strip()
                if line:                    # skip blank lines
                    parts = line.split("|", 2)   # name | status | description
                    if len(parts) == 3:
                        tasks.append({
                            "name":        parts[0],
                            "status":      parts[1],
                            "description": parts[2]
                        })
    except Exception as e:
        messagebox.showerror("File Error", f"Could not read tasks:\n{e}")
    return tasks


def save_tasks(tasks):
    """Overwrite the text file with the current task list (update)."""
    try:
        with open(FILE_NAME, "w") as f:
            for t in tasks:
                f.write(f"{t['name']}|{t['status']}|{t['description']}\n")
    except Exception as e:
        messagebox.showerror("File Error", f"Could not save tasks:\n{e}")


def append_task(task):
    """Append a single new task to the text file."""
    try:
        with open(FILE_NAME, "a") as f:
            f.write(f"{task['name']}|{task['status']}|{task['description']}\n")
    except Exception as e:
        messagebox.showerror("File Error", f"Could not append task:\n{e}")


# ─────────────────────────────────────────────
#  TASK LOGIC
# ─────────────────────────────────────────────
tasks = load_tasks()   # global in-memory task list


def add_task():
    """Validate inputs, create a task, append to file, refresh table."""
    name = entry_name.get().strip()
    desc = entry_desc.get().strip()

    # Validation
    if not name:
        messagebox.showwarning("Validation", "Task name cannot be empty.")
        return
    if not desc:
        messagebox.showwarning("Validation", "Task description cannot be empty.")
        return

    new_task = {"name": name, "status": "Pending", "description": desc}
    tasks.append(new_task)
    append_task(new_task)            # file: append only
    refresh_table()
    entry_name.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    messagebox.showinfo("Success", f'Task "{name}" added!')


def mark_completed():
    """Mark the selected task as Completed and update the file."""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection", "Please select a task first.")
        return

    index = tree.index(selected[0])
    if tasks[index]["status"] == "Completed":
        messagebox.showinfo("Info", "Task is already completed.")
        return

    tasks[index]["status"] = "Completed"
    save_tasks(tasks)                # file: full rewrite (update)
    refresh_table()
    messagebox.showinfo("Success", f'Task "{tasks[index]["name"]}" marked as Completed!')


def delete_task():
    """Delete the selected task from memory and the file."""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection", "Please select a task to delete.")
        return

    index = tree.index(selected[0])
    task_name = tasks[index]["name"]
    confirm = messagebox.askyesno("Confirm Delete", f'Delete task "{task_name}"?')
    if confirm:
        tasks.pop(index)
        save_tasks(tasks)            # file: full rewrite (update)
        refresh_table()
        messagebox.showinfo("Deleted", f'Task "{task_name}" deleted.')


def refresh_table():
    """Clear the Treeview and re-populate it from the in-memory list."""
    for row in tree.get_children():
        tree.delete(row)

    for i, t in enumerate(tasks, start=1):
        tag = "done" if t["status"] == "Completed" else "pending"
        tree.insert("", tk.END,
                    values=(i, t["name"], t["status"], t["description"]),
                    tags=(tag,))


# ─────────────────────────────────────────────
#  GUI SETUP
# ─────────────────────────────────────────────
root = tk.Tk()
root.title("📝  Daily Task Manager")
root.geometry("820x560")
root.resizable(False, False)
root.configure(bg="#1e1e2e")

# ── Colours ──────────────────────────────────
BG       = "#1e1e2e"
PANEL    = "#2a2a3d"
ACCENT   = "#7c6af7"
SUCCESS  = "#50fa7b"
DANGER   = "#ff5555"
FG       = "#cdd6f4"
FG_DIM   = "#6c7086"
ENTRY_BG = "#313244"

# ── Fonts ─────────────────────────────────────
FONT_TITLE  = ("Segoe UI", 18, "bold")
FONT_LABEL  = ("Segoe UI", 10)
FONT_BTN    = ("Segoe UI", 10, "bold")
FONT_TABLE  = ("Segoe UI", 10)

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
header = tk.Frame(root, bg=ACCENT, pady=12)
header.pack(fill="x")
tk.Label(header, text="📝  Daily Task Manager",
         font=FONT_TITLE, bg=ACCENT, fg="white").pack()
tk.Label(header, text="PIT Project – File-Based GUI To-Do System",
         font=("Segoe UI", 9), bg=ACCENT, fg="#e0d9ff").pack()

# ─────────────────────────────────────────────
#  INPUT PANEL
# ─────────────────────────────────────────────
input_frame = tk.Frame(root, bg=PANEL, padx=20, pady=14)
input_frame.pack(fill="x", padx=10, pady=(10, 0))

# Row 0 – Task Name
tk.Label(input_frame, text="Task Name:", font=FONT_LABEL,
         bg=PANEL, fg=FG).grid(row=0, column=0, sticky="w", pady=4)
entry_name = tk.Entry(input_frame, font=FONT_LABEL, width=38,
                      bg=ENTRY_BG, fg=FG, insertbackground=FG,
                      relief="flat", bd=6)
entry_name.grid(row=0, column=1, padx=(8, 20), pady=4, sticky="w")

# Row 1 – Description
tk.Label(input_frame, text="Description:", font=FONT_LABEL,
         bg=PANEL, fg=FG).grid(row=1, column=0, sticky="w", pady=4)
entry_desc = tk.Entry(input_frame, font=FONT_LABEL, width=38,
                      bg=ENTRY_BG, fg=FG, insertbackground=FG,
                      relief="flat", bd=6)
entry_desc.grid(row=1, column=1, padx=(8, 20), pady=4, sticky="w")

# Add Button
btn_add = tk.Button(input_frame, text="＋  Add Task",
                    font=FONT_BTN, bg=ACCENT, fg="white",
                    activebackground="#6a5ae0", activeforeground="white",
                    relief="flat", padx=14, pady=6, cursor="hand2",
                    command=add_task)
btn_add.grid(row=0, column=2, rowspan=2, padx=4)

# ─────────────────────────────────────────────
#  ACTION BUTTONS
# ─────────────────────────────────────────────
btn_frame = tk.Frame(root, bg=BG, pady=8)
btn_frame.pack(fill="x", padx=10)

btn_complete = tk.Button(btn_frame, text="✔  Mark Completed",
                         font=FONT_BTN, bg=SUCCESS, fg="#1e1e2e",
                         activebackground="#3dd164", relief="flat",
                         padx=16, pady=7, cursor="hand2",
                         command=mark_completed)
btn_complete.pack(side="left", padx=6)

btn_delete = tk.Button(btn_frame, text="🗑  Delete Task",
                       font=FONT_BTN, bg=DANGER, fg="white",
                       activebackground="#cc4444", relief="flat",
                       padx=16, pady=7, cursor="hand2",
                       command=delete_task)
btn_delete.pack(side="left", padx=6)

# Task count label (right-aligned)
count_var = tk.StringVar()
lbl_count = tk.Label(btn_frame, textvariable=count_var,
                     font=("Segoe UI", 9), bg=BG, fg=FG_DIM)
lbl_count.pack(side="right", padx=12)

# ─────────────────────────────────────────────
#  TASK TABLE  (Treeview)
# ─────────────────────────────────────────────
table_frame = tk.Frame(root, bg=BG)
table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background=PANEL, foreground=FG,
                fieldbackground=PANEL, rowheight=28,
                font=FONT_TABLE)
style.configure("Treeview.Heading",
                background=ACCENT, foreground="white",
                font=("Segoe UI", 10, "bold"), relief="flat")
style.map("Treeview",
          background=[("selected", ACCENT)],
          foreground=[("selected", "white")])

columns = ("#", "Task Name", "Status", "Description")
tree = ttk.Treeview(table_frame, columns=columns,
                    show="headings", selectmode="browse")

for col in columns:
    tree.heading(col, text=col)

tree.column("#",           width=40,  anchor="center")
tree.column("Task Name",   width=180, anchor="w")
tree.column("Status",      width=110, anchor="center")
tree.column("Description", width=430, anchor="w")

# Row colour tags
tree.tag_configure("done",    foreground=SUCCESS)
tree.tag_configure("pending", foreground=FG)

# Scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient="vertical",
                           command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
footer = tk.Frame(root, bg=PANEL, pady=5)
footer.pack(fill="x", side="bottom")
tk.Label(footer,
         text=f"Tasks saved in: {os.path.abspath(FILE_NAME)}",
         font=("Segoe UI", 8), bg=PANEL, fg=FG_DIM).pack()

# ─────────────────────────────────────────────
#  PATCH refresh_table to also update count
# ─────────────────────────────────────────────
_orig_refresh = refresh_table

def refresh_table():
    _orig_refresh()
    total     = len(tasks)
    completed = sum(1 for t in tasks if t["status"] == "Completed")
    count_var.set(f"Total: {total}  |  Completed: {completed}  |  Pending: {total - completed}")

# Initial load
refresh_table()

root.mainloop()