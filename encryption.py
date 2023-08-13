import base64

message = None

while True:
    with open("encrypt-instructions.txt", "r+") as file:
        read_data = file.readline()
        file.seek(0)
        file.truncate()
    
    if read_data == "encrypt":
        with open("encrypted-message-holder.txt", "r+") as message_file:
            message = message_file.read()
            message_file.seek(0)
            message_file.truncate()
            encoded_string = base64.b64encode(message.encode("utf-8")).decode("utf-8")
            print(encoded_string)
            message_file.write(encoded_string)
