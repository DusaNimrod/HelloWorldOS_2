import tkinter as tk

class KernelOSInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KernelOS information")
        
        # Create a label to display the information
        info_text = (
            "Name: KernelOS Professional Edition\n"
            "Built with: Python 3.12.5\n"
            "GUI: Tkinter\n"
            "Edition: Professional\n"
            "Open Source"
        )
        
        self.label = tk.Label(root, text=info_text, font=("Arial", 12), padx=20, pady=20)
        self.label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = KernelOSInfoApp(root)
    root.mainloop()
