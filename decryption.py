import base64

message = None
read_data = None

while True:
    with open("encrypted-message-holder.txt", "r+", encoding='utf-8') as message_file:
        message = message_file.read()

    with open("encrypt-instructions.txt", "r+", encoding='utf-8') as file:
        read_data = file.readline()
        file.seek(0)
        file.truncate()

    if read_data == "decrypt":
        with open("decrypted-message-holder.txt", "r+", encoding='utf-8') as message_file:
            missing_padding = len(message) % 4
            if missing_padding != 0:
                message += b'='* (4 - missing_padding)
            decoded_bytes = base64.b64decode(message)
            decoded_string = decoded_bytes.decode("utf-8")
            message_file.seek(0)
            message_file.truncate()
            message_file.write(decoded_string)
