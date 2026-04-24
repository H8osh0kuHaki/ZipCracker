import customtkinter as ctk
from tkinter import filedialog, messagebox
import pyzipper
import threading
import os
import webbrowser

# Theme Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class CyberZipCracker(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Zip Hacker v1.0")
        self.geometry("700x600")
        self.configure(fg_color="#0a0a0a") # Deep black background

        # --- Header ---
        self.header = ctk.CTkLabel(self, text="⚡ NASA SYSTEM BYPASS ⚡", font=("Fixedsys", 32, "bold"), text_color="red")
        self.header.pack(pady=(20, 5))
        
        # --- Channel Link ---
        self.link_btn = ctk.CTkButton(self, text="JOIN OWNER CHANNEL", font=("Courier New", 12, "bold"),
                                     fg_color="transparent", border_width=1, border_color="#00FF41",
                                     text_color="#00FF41", hover_color="#003311",
                                     command=lambda: webbrowser.open("https://whatsapp.com/channel/0029Vb67pP1KwqSYyhvn3x1T"))
        self.link_btn.pack(pady=(0, 20))

        # --- File Selection Frame ---
        self.frame = ctk.CTkFrame(self, fg_color="#111111", border_width=1, border_color="#333333")
        self.frame.pack(pady=10, padx=20, fill="x")

        self.zip_btn = ctk.CTkButton(self.frame, text="TARGET ZIP", width=120, command=self.select_zip)
        self.zip_btn.grid(row=0, column=0, padx=10, pady=10)
        self.zip_label = ctk.CTkLabel(self.frame, text="NONE SELECTED", text_color="#555555")
        self.zip_label.grid(row=0, column=1, sticky="w")

        self.word_btn = ctk.CTkButton(self.frame, text="WORDLIST", width=120, command=self.select_wordlist)
        self.word_btn.grid(row=1, column=0, padx=10, pady=10)
        self.word_label = ctk.CTkLabel(self.frame, text="NONE SELECTED", text_color="#555555")
        self.word_label.grid(row=1, column=1, sticky="w")

        # --- Real-time testing Display ---
        self.status_frame = ctk.CTkFrame(self, fg_color="black", height=40)
        self.status_frame.pack(fill="x", padx=20, pady=5)
        self.current_test_label = ctk.CTkLabel(self.status_frame, text="IDLE: READY TO INFILTRATE", 
                                             font=("Courier New", 14), text_color="#00FF41")
        self.current_test_label.pack(pady=5)

        # --- Terminal Log ---
        self.log = ctk.CTkTextbox(self, fg_color="black", text_color="#00FF41", 
                                 font=("Courier New", 12), border_width=1, border_color="#00FF41")
        self.log.pack(pady=10, padx=20, fill="both", expand=True)

        # --- Action Button ---
        self.attack_btn = ctk.CTkButton(self, text="EXECUTE ATTACK", height=50, 
                                       font=("Courier New", 18, "bold"),
                                       fg_color="#004400", hover_color="#006600",
                                       command=self.start_attack)
        self.attack_btn.pack(pady=20, padx=20, fill="x")

        self.files = {"zip": "", "wordlist": ""}

    def select_zip(self):
        file = filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])
        if file:
            self.files["zip"] = file
            self.zip_label.configure(text=os.path.basename(file), text_color="#00FF41")

    def select_wordlist(self):
        file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file:
            self.files["wordlist"] = file
            self.word_label.configure(text=os.path.basename(file), text_color="#00FF41")

    def add_log(self, msg):
        self.log.insert("end", f"> {msg}\n")
        self.log.see("end")

    def start_attack(self):
        if not self.files["zip"] or not self.files["wordlist"]:
            messagebox.showerror("DENIED", "Specify target and wordlist first!")
            return
        
        self.attack_btn.configure(state="disabled", text="RUNNING...")
        threading.Thread(target=self.crack_logic, daemon=True).start()

    def crack_logic(self):
        self.add_log(f"Infiltrating: {os.path.basename(self.files['zip'])}")
        count = 0
        
        try:
            with open(self.files["wordlist"], 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    password = line.strip()
                    if not password: continue
                    
                    # Update real-time status label
                    self.current_test_label.configure(text=f"{password}")
                    
                    try:
                        with pyzipper.AESZipFile(self.files["zip"]) as zf:
                            zf.pwd = password.encode('utf-8')
                            if zf.testzip() is None:
                                self.add_log(f"CRACK SUCCESSFUL!")
                                self.add_log(f"KEY FOUND: {password}")
                                self.current_test_label.configure(text="ACCESS GRANTED", text_color="yellow")
                                messagebox.showinfo("DECRYPTED", f"Password: {password}")
                                self.attack_btn.configure(state="normal", text="EXECUTE ATTACK")
                                return
                    except:
                        pass
                    count += 1
            
            self.add_log("Attack Finished. Key not found.")
            self.current_test_label.configure(text="FAILED: NO KEY FOUND", text_color="red")
        except Exception as e:
            self.add_log(f"CRITICAL ERROR: {str(e)}")
        
        self.attack_btn.configure(state="normal", text="EXECUTE ATTACK")

if __name__ == "__main__":
    app = CyberZipCracker()
    app.mainloop()
