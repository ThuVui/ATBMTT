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
    file_path = "original.txt"

    # Nhập nội dung từ người dùng
    user_input = input("Nhập dữ liệu cần lưu vào file: ")

    # Ghi dữ liệu vào file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(user_input + "\n")

    # In ra hash
    print("\n HASH của dữ liệu bạn vừa nhập:")
    print("SHA-256:", calculate_hash(file_path, "sha256"))
    print("SHA-512:", calculate_hash(file_path, "sha512"))

if __name__ == "__main__":
    main()
