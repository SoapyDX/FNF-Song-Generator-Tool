import os
import tkinter as tk
from tkinter import messagebox

def generate_folders():
    song_list = text_box.get("1.0", "end-1c").splitlines()
    base_dirs = ["data", "songs"]
    
    if not song_list:
        messagebox.showwarning("Input Error", "Please enter at least one song name.")
        return
    
    for song in song_list:
        if song.strip():
            for base_dir in base_dirs:
                folder_path = os.path.join(base_dir, song.strip())
                try:
                    os.makedirs(folder_path, exist_ok=True)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create folder: {e}")
                    return
    
    messagebox.showinfo("Success", "Folders generated successfully!")

root = tk.Tk()
root.title("Song Folder Generator")
root.geometry("400x300")

label = tk.Label(root, text="Enter song names (one per line):")
label.pack(pady=10)

text_box = tk.Text(root, height=10, width=40)
text_box.pack(pady=10)

generate_button = tk.Button(root, text="Generate Folders", command=generate_folders)
generate_button.pack(pady=10)

root.mainloop()
