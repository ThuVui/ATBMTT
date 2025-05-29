import hashlib
import os

def get_sha512_checksum(file_path):
    """Tính mã băm SHA-512 của file."""
    sha512_hash = hashlib.sha512()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha512_hash.update(byte_block)
    return sha512_hash.hexdigest()

def main():
    file_path = input("Nhập đường dẫn file ảnh cần kiểm tra: ")

    # Kiểm tra xem file có tồn tại không
    if not os.path.isfile(file_path):
        print(" File không tồn tại. Vui lòng kiểm tra lại đường dẫn.")
        return

    # Tính và in mã băm SHA-512
    checksum = get_sha512_checksum(file_path)
    print("\n Mã băm SHA-512 của file là:")
    print(checksum)

if __name__ == "__main__":
    main()