import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
from cracker import ArchiveCracker
import string

class ArchiveCrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Weakness - Archive Password Cracker")
        self.root.geometry("700x600")
        self.root.configure(bg="#2b2b2b")
        
        self.cracker = None
        self.cracking_thread = None
        self.is_cracking = False
        
        self.setup_styles()
        self.create_widgets()
    
    def setup_styles(self):
        """Setup custom styles for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background="#2b2b2b", foreground="#ffffff")
        style.configure('TButton', background="#0d47a1", foreground="#ffffff")
        style.configure('TFrame', background="#2b2b2b")
        style.configure('TEntry', fieldbackground="#1e1e1e", foreground="#ffffff")
        style.configure('TCombobox', fieldbackground="#1e1e1e", foreground="#ffffff")
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title
        title_label = ttk.Label(self.root, text="Archive Password Cracker", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Frame for file selection
        file_frame = ttk.LabelFrame(self.root, text="Archive Selection", padding=10)
        file_frame.pack(pady=10, padx=10, fill="x")
        
        ttk.Label(file_frame, text="Archive File:").grid(row=0, column=0, sticky="w")
        self.file_path_var = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=40)
        self.file_entry.grid(row=0, column=1, padx=5)
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.grid(row=0, column=2)
        
        # Frame for method selection
        method_frame = ttk.LabelFrame(self.root, text="Attack Method", padding=10)
        method_frame.pack(pady=10, padx=10, fill="x")
        
        ttk.Label(method_frame, text="Method:").grid(row=0, column=0, sticky="w")
        self.method_var = tk.StringVar(value="dictionary")
        method_combo = ttk.Combobox(method_frame, textvariable=self.method_var, 
                                    values=["dictionary", "brute_force"], state="readonly", width=30)
        method_combo.grid(row=0, column=1, padx=5)
        method_combo.bind("<<ComboboxSelected>>", self.on_method_changed)
        
        # Frame for dictionary/charset options
        options_frame = ttk.LabelFrame(self.root, text="Options", padding=10)
        options_frame.pack(pady=10, padx=10, fill="x")
        
        # Dictionary path
        ttk.Label(options_frame, text="Wordlist File:").grid(row=0, column=0, sticky="w")
        self.wordlist_var = tk.StringVar()
        self.wordlist_entry = ttk.Entry(options_frame, textvariable=self.wordlist_var, width=40)
        self.wordlist_entry.grid(row=0, column=1, padx=5)
        
        self.browse_wordlist_btn = ttk.Button(options_frame, text="Browse", command=self.browse_wordlist)
        self.browse_wordlist_btn.grid(row=0, column=2)
        
        # Charset options
        ttk.Label(options_frame, text="Character Set:").grid(row=1, column=0, sticky="w")
        self.charset_var = tk.StringVar(value="letters+digits")
        
        # Max length for brute force
        ttk.Label(options_frame, text="Max Length:").grid(row=2, column=0, sticky="w")
        self.max_length_var = tk.StringVar(value="6")
        ttk.Spinbox(options_frame, from_=1, to=10, textvariable=self.max_length_var, width=10).grid(row=2, column=1, sticky="w", padx=5)
        
        # Progress section
        progress_frame = ttk.LabelFrame(self.root, text="Progress", padding=10)
        progress_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill="x", pady=5)
        
        # Status text
        ttk.Label(progress_frame, text="Status:").pack(anchor="w")
        self.status_text = tk.Text(progress_frame, height=8, width=70, bg="#1e1e1e", fg="#00ff00")
        self.status_text.pack(fill="both", expand=True, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.start_btn = ttk.Button(button_frame, text="Start Cracking", command=self.start_cracking)
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="Stop", command=self.stop_cracking, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="Clear Log", command=self.clear_log)
        self.clear_btn.pack(side="left", padx=5)
    
    def browse_file(self):
        """Browse for archive file"""
        filetypes = [("All Archives", "*.zip *.rar *.pdf"), 
                     ("ZIP files", "*.zip"), 
                     ("RAR files", "*.rar"), 
                     ("PDF files", "*.pdf")]
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        if file_path:
            self.file_path_var.set(file_path)
    
    def browse_wordlist(self):
        """Browse for wordlist file"""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.wordlist_var.set(file_path)
    
    def on_method_changed(self, event=None):
        """Handle method change"""
        method = self.method_var.get()
        if method == "dictionary":
            self.wordlist_entry.config(state="normal")
            self.browse_wordlist_btn.config(state="normal")
        else:
            self.wordlist_entry.config(state="disabled")
            self.browse_wordlist_btn.config(state="disabled")
    
    def log_message(self, message):
        """Add message to the log"""
        self.status_text.insert("end", message + "\n")
        self.status_text.see("end")
        self.root.update()
    
    def clear_log(self):
        """Clear the log"""
        self.status_text.delete("1.0", "end")
    
    def start_cracking(self):
        """Start the cracking process"""
        archive_path = self.file_path_var.get()
        
        if not archive_path or not os.path.exists(archive_path):
            messagebox.showerror("Error", "Please select a valid archive file")
            return
        
        self.is_cracking = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.progress_bar.start()
        
        self.log_message(f"Starting attack on: {archive_path}")
        self.log_message(f"Method: {self.method_var.get()}")
        self.log_message("=" * 60)
        
        # Create cracker instance
        self.cracker = ArchiveCracker(archive_path)
        
        # Start cracking in a separate thread
        method = self.method_var.get()
        if method == "dictionary":
            wordlist_path = self.wordlist_var.get()
            if not wordlist_path or not os.path.exists(wordlist_path):
                messagebox.showerror("Error", "Please select a valid wordlist file")
                self.is_cracking = False
                self.start_btn.config(state="normal")
                self.stop_btn.config(state="disabled")
                self.progress_bar.stop()
                return
            
            self.cracking_thread = threading.Thread(target=self._dictionary_attack, args=(wordlist_path,))
        else:
            self.cracking_thread = threading.Thread(target=self._brute_force_attack)
        
        self.cracking_thread.daemon = True
        self.cracking_thread.start()
    
    def _dictionary_attack(self, wordlist_path):
        """Dictionary attack in separate thread"""
        def callback(status, data, attempts, elapsed=0):
            if status == 'found':
                self.log_message(f"✓ PASSWORD FOUND: {data}")
                self.log_message(f"Attempts: {attempts}")
                self.log_message(f"Time: {elapsed:.2f} seconds")
            elif status == 'progress':
                if attempts % 1000 == 0:
                    self.log_message(f"Attempts: {attempts} | Last tried: {data}")
        
        result = self.cracker.dictionary_attack(wordlist_path, callback=callback)
        
        if result:
            self.log_message(f"\n✓ SUCCESS! Password: {result}")
        else:
            self.log_message("\n✗ Password not found in wordlist")
        
        self.finish_cracking()
    
    def _brute_force_attack(self):
        """Brute force attack in separate thread"""
        max_length = int(self.max_length_var.get())
        charset = string.ascii_letters + string.digits + string.punctuation
        
        def callback(status, data, attempts, elapsed=0):
            if status == 'found':
                self.log_message(f"✓ PASSWORD FOUND: {data}")
                self.log_message(f"Attempts: {attempts}")
                self.log_message(f"Time: {elapsed:.2f} seconds")
            elif status == 'progress':
                if attempts % 1000 == 0:
                    speed = attempts / elapsed if elapsed > 0 else 0
                    self.log_message(f"Attempts: {attempts} | Speed: {speed:.0f} p/s | Last: {data}")
        
        result = self.cracker.brute_force(charset=charset, max_length=max_length, callback=callback)
        
        if result:
            self.log_message(f"\n✓ SUCCESS! Password: {result}")
        else:
            self.log_message("\n✗ Password not found with given parameters")
        
        self.finish_cracking()
    
    def stop_cracking(self):
        """Stop the cracking process"""
        if self.cracker:
            self.cracker.stop_cracking()
        self.log_message("\nCracking stopped by user")
        self.finish_cracking()
    
    def finish_cracking(self):
        """Finish the cracking process"""
        self.is_cracking = False
        self.progress_bar.stop()
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        
        if self.cracker:
            stats = self.cracker.get_stats()
            self.log_message("\n" + "=" * 60)
            self.log_message(f"Total attempts: {stats['attempts']}")
            self.log_message(f"Time elapsed: {stats['elapsed_time']:.2f} seconds")
            self.log_message(f"Speed: {stats['passwords_per_second']:.2f} passwords/second")


def main():
    root = tk.Tk()
    app = ArchiveCrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()