import tkinter as tk
from tkinter import ttk
import psutil
import pygame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 🔊 Sound setup
pygame.mixer.init()
def play_alert():
    pygame.mixer.music.load("alert.mp3")  # Replace with your own short alert sound
    pygame.mixer.music.play()

# 🌗 Theme toggle
def toggle_theme():
    current = root.cget("bg")
    new_bg = "#ffffff" if current == "#1e1e1e" else "#1e1e1e"
    new_fg = "black" if new_bg == "#ffffff" else "lime"
    root.configure(bg=new_bg)
    for widget in [cpu_label, mem_label, apps_label, theme_btn]:
        widget.configure(bg=new_bg, fg=new_fg)

# 🖼️ Create main window FIRST
root = tk.Tk()
root.title("Advanced System Monitor")
root.geometry("600x400")
root.configure(bg="#1e1e1e")

# 📊 Graph setup
fig, ax = plt.subplots(figsize=(4, 2))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

cpu_history = []

def update_stats():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    running_apps = [p.name() for p in psutil.process_iter()]
    
    cpu_label.config(text=f"CPU Usage: {cpu}%")
    mem_label.config(text=f"Memory Usage: {memory}%")
    apps_label.config(text=f"Apps: {', '.join(running_apps[:5])}...")

    if cpu > 80:
        play_alert()

    cpu_history.append(cpu)
    if len(cpu_history) > 30:
        cpu_history.pop(0)
    ax.clear()
    ax.plot(cpu_history, color="lime")
    ax.set_title("CPU Usage Over Time")
    ax.set_ylim(0, 100)
    canvas.draw()

    root.after(3000, update_stats)

# 🧱 UI Elements
cpu_label = tk.Label(root, font=("Arial", 14), fg="lime", bg="#1e1e1e")
mem_label = tk.Label(root, font=("Arial", 14), fg="cyan", bg="#1e1e1e")
apps_label = tk.Label(root, font=("Arial", 10), fg="orange", bg="#1e1e1e", wraplength=580)
theme_btn = tk.Button(root, text="Toggle Theme", command=toggle_theme)

cpu_label.pack(pady=5)
mem_label.pack(pady=5)
apps_label.pack(pady=5)
theme_btn.pack(pady=10)

update_stats()
root.mainloop()