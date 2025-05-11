import tkinter as tk
from tkinter import messagebox
import json
import os

DATA_FILE = 'comic_reviews.json'
selected_index = None  

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def save_review():
    global selected_index
    comic_name = entry_name.get()
    rating = rating_var.get()
    comment = comment_box.get("1.0", tk.END).strip()

    if not comic_name or not comment:
        messagebox.showerror("Missing Data", "Please fill out all fields.")
        return

    review = {
        "comic_name": comic_name,
        "issue_number": 0,
        "rating": rating,
        "comment": comment
    }

    data = load_data()

    if selected_index is not None:
        # EXISTING 
        data[selected_index] = review
        selected_index = None
        messagebox.showinfo("Updated", "Review updated successfully.")
    else:
        # NEW
        data.append(review)
        messagebox.showinfo("Saved", "New review saved.")

    save_data(data)
    clear_form()

def clear_form():
    entry_name.delete(0, tk.END)
    rating_var.set(5)
    comment_box.delete("1.0", tk.END)

def view_reviews():
    top = tk.Toplevel(root)
    top.title("Edit Comic Reviews")
    top.geometry("400x300")

    listbox = tk.Listbox(top, width=50)
    listbox.pack(fill=tk.BOTH, expand=True)

    data = load_data()

    for i, review in enumerate(data):
        listbox.insert(tk.END, f"{i+1}. {review['comic_name']} ({review['rating']}/10)")

    def on_select(event):
        global selected_index
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            selected_index = index
            review = data[index]
            entry_name.delete(0, tk.END)
            entry_name.insert(0, review["comic_name"])
            rating_var.set(review["rating"])
            comment_box.delete("1.0", tk.END)
            comment_box.insert("1.0", review["comment"])
            top.destroy()

    listbox.bind("<<ListboxSelect>>", on_select)

# --- UI ---

root = tk.Tk()
root.title("Comic Book Review")
root.geometry("300x400")

tk.Label(root, text="Comic Book Name:").pack()
entry_name = tk.Entry(root, width=30)
entry_name.pack()

tk.Label(root, text="Issue Number:").pack()
entry_issue = tk.Entry(root, width=30)
entry_issue.pack()
entry_issue.insert(0, "0")  

tk.Label(root, text="Rating (1–10):").pack()
rating_var = tk.IntVar(value=5)
tk.Spinbox(root, from_=1, to=10, textvariable=rating_var).pack()

tk.Label(root, text="Comments:").pack()
comment_box = tk.Text(root, height=10, width=30)
comment_box.pack()

tk.Button(root, text="Submit / Update Review", command=save_review).pack(pady=5)
tk.Button(root, text="View / Edit Reviews", command=view_reviews).pack()

root.mainloop()
