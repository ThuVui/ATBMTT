# receiver.py - Nhận file mã hóa và giải mã với giao diện đẹp hơn
import socket
import rsa
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
from tkinter import ttk

HOST = '0.0.0.0'
PORT = 65432

class ReceiverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Người Nhận - RSA File Receiver")
        self.root.geometry("500x300")
        self.root.configure(bg="#f0f4f8")

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)
        self.style.configure("TLabel", font=("Segoe UI", 11), background="#f0f4f8")

        ttk.Label(root, text="🛡️ Trình Nhận File Bảo Mật").pack(pady=10)
        ttk.Button(root, text="🔐 Tạo khóa nhận", command=self.generate_keys).pack(pady=5)

        self.status_label = ttk.Label(root, text="Đang chờ file gửi đến...", foreground="green")
        self.status_label.pack(pady=10)

        self.save_button = ttk.Button(root, text="💾 Lưu file giải mã", command=self.save_file)
        self.save_button.pack(pady=5)
        self.save_button['state'] = 'disabled'

        self.decrypted_data = None

        threading.Thread(target=self.listen_for_file, daemon=True).start()

    def generate_keys(self):
        pubkey, privkey = rsa.newkeys(2048)
        with open("receiver_public.pem", "wb") as pub_file:
            pub_file.write(pubkey.save_pkcs1())
        with open("receiver_private.pem", "wb") as priv_file:
            priv_file.write(privkey.save_pkcs1())
        messagebox.showinfo("Khóa RSA", "Đã tạo receiver_public.pem và receiver_private.pem")

    def listen_for_file(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    encrypted_data = conn.recv(65536)
                    self.status_label.config(text=f"📥 Đã nhận file từ {addr[0]}")
                    self.decrypt_file(encrypted_data)

    def decrypt_file(self, encrypted_data):
        try:
            with open("receiver_private.pem", "rb") as priv_file:
                privkey = rsa.PrivateKey.load_pkcs1(priv_file.read())
            self.decrypted_data = rsa.decrypt(encrypted_data, privkey)
            self.save_button['state'] = 'normal'
            messagebox.showinfo("Thành công", "Đã giải mã file, vui lòng chọn nơi lưu.")
        except Exception as e:
            messagebox.showerror("Lỗi giải mã", f"{str(e)}")

    def save_file(self):
        if self.decrypted_data:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if file_path:
                with open(file_path, 'wb') as f:
                    f.write(self.decrypted_data)
                messagebox.showinfo("Đã lưu", f"File đã lưu tại: {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReceiverApp(root)
    root.mainloop()
