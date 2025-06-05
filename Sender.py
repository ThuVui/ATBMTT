import socket
import rsa
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk

# Thay IP máy nhận ở đây nếu chạy LAN
HOST = '127.0.0.1'
PORT = 65432

class SenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Người Gửi - RSA File Sender")
        self.root.geometry("500x280")
        self.root.configure(bg="#f0f4f8")

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)
        self.style.configure("TLabel", font=("Segoe UI", 11), background="#f0f4f8")

        ttk.Label(root, text="📁 Chọn file cần gửi:").pack(pady=10)
        
        self.file_path = tk.StringVar()
        self.entry = ttk.Entry(root, textvariable=self.file_path, width=50)
        self.entry.pack()

        ttk.Button(root, text="Browse", command=self.browse_file).pack(pady=5)
        ttk.Button(root, text="🔐 Mã hóa & Gửi", command=self.encrypt_and_send).pack(pady=15)

        self.status_label = ttk.Label(root, text="", foreground="blue", background="#f0f4f8")
        self.status_label.pack()

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if path:
            self.file_path.set(path)

    def encrypt_and_send(self):
        if not self.file_path.get():
            messagebox.showwarning("Chưa chọn file", "Vui lòng chọn file để gửi.")
            return
        try:
            self.status_label.config(text="Đang đọc khóa công khai người nhận...")
            with open("receiver_public.pem", "rb") as pub_file:
                pubkey = rsa.PublicKey.load_pkcs1(pub_file.read())

            self.status_label.config(text="Đang đọc file và mã hóa...")
            with open(self.file_path.get(), "rb") as f:
                data = f.read()

            encrypted_data = rsa.encrypt(data, pubkey)

            self.status_label.config(text="Đang kết nối và gửi file...")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(encrypted_data)

            self.status_label.config(text="Gửi file thành công!")
            messagebox.showinfo("Thành công", "Đã mã hóa và gửi file thành công!")

        except FileNotFoundError:
            self.status_label.config(text="")
            messagebox.showerror("Lỗi", "Không tìm thấy file 'receiver_public.pem'. Vui lòng chắc chắn đã có file này.")
        except Exception as e:
            self.status_label.config(text="")
            messagebox.showerror("Lỗi", f"Lỗi khi gửi: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SenderApp(root)
    root.mainloop()
