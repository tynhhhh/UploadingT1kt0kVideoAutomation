import tkinter as tk
from tkinter import filedialog, scrolledtext
from MobileControl import *


def detect_devices():
    # Replace this with actual device detection logic
    connected_devices = GetDevices()
    devices_text.config(state=tk.NORMAL)  # Enable editing temporarily
    devices_text.delete(1.0, tk.END)
    for device in connected_devices:
        devices_text.insert(tk.END, device + '\n')
    devices_text.config(state=tk.DISABLED)  # Disable editing again

def perform_function():
    for m in range(1):
        threading.Thread(target=main, args=(m,)).start()

# Create the main application window
app = tk.Tk()
app.title("Basic App")


# Connected devices label (scrollable)
devices_label = tk.Label(app, text="Connected devices:")
devices_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
devices_text = scrolledtext.ScrolledText(app, width=30, height=5, state=tk.DISABLED)  # Read-only
devices_text.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="we")

# Detect devices button
detect_button = tk.Button(app, text="Detect Devices", command=detect_devices)
detect_button.grid(row=2, column=0, padx=5, pady=5, sticky="we")

# Perform function button
function_button = tk.Button(app, text="Perform Function", command=perform_function)
function_button.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="we")

# Start the Tkinter event loop
app.mainloop()
