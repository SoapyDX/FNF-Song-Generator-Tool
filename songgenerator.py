import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

classic_mode = False
files_for_songs = {}

def toggle_classic_mode():
    global classic_mode
    classic_mode = not classic_mode
    if classic_mode:
        classic_mode_button.config(text="Classic Mode: ON")
    else:
        classic_mode_button.config(text="Classic Mode: OFF")

def generate_folders():
    song_list = text_box.get("1.0", "end-1c").splitlines()
    base_dirs = ["data", "songs"]
    
    if not song_list:
        messagebox.showwarning("Input Error", "Please enter at least one song name.")
        return

    for song in song_list:
        song_name = song.strip()
        if song_name:
            folder_name = song_name.replace(" ", "-") if classic_mode else song_name
            for base_dir in base_dirs:
                folder_path = os.path.join(base_dir, folder_name)
                try:
                    os.makedirs(folder_path, exist_ok=True)
                    if song_name in files_for_songs:
                        for file_path in files_for_songs[song_name]:
                            try:
                                file_name = os.path.basename(file_path)
                                destination = os.path.join(folder_path, file_name)
                                with open(file_path, "rb") as file_read, open(destination, "wb") as file_write:
                                    file_write.write(file_read.read())
                            except Exception as e:
                                messagebox.showerror("Error", f"Failed to add file '{file_name}': {e}")
                                return
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create folder: {e}")
                    return
    
    messagebox.showinfo("Success", "Folders and files generated successfully!")

def select_files_for_song():
    song_list = text_box.get("1.0", "end-1c").splitlines()
    selected_song = song_dropdown.get()
    
    if not selected_song or selected_song.strip() not in song_list:
        messagebox.showwarning("Selection Error", "Please select a valid song from the dropdown.")
        return

    selected_files = filedialog.askopenfilenames(title=f"Select Files for {selected_song}")
    
    if selected_files:
        files_for_songs[selected_song] = selected_files
        file_label.config(text=f"{len(selected_files)} file(s) selected for {selected_song}")
    else:
        file_label.config(text=f"No files selected for {selected_song}")

root = tk.Tk()
root.title("Song Folder Generator")
root.geometry("400x400")

root.state('zoomed')

label = tk.Label(root, text="Enter song names (one per line):")
label.pack(pady=10)

text_box = tk.Text(root, height=10, width=40)
text_box.pack(pady=10)

generate_button = tk.Button(root, text="Generate Folders", command=generate_folders)
generate_button.pack(pady=10)

song_dropdown_label = tk.Label(root, text="Select a song to add files:")
song_dropdown_label.pack(pady=5)

song_dropdown = tk.StringVar(root)
song_dropdown_menu = tk.OptionMenu(root, song_dropdown, "")
song_dropdown_menu.pack(pady=5)

select_button = tk.Button(root, text="Select Files for Song", command=select_files_for_song)
select_button.pack(pady=10)

file_label = tk.Label(root, text="No files selected")
file_label.pack(pady=5)

classic_mode_button = tk.Button(root, text="Classic Mode: OFF", command=toggle_classic_mode)
classic_mode_button.pack(pady=10)

def update_song_dropdown(*args):
    song_list = text_box.get("1.0", "end-1c").splitlines()
    song_dropdown_menu['menu'].delete(0, 'end')
    for song in song_list:
        song_dropdown_menu['menu'].add_command(label=song, command=tk._setit(song_dropdown, song))
    song_dropdown.set('')

text_box.bind('<KeyRelease>', update_song_dropdown)

root.mainloop()
