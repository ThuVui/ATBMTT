import hashlib

def calculate_hash(file_path, algorithm="sha256"):
    """Băm file bằng SHA-256 hoặc SHA-512."""
    with open(file_path, "rb") as f:
        data = f.read()

    if algorithm == "sha256":
        return hashlib.sha256(data).hexdigest()
    elif algorithm == "sha512":
        return hashlib.sha512(data).hexdigest()
    else:
        raise ValueError("Chỉ hỗ trợ SHA-256 và SHA-512")

def main():
    original_path = "original.txt"
    modified_path = "modified.txt"

    # Nhập dữ liệu gốc
    original_data = input("Nhập dữ liệu ban đầu: ")
    with open(original_path, "w", encoding="utf-8") as f:
        f.write(original_data + "\n")

    print("\n➤ HASH của dữ liệu BAN ĐẦU:")
    sha256_original = calculate_hash(original_path, "sha256")
    sha512_original = calculate_hash(original_path, "sha512")
    print("SHA-256:", sha256_original)
    print("SHA-512:", sha512_original)

    # Nhập dữ liệu đã sửa
    modified_data = input("\nNhập dữ liệu sau khi sửa: ")
    with open(modified_path, "w", encoding="utf-8") as f:
        f.write(modified_data + "\n")

    print("\n HASH của dữ liệu ĐÃ SỬA:")
    sha256_modified = calculate_hash(modified_path, "sha256")
    sha512_modified = calculate_hash(modified_path, "sha512")
    print("SHA-256:", sha256_modified)
    print("SHA-512:", sha512_modified)

    # So sánh hash SHA-256
    print("\n KẾT LUẬN:")
    if sha256_original == sha256_modified:
        print("Dữ liệu KHÔNG bị thay đổi (hash SHA-256 giống nhau).")
    else:
        print("Dữ liệu ĐÃ BỊ THAY ĐỔI (hash SHA-256 khác nhau).")

if __name__ == "__main__":
    main()