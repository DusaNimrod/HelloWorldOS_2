import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
from cmd_prompt import KernelOSCLIApp  # Import the command prompt GUI
from KernelOS_info import KernelOSInfoApp  # Import the info app
from calculator import Calculator  # Import the Calculator app
import time
import os

# Create the main OS window
class KernelOS(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KernelOS")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.configure(bg="skyblue")  # Set the background color to skyblue

        # Make the window fullscreen
        self.attributes('-fullscreen', True)

        # Add a menubar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        app_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Apps", menu=app_menu)
        app_menu.add_command(label="Command Prompt", command=self.open_command_prompt)
        app_menu.add_command(label="Info", command=self.open_info)  # Add Info option
        app_menu.add_command(label="Calculator", command=self.open_calculator)  # Add Calculator option
        app_menu.add_separator()
        app_menu.add_command(label="Exit", command=self.quit_os)  # Exit option

        # Create a menu for shutdown and reload
        shutdown_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="System", menu=shutdown_menu)
        shutdown_menu.add_command(label="Shutdown", command=self.quit_os)  # Shutdown option
        shutdown_menu.add_command(label="Reload", command=self.reload_os)  # Reload option
        shutdown_menu.add_command(label="New Session", command=self.open_new_session)  # New Session option
        shutdown_menu.add_command(label="+", command=self.open_file_manager)  # File manager option

        # Create a frame for the buttons
        self.button_frame = tk.Frame(self, bg="skyblue")
        self.button_frame.pack(side='left', fill='y', padx=10, pady=10)

        # Create smaller buttons for each app
        command_prompt_button = tk.Button(self.button_frame, text="Command Prompt", width=8, height=2,
                                           command=self.open_command_prompt)
        command_prompt_button.pack(pady=10)

        info_button = tk.Button(self.button_frame, text="Info", width=8, height=2,
                                command=self.open_info)  # Info button
        info_button.pack(pady=10)

        calculator_button = tk.Button(self.button_frame, text="Calculator", width=8, height=2,
                                      command=self.open_calculator)  # Calculator button
        calculator_button.pack(pady=10)

        # Add a desktop label
        desktop_label = tk.Label(self, text="Desktop", font=("Arial", 24), bg="skyblue")
        desktop_label.pack(pady=100)

        # Create a taskbar at the bottom
        self.taskbar_frame = tk.Frame(self, bg="gray", height=40)
        self.taskbar_frame.pack(side='bottom', fill='x')

        # Add the "Start" button to the taskbar
        start_button = tk.Button(self.taskbar_frame, text="Start", command=self.open_start_menu)
        start_button.pack(side='left', padx=5)

        # Add buttons to the taskbar
        taskbar_command_prompt_button = tk.Button(self.taskbar_frame, text="Command Prompt", command=self.open_command_prompt)
        taskbar_command_prompt_button.pack(side='left', padx=5)

        taskbar_info_button = tk.Button(self.taskbar_frame, text="Info", command=self.open_info)  # Taskbar Info button
        taskbar_info_button.pack(side='left', padx=5)

        taskbar_calculator_button = tk.Button(self.taskbar_frame, text="Calculator", command=self.open_calculator)  # Taskbar Calculator button
        taskbar_calculator_button.pack(side='left', padx=5)

        # Time display in the taskbar
        self.time_label = tk.Label(self.taskbar_frame, bg="gray", fg="white")
        self.time_label.pack(side='right', padx=10)

        self.update_time()

    def open_start_menu(self):
        # Create a new window for the Start menu
        start_menu = tk.Toplevel(self)
        start_menu.title("Start Menu")
        start_menu.geometry("150x200")  # Size of the start menu window
        
        # Make sure the window stays on top
        start_menu.wm_attributes("-topmost", 1)

        # Add buttons to the start menu
        tk.Button(start_menu, text="Command Prompt", command=self.open_command_prompt).pack(pady=5)
        tk.Button(start_menu, text="Info", command=self.open_info).pack(pady=5)
        tk.Button(start_menu, text="Calculator", command=self.open_calculator).pack(pady=5)
        tk.Button(start_menu, text="Exit", command=self.quit_os).pack(pady=5)

    def open_command_prompt(self):
        # Open the Command Prompt in a new window (detached)
        new_window = tk.Toplevel(self)
        new_window.title("Command Prompt")
        new_window.geometry("800x600")  # You can adjust the size as needed
        
        # Make sure the window stays on top
        new_window.wm_attributes("-topmost", 1)

        # Create the command prompt app from cmd_prompt.py in the new window
        KernelOSCLIApp(new_window)

    def open_info(self):
        # Open the Info application in a new window (detached)
        new_window = tk.Toplevel(self)
        new_window.title("KernelOS Info")
        new_window.geometry("600x400")  # Adjust the size as needed
        
        # Make sure the window stays on top
        new_window.wm_attributes("-topmost", 1)

        # Create the info app from KernelOS_info.py in the new window
        KernelOSInfoApp(new_window)

    def open_calculator(self):
        # Open the Calculator in a new window (detached)
        new_window = tk.Toplevel(self)
        new_window.title("Calculator")
        new_window.geometry("400x500")  # Adjust the size as needed
        
        # Make sure the window stays on top
        new_window.wm_attributes("-topmost", 1)

        # Create the Calculator app from calculator.py in the new window
        Calculator(new_window)

    def open_file_manager(self):
        # Open a file dialog to select a Python file
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py;*.pyw")])
        if file_path:
            # Add a button on the desktop to run the selected file
            self.add_app_button(file_path)

    def add_app_button(self, file_path):
        # Get the file name without the extension
        file_name = os.path.basename(file_path)
        file_button = tk.Button(self.button_frame, text=file_name, width=8, height=2,
                                command=lambda: self.run_script(file_path))
        file_button.pack(pady=10)

    def run_script(self, file_path):
        # Create a new top-level window for the script
        script_window = tk.Toplevel(self)
        script_window.title(os.path.basename(file_path))
        script_window.geometry("800x600")  # Adjust as needed
        
        # Make sure the window stays on top
        script_window.wm_attributes("-topmost", 1)

        # Run the selected Python script
        try:
            subprocess.Popen(["python", file_path], shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run the script:\n{str(e)}")

    def quit_os(self):
        self.destroy()

    def reload_os(self):
        # Reload the application (close and reopen)
        self.quit_os()
        self.__init__()  # Re-initialize the KernelOS class to reload it

    def open_new_session(self):
        # Create a new session window for KernelOS
        new_session = tk.Toplevel(self)
        new_session.title("New KernelOS Session")
        new_session.geometry("800x600")  # Set the size of the new session
        new_session.wm_attributes("-topmost", 1)  # Keep it on top

        # Initialize KernelOS inside the new session window
        new_os = KernelOS()
        new_os.wm_attributes("-fullscreen", False)  # Disable fullscreen in the new session

    def update_time(self):
        # Update the time display on the taskbar
        current_time = time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)  # Refresh every second

if __name__ == "__main__":
    app = KernelOS()
    app.mainloop()
