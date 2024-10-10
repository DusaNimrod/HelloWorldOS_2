import tkinter as tk
from datetime import datetime
import platform
import os
import re

class KernelOSCLIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KernelOS CLI")  # Alkalmazás neve
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')

        # Kilépés az ESC gomb lenyomásával
        self.root.bind("<Escape>", self.exit_fullscreen)

        self.text = tk.Text(root, bg='black', fg='white', insertbackground='white', font=("Consolas", 12), state=tk.DISABLED)
        self.text.pack(fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(root, bg='black', fg='white', insertbackground='white', font=("Consolas", 12))
        self.entry.pack(fill=tk.X, side=tk.BOTTOM)
        self.entry.bind('<Return>', self.enter_command)

        self.command_history = []
        self.history_index = -1

        # Globális változók
        self.register = None
        self.global_var = None

        # Elérhető parancsok listája
        self.commands = {
            'help': self.help_command,
            'echo': self.echo_command,
            'clear': self.clear_command,
            'exit': self.exit_fullscreen,
            'date': self.date_command,
            'repeat': self.repeat_command,
            'printf': self.printf_command,
            'mov': self.mov_command,
            'int': self.int_command,
            'global': self.global_command,
            'add': self.add_command,
            'sub': self.sub_command,
            'mul': self.mul_command,
            'div': self.div_command,
            'save': self.save_command,
            'load': self.load_command,
            'sysinfo': self.sysinfo_command,
            'qed': self.qed_command,
        }

        self.show_welcome_message()

    def show_welcome_message(self):
        self.text.config(state=tk.NORMAL)
        welcome_message = "KernelOS CLI - Type 'help' for available commands.\n"
        self.text.insert(tk.END, welcome_message)
        self.text.config(state=tk.DISABLED)

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)
        self.root.quit()

    def enter_command(self, event):
        command = self.entry.get().strip()
        self.entry.delete(0, tk.END)  # Töröljük a beviteli mezőt

        if command:
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            self.process_command(command)
            self.text.see(tk.END)

        return "break"

    def process_command(self, command):
        parts = command.split()
        cmd_name = parts[0].lower()  # Kisbetűssé alakítás
        args = parts[1:]

        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, f"\n> {command}\n")  # Megjelenítjük a beírt parancsot

        if cmd_name in self.commands:
            self.commands[cmd_name](args)
        else:
            self.text.insert(tk.END, f"Unknown command: {cmd_name}\n")
        
        self.text.config(state=tk.DISABLED)

    def help_command(self, args):
        help_text = "\nAvailable commands:\n"
        help_text += "  help    - Show this help message\n"
        help_text += "  echo    - Echo the input text\n"
        help_text += "  clear   - Clear the terminal\n"
        help_text += "  exit    - Exit the terminal\n"
        help_text += "  date    - Show current date and time\n"
        help_text += "  repeat  - Repeat the given text a specified number of times\n"
        help_text += "  printf  - Print formatted text (e.g., printf %s Hello)\n"
        help_text += "  mov     - Move a value to a register (e.g., mov eax, 10)\n"
        help_text += "  int     - Simulate an interrupt (e.g., int 21h)\n"
        help_text += "  global  - Set a global variable (e.g., global var_name value)\n"
        help_text += "  add     - Add two numbers (e.g., add 5 3)\n"
        help_text += "  sub     - Subtract two numbers (e.g., sub 5 3)\n"
        help_text += "  mul     - Multiply two numbers (e.g., mul 5 3)\n"
        help_text += "  div     - Divide two numbers (e.g., div 6 2)\n"
        help_text += "  save    - Save text to a file (e.g., save filename.txt text)\n"
        help_text += "  load    - Load and display file content (e.g., load filename.txt)\n"
        help_text += "  sysinfo - Display system information\n"
        help_text += "  qed     - Open a fullscreen editor with syntax highlighting\n"
        self.text.insert(tk.END, help_text + "\n")

    def echo_command(self, args):
        echo_text = " ".join(args)
        self.text.insert(tk.END, f"{echo_text}\n")

    def clear_command(self, args):
        self.text.config(state=tk.NORMAL)
        self.text.delete('1.0', tk.END)
        self.show_welcome_message()
        self.text.config(state=tk.DISABLED)

    def date_command(self, args):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.text.insert(tk.END, f"{current_time}\n")

    def repeat_command(self, args):
        if len(args) < 2:
            self.text.insert(tk.END, "Usage: repeat <number> <text>\n")
            return

        try:
            count = int(args[0])
            if count < 0:
                self.text.insert(tk.END, "The number must be non-negative.\n")
                return

            text = " ".join(args[1:])
            max_count = 1000
            if count > max_count:
                self.text.insert(tk.END, f"Limiting repeat count to {max_count}.\n")
                count = max_count

            self.text.insert(tk.END, f"\nRepeating text...\n")
            self.root.update()

            for _ in range(count):
                self.text.insert(tk.END, f"{text}\n")
                self.root.update()

        except ValueError:
            self.text.insert(tk.END, "Invalid number.\n")

    def printf_command(self, args):
        if len(args) < 2 or args[0] != '%s':
            self.text.insert(tk.END, "Usage: printf %s <text>\n")
        else:
            text = " ".join(args[1:])
            self.text.insert(tk.END, f"{text}\n")

    def mov_command(self, args):
        if len(args) != 2:
            self.text.insert(tk.END, "Usage: mov <register>, <value>\n")
        else:
            reg = args[0].lower()
            value = args[1]
            self.register = value
            self.text.insert(tk.END, f"Moved {value} to {reg}\n")

    def int_command(self, args):
        if len(args) != 1:
            self.text.insert(tk.END, "Usage: int <interrupt_number>\n")
        else:
            interrupt_number = args[0]
            if interrupt_number == "21h":
                self.text.insert(tk.END, "Interrupt 21h: DOS interrupt simulated.\n")
            else:
                self.text.insert(tk.END, f"Interrupt {interrupt_number} not supported.\n")

    def global_command(self, args):
        if len(args) != 2:
            self.text.insert(tk.END, "Usage: global <var_name> <value>\n")
        else:
            var_name = args[0]
            value = args[1]
            self.global_var = {var_name: value}
            self.text.insert(tk.END, f"Global variable {var_name} set to {value}\n")

    def add_command(self, args):
        if len(args) != 2:
            self.text.insert(tk.END, "Usage: add <num1> <num2>\n")
        else:
            try:
                num1 = float(args[0])
                num2 = float(args[1])
                result = num1 + num2
                self.text.insert(tk.END, f"Result: {result}\n")
            except ValueError:
                self.text.insert(tk.END, "Invalid numbers.\n")

    def sub_command(self, args):
        if len(args) != 2:
            self.text.insert(tk.END, "Usage: sub <num1> <num2>\n")
        else:
            try:
                num1 = float(args[0])
                num2 = float(args[1])
                result = num1 - num2
                self.text.insert(tk.END, f"Result: {result}\n")
            except ValueError:
                self.text.insert(tk.END, "Invalid numbers.\n")

    def mul_command(self, args):
        if len(args) != 2:
            self.text.insert(tk.END, "Usage: mul <num1> <num2>\n")
        else:
            try:
                num1 = float(args[0])
                num2 = float(args[1])
                result = num1 * num2
                self.text.insert(tk.END, f"Result: {result}\n")
            except ValueError:
                self.text.insert(tk.END, "Invalid numbers.\n")

    def div_command(self, args):
        if len(args) != 2:
            self.text.insert(tk.END, "Usage: div <num1> <num2>\n")
        else:
            try:
                num1 = float(args[0])
                num2 = float(args[1])
                if num2 == 0:
                    self.text.insert(tk.END, "Cannot divide by zero.\n")
                else:
                    result = num1 / num2
                    self.text.insert(tk.END, f"Result: {result}\n")
            except ValueError:
                self.text.insert(tk.END, "Invalid numbers.\n")

    def save_command(self, args):
        if len(args) < 2:
            self.text.insert(tk.END, "Usage: save <filename> <text>\n")
        else:
            filename = args[0]
            content = " ".join(args[1:])
            try:
                with open(filename, 'w') as f:
                    f.write(content)
                self.text.insert(tk.END, f"Saved to {filename}\n")
            except Exception as e:
                self.text.insert(tk.END, f"Error saving file: {e}\n")

    def load_command(self, args):
        if len(args) != 1:
            self.text.insert(tk.END, "Usage: load <filename>\n")
        else:
            filename = args[0]
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                self.text.insert(tk.END, f"{content}\n")
            except Exception as e:
                self.text.insert(tk.END, f"Error loading file: {e}\n")

    def sysinfo_command(self, args):
        sysinfo_text = (
            "Running in: Python 3.12.5\n"
            "System: KernelOS CLI\n"
            "Version: 1.0\n"
            "Open source\n"
        )
        self.text.insert(tk.END, f"{sysinfo_text}\n")

    def qed_command(self, args):
        # Create a new window for the QED editor
        qed_window = tk.Toplevel(self.root)
        qed_window.title("QED Editor")
        qed_window.attributes('-fullscreen', True)
        qed_window.configure(bg='black')

        # Text widget for QED editor with syntax highlighting
        qed_text = tk.Text(qed_window, bg='black', fg='white', insertbackground='white', font=("Consolas", 12), selectbackground='gray')
        qed_text.pack(fill=tk.BOTH, expand=True)

        # Add syntax highlighting
        qed_text.tag_configure("text", foreground="green")
        qed_text.tag_configure("number", foreground="blue")
        qed_text.tag_configure("paren", foreground="yellow")
        qed_text.tag_configure("angle", foreground="brown")
        qed_text.tag_configure("dollar", foreground="purple")

        # Set block cursor
        qed_text.config(insertbackground='white')  # White block cursor

        def on_key_release(event):
            self.highlight_syntax(qed_text)

        qed_text.bind('<KeyRelease>', on_key_release)
        
        # Close button
        close_button = tk.Button(qed_window, text="Close", command=qed_window.destroy, bg='black', fg='white', font=("Consolas", 12))
        close_button.pack(side=tk.BOTTOM, fill=tk.X)

        # Initial highlighting
        self.highlight_syntax(qed_text)

    def highlight_syntax(self, text_widget):
        # Remove all existing tags
        text_widget.tag_remove("text", "1.0", tk.END)
        text_widget.tag_remove("number", "1.0", tk.END)
        text_widget.tag_remove("paren", "1.0", tk.END)
        text_widget.tag_remove("angle", "1.0", tk.END)
        text_widget.tag_remove("dollar", "1.0", tk.END)

        content = text_widget.get("1.0", tk.END)
        
        # Regular expressions for syntax highlighting
        patterns = {
            "text": r'[a-zA-Z_][a-zA-Z0-9_]*',  # Text
            "number": r'\b\d+(\.\d+)?\b',       # Numbers
            "paren": r'[(){}[\]]',               # Parentheses
            "angle": r'<[^>]*>',                 # Angle brackets
            "dollar": r'\$\w+'                   # Dollar sign
        }

        for tag, pattern in patterns.items():
            for match in re.finditer(pattern, content):
                start, end = match.span()
                text_widget.tag_add(tag, f"1.0 + {start}c", f"1.0 + {end}c")

if __name__ == "__main__":
    root = tk.Tk()
    app = KernelOSCLIApp(root)
    root.mainloop()
