"""
Author: Long To Lotto Tang
Date: 7/10/2023
Course: CS361 Personal Project
Description: "main.py" provides a graphical user-interface (GUI) for EZChat
"""

# libraries
from tkinter import *
from tkinter.font import Font
from tkinter import ttk

import Pmw # pip install Pmw
import time
import heapq
import os

# Window asking confirmation for entering the Advanced Mode
def alert_advanced():
    
    alert_window = Toplevel()
    alert_window.title('ALERT')
    alert_window.resizable(0, 0)
    
    # Size of the Choose User Window
    alert_window_width = 400
    alert_window_height = 250
    position_x = (screen_width/2) - (alert_window_width/2)
    position_y = (screen_height/2) - (alert_window_height/2)
    alert_window.geometry(f'{alert_window_width}x{alert_window_height}+{int(position_x)}+{int(position_y)}')
    
    # Content of the Choose User Window
    message1 = "ALERT\n\nAdvanced mode is for experienced user only\n(Showing the encrypted text)\n\nPlease confirm for entering this mode:"
    alert_label = Label(alert_window, text=message1, font=normal_text, fg='red')
    alert_label.pack(pady=5)

    alert1 = Button(alert_window, text="Yes", command=lambda: choose_user(1),
                    padx=40, pady=10, font=button_text)
    alert1.pack(side=LEFT, padx=35)
    alert2 = Button(alert_window, text="No", command=alert_window.destroy,
                    padx=40, pady=10, font=button_text)
    alert2.pack(side=RIGHT, padx=35)

# Window to choose User1 or User2 (for Advanced Mode)
def choose_user(mode):
    user_window = Toplevel()
    user_window.title('Choose a User')
    user_window.resizable(0, 0)

    # Size of the Choose User Window
    user_window_width = 400
    user_window_height = 250
    position_x = (screen_width/2) - (user_window_width/2)
    position_y = (screen_height/2) - (user_window_height/2)
    user_window.geometry(f'{user_window_width}x{user_window_height}+{int(position_x)}+{int(position_y)}')

    # Helper function for choosing the corresponding mode
    def choose_chatbox(mode, user):
        if user == 1 and mode == 1:
            chatbox_advanced(1)
        elif user == 2 and mode == 1:
            chatbox_advanced(2)
        elif user == 1 and mode == 0:
            chatbox_simplified(1)
        elif user == 2 and mode == 0:
            chatbox_simplified(2)

    # Content of the Choose User Window
    user_window.title('Please Choose a User')
    message1 = "Select User1 for application window1\nUser2 for application window2"
    user_prompt = Label(user_window, text=message1, font=normal_text)
    user_prompt.pack(pady=15)
    user1 = Button(user_window, text="User1", font=button_text,
                   command=lambda: choose_chatbox(mode, 1), padx=40, pady=5)
    user1.pack(pady=5)
    user2 = Button(user_window, text="User2", font=button_text,
                   command=lambda: choose_chatbox(mode, 2), padx=40, pady=5)
    user2.pack(pady=5)


# Write the encryption instruction to external text
def activate_encryption():
    with open("encrypt-instructions.txt", "r+") as file:
        file.seek(0)
        file.truncate()
        file.write("encrypt")


# Write the decryption instruction to external text
def activate_decryption():
    with open("encrypt-instructions.txt", "r+") as file:
        file.seek(0)
        file.truncate()
        file.write("decrypt")


# Write the valid message to external file (for encryption)
def write_encryption(text):
    with open("encrypted-message-holder.txt", "r+") as message_file:
        message_file.seek(0)
        message_file.truncate()
        message_file.write(text)

# Read the encrypted text from external file
def read_encrypted():
    with open("encrypted-message-holder.txt", "r") as message_file:
        return message_file.readline()

# Check the length of the outgoing text (in characters) and activate the encryption/decryption process
def check_text(text, msg_queue, user_number):
    global msgID_counter
    text_length = len(text)
    valid = True
    # if valid, write to the encrypted-message-holder.txt
    if text_length > 0 and text_length <= 1000:
        # accept only characters within ascii 32 - 126 (inclusive)
        for i in range(text_length):
            if ord(text[i]) < 32 or ord(text[i]) > 126:
                valid = False
            if not valid:
                print('Invalid characters spotted!')
                break
    # number of characters out of range
    else:
        print("Maximum characters exceeded per single transmission!")
        valid = False
    
    if valid:
        write_encryption(text)
        activate_encryption()
        time.sleep(1)
        encrypted_text = read_encrypted()
        activate_decryption()
        heapq.heappush(msg_queue, (f"{time.time()}-/xseparator{time.strftime('%m-%d %H:%M',time.localtime())}-/xseparator{user_number}-/xseparator{text}-/xseparator{encrypted_text}-/xseparator{msgID_counter}"))
        save_chat(msg_queue)
        msgID_counter += 1

# Save the messages into external file for record
def save_chat(msg_queue):
    with open("message_record.txt", "a") as record_file:
        msg = heapq.heappop(msg_queue)
        record_file.write(f'{msg}\n')

# Window for Chatbox (Advanced Version)
def chatbox_advanced(user_number):
    
    chatbox_window = Toplevel()
    chatbox_window.title('EZChat - Advanced Mode')
    chatbox_window.resizable(0, 0)

    # Size of the Choose User Window
    chatbox_window_width = 600
    chatbox_window_height = 700
    position_x = (screen_width/2) - (chatbox_window_width/2)
    position_y = (screen_height/2) - (chatbox_window_height/2)
    chatbox_window.geometry(f'{chatbox_window_width}x{chatbox_window_height}+{int(position_x)}+{int(position_y)}')

    # Header of the Chatbox
    if user_number == 1:
        recipent_number = 2
    else:
        recipent_number = 1

    # Header Canvas
    header_canvas = Canvas(chatbox_window, bg="#435B66", width=600, height=50,
                           highlightthickness=0)
    header_canvas.grid(row=0, column=0, sticky=EW)

    chatbox_window.grid_columnconfigure(0, weight=1)
    header_canvas.grid_columnconfigure((0, 5), minsize=150)

    back_button = Button(header_canvas, text="Return", font=normal_text,
                         command=chatbox_window.destroy)
    back_button.grid(row=0, column=0, pady=15)
    
    back_tooltip = Pmw.Balloon(chatbox_window)
    back_tooltip.bind(back_button, 'Click to return to mainpage.')

    header_canvas.create_text((300, 35), text=f"User{recipent_number}",
                              font=heading4, fill="white")
    
    # Chatbox
    chatbox_frame = Frame(chatbox_window, width=600, height=330)
    chatbox_frame.grid(row=1, column=0)

    chatbox_canvas = Canvas(chatbox_frame, background="#9DB2BF", width=600, 
                            height=330, highlightthickness=0,
                            scrollregion=(0, 0, 800, 3000))
    chatbox_canvas.grid(row=0, column=1)

    vbar = Scrollbar(chatbox_frame, orient="vertical")
    vbar.grid(row=0, column=1, sticky=NS+E)
    vbar.config(command=chatbox_canvas.yview)

    chatbox_canvas.config(width=600, height=330)
    chatbox_canvas.config(yscrollcommand=vbar.set)
    
    # For placeholder
    def click(event):
        input_text.config(state=NORMAL)
        input_text.delete(0, END)

    # Input Frame
    input_frame = Frame(chatbox_window, bg="#435B66", width=600, height=55)
    input_frame.grid(row=2, column=0)

    input_frame.grid_columnconfigure((0, 1), minsize=300)

    input_text = Entry(input_frame)
    input_text.insert(0, "Enter Text Here")
    input_text.config(state=DISABLED)
    input_text.bind("<Button-1>", click)
    input_text.grid(row=1, column=0, padx=20, ipadx=170, ipady=10)

    # Display messages on the screen
    def display_message(msg_positionY):
        with open("message_record.txt", "r") as record_file:
            for line in record_file:
                extracted_msg = line.split('-/xseparator')
                if (user_number == 1 and extracted_msg[2] == "1") or (user_number == 2 and extracted_msg[2] == "2"):
                    msg_positionX = 10
                    anchor = "w"
                else:
                    msg_positionX = 575
                    anchor = "e"
                msg = chatbox_canvas.create_text(msg_positionX, msg_positionY, anchor=anchor, text=f"User{extracted_msg[2]}: {extracted_msg[3]}", font=message_text)  
                msg_positionY += 20 
                msg = chatbox_canvas.create_text(msg_positionX, msg_positionY, anchor=anchor, text=extracted_msg[1])    
                msg_positionY += 20

    display_message(msg_positionY)

    refresh_button = Button(header_canvas, text="Refresh", font=normal_text,
                         command=lambda: display_message(msg_positionY))
    refresh_button.grid(row=0, column=1, pady=15, sticky=E)
    refresh_tooltip = Pmw.Balloon(chatbox_window)
    refresh_tooltip.bind(refresh_button, 'Click to refresh messages.')

     # Clear the chat messages
    def clear_chat(alert_window):
        alert_window.destroy()
        with open("message_record.txt", "r+") as record_file:
            record_file.seek(0)
            record_file.truncate()
            chatbox_window.destroy()

    # Window asking confirmation for clearing all the messages
    def alert_clearMsg():
    
        alert_window = Toplevel()
        alert_window.title('ALERT')
        alert_window.resizable(0, 0)
        
        # Size of the Choose User Window
        alert_window_width = 400
        alert_window_height = 250
        position_x = (screen_width/2) - (alert_window_width/2)
        position_y = (screen_height/2) - (alert_window_height/2)
        alert_window.geometry(f'{alert_window_width}x{alert_window_height}+{int(position_x)}+{int(position_y)}')
        
        # Content of the Choose User Window
        message1 = "ALERT\n\nAll messages will be cleared with no recovery!\n\nPlease confirm:"
        alert_label = Label(alert_window, text=message1, font=normal_text, fg='red')
        alert_label.pack(pady=5)

        alert1 = Button(alert_window, text="Yes", command=lambda:clear_chat(alert_window),
                        padx=40, pady=10, font=button_text)
        alert1.pack(side=LEFT, padx=35)
        alert2 = Button(alert_window, text="No", command=alert_window.destroy,
                        padx=40, pady=10, font=button_text)
        alert2.pack(side=RIGHT, padx=35)

    clear_button = Button(header_canvas, text="Clear Chat", font=normal_text,
                         command=alert_clearMsg)
    clear_button.grid(row=0, column=2, padx=150, pady=15, sticky=W)
    clear_tooltip = Pmw.Balloon(chatbox_window)
    clear_tooltip.bind(clear_button, 'Click to clear all messages.')

    # extract the entry text
    def send_msg():
        msg = input_text.get()
        if msg:
            check_text(msg, msg_queue, user_number)
            input_text.delete(0, END)
            display_message(msg_positionY)
            insert_encrypted()
        else:
            return

    send_button = Button(input_frame, text="Send", font=normal_text,
                         command=send_msg)
    send_button.grid(row=1, column=1, padx=15, pady=10, sticky=W)

    send_tooltip = Pmw.Balloon(chatbox_window)
    send_tooltip.bind(send_button, 'Click to send the message.')

    # Encrypted Frame
    encrypred_frame = Frame(chatbox_window, width=600)
    encrypred_frame.grid(row=3, column=0)

    encrypred_canvas = Canvas(encrypred_frame, width=600,
                              highlightthickness=0, scrollregion=(0, 0, 200, 200))
    encrypred_canvas.grid(row=0, column=0)

    yscrollbar = Scrollbar(encrypred_canvas, orient="vertical")
    
    # Tree view setup
    tree = ttk.Treeview(encrypred_canvas, columns=("c0"))
    tree.grid(row=0, column=0)

    tree.column("#0", width=70, anchor=W, stretch=NO)
    tree.column("#1", width=510, anchor=W, stretch=NO)

    tree.heading("#0", text="MessageID")
    tree.heading("#1", text="Encrypted Text")

    # Display all encrypted messages when new window is opened
    def display_encrypted():
        with open("message_record.txt", "r") as record_file:
            for line in record_file:
                extracted_msg = line.split('-/xseparator')
                tree.insert('', 'end', text=extracted_msg[5], values=(extracted_msg[4]))

    # Display all encrypted messages when new window is opened
    def insert_encrypted():
        with open("message_record.txt", "r") as record_file:
            last_line = record_file.readlines()[-1]
            extracted_msg = last_line.split('-/xseparator')
            tree.insert('', 'end', text=extracted_msg[5], values=(extracted_msg[4]))

    # Display the previous messages first
    display_message(msg_positionY)
    display_encrypted()

    yscrollbar.configure(command=tree.yview)
    yscrollbar.grid(row=0, column=1, sticky=NS)



# Window for Chatbox (Simplified Version)
def chatbox_simplified(user_number):
    
    chatbox_window = Toplevel()
    chatbox_window.title('EZChat - Simplified Mode')
    chatbox_window.resizable(0, 0)

    # Size of the Choose User Window
    chatbox_window_width = 600
    chatbox_window_height = 700
    position_x = (screen_width/2) - (chatbox_window_width/2)
    position_y = (screen_height/2) - (chatbox_window_height/2)
    chatbox_window.geometry(
        f'{chatbox_window_width}x{chatbox_window_height}+{int(position_x)}+{int(position_y)}')

    # Header of the Chatbox
    if user_number == 1:
        recipent_number = 2
    else:
        recipent_number = 1

    # Header Canvas
    header_canvas = Canvas(chatbox_window, bg="#435B66", width=600, height=50,
                           highlightthickness=0)
    header_canvas.grid(row=0, column=0, sticky=EW)

    chatbox_window.grid_columnconfigure(0, weight=1)
    header_canvas.grid_columnconfigure((0, 5), minsize=150)

    back_button = Button(header_canvas, text="Return", font=normal_text,
                         command=chatbox_window.destroy)
    back_button.grid(row=0, column=0, padx=10, pady=15, sticky=E)
    back_tooltip = Pmw.Balloon(chatbox_window)
    back_tooltip.bind(back_button, 'Click to return to mainpage.')

    header_canvas.create_text((300, 35), text=f"User{recipent_number}",
                              font=heading4, fill="white")
    
    # Chatbox
    chatbox_frame = Frame(chatbox_window, width=600, height=565)
    chatbox_frame.grid(row=1, column=0)

    chatbox_canvas = Canvas(chatbox_frame, background="#9DB2BF", width=600,
                            height=565, highlightthickness=0,
                            scrollregion=(0, 0, 800, 3000))
    chatbox_canvas.grid(row=0, column=1)

    vbar = Scrollbar(chatbox_frame, orient="vertical")
    vbar.grid(row=0, column=1, sticky=NS+E)
    vbar.config(command=chatbox_canvas.yview)

    chatbox_canvas.config(width=600, height=565)
    chatbox_canvas.config(yscrollcommand=vbar.set)

    # For placeholder
    def click(event):
        input_text.config(state=NORMAL)
        input_text.delete(0, END)

    # Input Frame
    input_frame = Frame(chatbox_window, bg="#435B66", width=600, height=55)
    input_frame.grid(row=3, column=0)

    input_frame.grid_columnconfigure((0, 1), minsize=300)

    input_text = Entry(input_frame)
    input_text.insert(0, "Enter Text Here")
    input_text.config(state=DISABLED)
    input_text.bind("<Button-1>", click)
    input_text.grid(row=0, column=0, padx=20, ipadx=170, ipady=10)

    # Display messages on the screen
    def display_message(msg_positionY):
        with open("message_record.txt", "r") as record_file:
            for line in record_file:
                extracted_msg = line.split('-/xseparator')
                if (user_number == 1 and extracted_msg[2] == "1") or (user_number == 2 and extracted_msg[2] == "2"):
                    msg_positionX = 10
                    anchor = "w"
                else:
                    msg_positionX = 575
                    anchor = "e"
                msg = chatbox_canvas.create_text(msg_positionX, msg_positionY, anchor=anchor, text=f"User{extracted_msg[2]}: {extracted_msg[3]}", font=message_text)  
                msg_positionY += 20 
                msg = chatbox_canvas.create_text(msg_positionX, msg_positionY, anchor=anchor, text=extracted_msg[1])    
                msg_positionY += 20
    
    display_message(msg_positionY)

    refresh_button = Button(header_canvas, text="Refresh", font=normal_text,
                         command=lambda: display_message(msg_positionY))
    refresh_button.grid(row=0, column=1, pady=15, sticky=E)
    refresh_tooltip = Pmw.Balloon(chatbox_window)
    refresh_tooltip.bind(refresh_button, 'Click to refresh messages.')

    # Clear the chat messages
    def clear_chat(alert_window):
        alert_window.destroy()
        with open("message_record.txt", "r+") as record_file:
            record_file.seek(0)
            record_file.truncate()
            chatbox_window.destroy()

    # Window asking confirmation for clearing all the messages
    def alert_clearMsg():
    
        alert_window = Toplevel()
        alert_window.title('ALERT')
        alert_window.resizable(0, 0)
        
        # Size of the Choose User Window
        alert_window_width = 400
        alert_window_height = 250
        position_x = (screen_width/2) - (alert_window_width/2)
        position_y = (screen_height/2) - (alert_window_height/2)
        alert_window.geometry(f'{alert_window_width}x{alert_window_height}+{int(position_x)}+{int(position_y)}')
        
        # Content of the Choose User Window
        message1 = "ALERT\n\nAll messages will be cleared with no recovery!\n\nPlease confirm:"
        alert_label = Label(alert_window, text=message1, font=normal_text, fg='red')
        alert_label.pack(pady=5)

        alert1 = Button(alert_window, text="Yes", command=lambda:clear_chat(alert_window),
                        padx=40, pady=10, font=button_text)
        alert1.pack(side=LEFT, padx=35)
        alert2 = Button(alert_window, text="No", command=alert_window.destroy,
                        padx=40, pady=10, font=button_text)
        alert2.pack(side=RIGHT, padx=35)

    clear_button = Button(header_canvas, text="Clear Chat", font=normal_text,
                         command=alert_clearMsg)
    clear_button.grid(row=0, column=2, padx=150, pady=15, sticky=W)
    clear_tooltip = Pmw.Balloon(chatbox_window)
    clear_tooltip.bind(clear_button, 'Click to clear all messages.')
    
    # extract the entry text
    def send_msg():
        msg = input_text.get()
        if msg:
            check_text(msg, msg_queue, user_number)
            input_text.delete(0, END)
            display_message(msg_positionY)
        else:
            return

    send_button = Button(input_frame, text="Send", font=normal_text,
                         command=send_msg)
    send_button.grid(row=0, column=1, padx=15, pady=10, sticky=W)

    send_tooltip = Pmw.Balloon(chatbox_window)
    send_tooltip.bind(send_button, 'Click to send the message.')


# Setting up the GUI
root = Tk()
root.title("EZChat")
Pmw.initialise(root)

# Font
heading1 = Font(
    family="Segoe UI",
    size=60,
    weight="bold"
)

heading2 = Font(
    family="Segoe UI",
    size=24,
    weight="bold"
)

heading3 = Font(
    family="Segoe UI",
    size=18,
    underline=1
)

heading4 = Font(
    family="Segoe UI",
    size=18,
    weight="bold"
)

normal_text = Font(
    family="Segoe UI",
    size=14
)

button_text = Font(
    family="Segoe UI",
    size=16,
    weight="bold"
)

message_text = Font(
    family="Segoe UI",
    size=12
)

style = ttk.Style(root)
style.theme_use("clam") # set theam to clam
style.configure("Treeview", background="#32444D",
                fieldbackground="#32444D", foreground="white")

# Size of the GUI
root_width = 1024
root_height = 768
root.resizable(0, 0)
root.grid_columnconfigure((0, 4), weight=1)

# Positioning
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
screen_x = (screen_width/2) - (root_width/2)
screen_y = (screen_height/2) - (root_height/2)
root.geometry(f'{root_width}x{root_height}+{int(screen_x)}+{int(screen_y)}')

# Content of the GUI
title = Label(root, text="EZChat", font=heading1)
title.grid(row=0, column=2)

# Sub-Heading
sub_title = Label(root, text="- Simple and Secure Text Communication -", font=heading2)
sub_title.grid(row=1, column=2)

# User Guide
guide_frame = LabelFrame(root)
guide_frame.grid(row=2, column=0, columnspan=5, ipadx=15, pady=15)

guide1 = Label(guide_frame, text="User Guide:", font=heading3)
guide1.grid(row=3, column=0, sticky=W)

guide2 = Label(guide_frame, text="1. This application only accepts alphanumeric characters", font=normal_text)
guide2.grid(row=4, column=0, sticky=W)

guide3 = Label(guide_frame, text="2. To demonstrate the send and receive function, please open 2 application windows", font=normal_text)
guide3.grid(row=5, column=0, sticky=W)

guide4 = Label(guide_frame, text="    (choose User1 and User2 respectively after choosing the mode) ", font=normal_text)
guide4.grid(row=6, column=0, sticky=W)

guide5 = Label(guide_frame, text="3. This application contains 2 modes for users:", font=normal_text)
guide5.grid(row=7, column=0, sticky=W)

guide6 = Label(guide_frame, text="   - Simplified Mode: Send text messages (Suitable for Normal User)", font=normal_text)
guide6.grid(row=8, column=0, sticky=W)

guide7 = Label(guide_frame, text="   - Advanced Mode: Send and view the original and encrypted text messages (Suitable for Experienced User)", font=normal_text)
guide7.grid(row=9, column=0, sticky=W)

# Buttons for entering the Modes
simplified_button = Button(root, text="Start a Chat\n(Simplified Mode)", font=button_text, command=lambda: choose_user(0), padx=30, pady=20)
simplified_button.grid(row=10, column=2, pady=10)

simplified_tooltip = Pmw.Balloon(root)
simplified_tooltip.bind(simplified_button, 'Suitable for all users.')

advanced_button = Button(root, text="Start a Chat\n(Advanced Mode)", font=button_text, command=alert_advanced, padx=30, pady=20)
advanced_button.grid(row=11, column=2, pady=10)

advanced_tooltip = Pmw.Balloon(root)
advanced_tooltip.bind(advanced_button, 'Suitable for advanced users only.')

# Message variable
msg_queue = []
msg_positionY = 20
global msgID_counter
msgID_counter = 1
global msgID_queue
msgID_queue = []

mainloop()