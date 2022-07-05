import tkinter as tk
import json
import urllib.request
import serial
import threading
from tkinter.ttk import *
data ={
    "toCtry": "",
    "toBank": "",

    "acctNo": "",
    "pin": "",
    "amount": "",

    "path": ""
}
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # TODO change this for pi
ser.reset_input_buffer()

root = tk.Tk()
root.title("ODUO GUI")
root.geometry("1024x600+0+0") # should be 1024 x 600
root.configure(bg="#f5721b")

root.attributes("-fullscreen", True)
pinData = tk.StringVar()
otherValData = tk.StringVar()

treadStop = False
keypadData = ""
pinInput = tk.StringVar()
attemptsLeft = tk.StringVar()
attemptsLeft.set("3")
withdrawAmount = tk.StringVar()
withdrawString = ""
otherValInput = tk.StringVar()
balanceVal = tk.StringVar()
balanceVal.set("¤ ....")

mainFrameDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Frames/Resized/mainFrame.png')
label = tk.Label(root, image=mainFrameDesign, borderwidth=0)
label.pack()
noBalanceFrameDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Frames/Resized/noBalance-screen.png')
pinFrameDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Frames/Resized/pin-invoer.png')
incorrectPinFrameDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Frames/Resized/wrong-pin-reworked.png')
menuFrameDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Frames/Resized/main-menu.png')
balanceFrameDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Frames/Resized/balance.png')
withdrawFrameDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Frames/Resized/pin-amount.png')
otherValFrameDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Frames/Resized/ander-bedrag.png')
confirmFrameDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Frames/Resized/confirmation-screen.png')
receiptFrameDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Frames/Resized/bon-scherm.png')
waitFrameDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Frames/Resized/wacht-scherm.png')
finalFrameDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Frames/Resized/end-screen.png')


aButtonDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Buttons/Abutton.png')
bButtonDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Buttons/Bbutton.png')
cButtonDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Buttons/Cbutton.png')
dButtonDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Buttons/Dbutton.png')
startButtonDesign = tk.PhotoImage(file='/home/pi/atm/ATM CODE/Frames/Resized/home-screen.png')


idleCover = tk.Frame(root, bg='black')
waitFrame = tk.Frame(root, bg="cyan")
label = tk.Label(waitFrame, image=waitFrameDesign, borderwidth=0)
label.pack()
finalFrame = tk.Frame(root, bg="magenta")
label = tk.Label(finalFrame, image=finalFrameDesign, borderwidth=0)
label.pack()


buttonArea = tk.Frame(root, bg="#bababa")
buttonArea.place(relwidth=0.2, relheight=0.94, relx=0.76, rely=0.03)

pinFrame = tk.Frame(root, bg="blue", borderwidth=0, highlightthickness=-1)
pinFrame.place(relwidth=0.7, relheight=0.94, relx=0.03, rely=0.03)  # 716.8 x 564
label = tk.Label(pinFrame, image=pinFrameDesign, borderwidth=0)
label.pack()
pinField = tk.Label(pinFrame, textvariable=pinInput, borderwidth=0, bg="#bababa", font=('Helvatical bold', 73))  # was 100
pinField.place(relx=0.2067, rely=0.39)

incorrectPinFrame = tk.Frame(root, bg="blue", borderwidth=0, highlightthickness=-1)
incorrectPinFrame.place(relwidth=0.7, relheight=0.94, relx=0.03, rely=0.03)
label = tk.Label(incorrectPinFrame, image=incorrectPinFrameDesign, borderwidth=0)
label.pack()
attemptsLeftField = tk.Label(incorrectPinFrame, textvariable=attemptsLeft, borderwidth=0, bg="#ff3232", fg="#ffffff", font=('Helvatical bold', 90))  # was 100
attemptsLeftField.place(relx=0.738, rely=0.575)

passBlockedFrame = tk.Frame(root, bg="#bababa", borderwidth=0, highlightthickness=-1)
passBlockedFrame.place(relwidth=0.7, relheight=0.94, relx=0.03, rely=0.03)
label = tk.Label(passBlockedFrame, text="Pass has been blocked", borderwidth=0, bg="#ff3232", fg="#ffffff", font=('Helvatical bold', 40))
label.place(relx=0.1, rely=0.4)

menuFrame = tk.Frame(root, bg="#bababa", borderwidth=0, highlightthickness=0)
menuFrame.place(relwidth=0.7, relheight=0.94, relx=0.03, rely=0.03)
label = tk.Label(menuFrame, image=menuFrameDesign, borderwidth=0)
label.pack()

balanceFrame = tk.Frame(root, bg="green")
balanceFrame.place(relwidth=0.7, relheight=0.94, relx=0.03, rely=0.03)
label = tk.Label(balanceFrame, image=balanceFrameDesign, borderwidth=0)
label.pack()
balanceField = tk.Label(balanceFrame, textvariable=balanceVal, borderwidth=0, bg="#f5721b", font=('Helvatical bold', 68))  # was 80
balanceField.place(relx=0.18, rely=0.45)

noBalanceFrame = tk.Frame(root, bg="green")
noBalanceFrame.place(relwidth=0.7, relheight=0.94, relx=0.03, rely=0.03)
label = tk.Label(noBalanceFrame, image=noBalanceFrameDesign, borderwidth=0)
label.pack()

withdrawFrame = tk.Frame(root, bg="red")
withdrawFrame.place(relwidth=0.7, relheight=0.94, relx=0.03, rely=0.03)
label = tk.Label(withdrawFrame, image=withdrawFrameDesign, borderwidth=0)
label.pack()

otherValFrame = tk.Frame(root, bg="orange")
otherValFrame.place(relwidth=0.7, relheight=0.94, relx=0.03, rely=0.03)
label = tk.Label(otherValFrame, image=otherValFrameDesign, borderwidth=0)
label.pack()
otherValField = tk.Label(otherValFrame, textvariable=otherValInput, borderwidth=0, bg="#bababa", font=('Helvatical bold', 68))  # was 80
otherValField.place(relx=0.32, rely=0.37)

confirmFrame = tk.Frame(root, bg="yellow")
confirmFrame.place(relwidth=0.7, relheight=0.94, relx=0.03, rely=0.03)
label = tk.Label(confirmFrame, image=confirmFrameDesign, borderwidth=0)
label.pack()
withdrawField = tk.Label(confirmFrame, textvariable=withdrawAmount, borderwidth=0, bg="#bababa", font=('Franklin Gothic Heavy', 30))  # was 80
withdrawField.place(relx=0.63, rely=0.335)

receiptFrame = tk.Frame(root, bg="pink")
receiptFrame.place(relwidth=0.7, relheight=0.94, relx=0.03, rely=0.03)
label = tk.Label(receiptFrame, image=receiptFrameDesign, borderwidth=0)
label.pack()


aButton = tk.Button(buttonArea, text="A", command="none", image=aButtonDesign, borderwidth=-1, bg="#bebebe")
aButton.place(relx=0.5, rely=0.2, anchor='center')

bButton = tk.Button(master=buttonArea, text="B", command="none", image=bButtonDesign, borderwidth=-1, bg="#bebebe")
bButton.place(relx=0.5, rely=0.4, anchor='center')

cButton = tk.Button(master=buttonArea, text="C", command="none", image=cButtonDesign, borderwidth=-1, bg="#bebebe")
cButton.place(relx=0.5, rely=0.6, anchor='center')

dButton = tk.Button(master=buttonArea, text="D", command="none", image=dButtonDesign, borderwidth=-1, bg="#bebebe")
dButton.place(relx=0.5, rely=0.8, anchor='center')

startButton = tk.Button(idleCover, image=startButtonDesign, borderwidth=-1, command="none")
startButton.place(relwidth=1, relheight=1)


# lbl_value = tk.Label(master=root, text="0")
# lbl_value.grid(row=0, column=1)

def pin():
    pinInput.set("")
    aButton.configure(command=pinput)
    bButton.configure(command=pundo)
    cButton.configure(command=confirm)
    pinData.set("")
    pinFrame.tkraise()


def incorrectPin():
    aButton.configure(command="none")
    bButton.configure(command="none")
    cButton.configure(command=pin)
    if int(attemptsLeft.get()) == 0:
        passBlockedFrame.tkraise()
        passBlockedFrame.after(3000, pin)
    else:
        incorrectPinFrame.tkraise()
        incorrectPinFrame.after(3000, pin)


def menu():
    global treadStop
    treadStop = True
    data["path"] = "/balance"
    json_object = json.dumps(data, indent=4)

    with open("/home/pi/atm/ATM CODE/out.json", "w") as outfile:
        outfile.write(json_object)
        
    noBalanceFrame.place_forget()
    aButton.configure(command=balance)
    bButton.configure(command=withdraw)
    cButton.configure(command=amount70)
    dButton.configure(command=cover)
    menuFrame.tkraise()


def noBalance():
    noBalanceFrame.place(relwidth=1, relheight=1)
    noBalanceFrame.tkraise()
    noBalanceFrame.after(2000, menu)


def balance():
    data["path"] = "/balance"
    json_object = json.dumps(data, indent=4)

    with open("/home/pi/atm/ATM CODE/out.json", "w") as outfile:
        outfile.write(json_object)

    my_request = urllib.request.urlopen("http://127.0.0.1:8443/python")
    balanceVal.set("¤ " + my_request.read().decode("utf8"))
    print(balanceVal.get())
    aButton.configure(command=withdraw)
    bButton.configure(command="none")
    cButton.configure(command="none")
    dButton.configure(command=menu)
    balanceFrame.tkraise()


def amountOther():
    withdrawAmount.set(otherValInput.get())
    if withdrawAmount != "":
        confirmAmount()
    else:
        ser.write(b"0\n")


def amount300():
    global treadStop
    treadStop = True
    withdrawAmount.set("300")
    confirmAmount()


def amount200():
    global treadStop
    treadStop = True
    withdrawAmount.set("200")
    confirmAmount()


def amount150():
    withdrawAmount.set("150")
    confirmAmount()


def amount100():
    withdrawAmount.set("100")
    confirmAmount()


def amount50():
    withdrawAmount.set("50")
    confirmAmount()


def amount20():
    withdrawAmount.set("20")
    confirmAmount()


def amount70():
    json_object = json.dumps(data, indent=4)

    with open("/home/pi/atm/ATM CODE/out.json", "w") as outfile:
        outfile.write(json_object)

    my_request = urllib.request.urlopen("http://127.0.0.1:8443/pypin")

    stringtest = my_request.read().decode("utf8")
    print(stringtest)
    if not stringtest:
        ser.write(b"1\n")
        withdrawAmount.set("70")
        confirmAmount()
    elif int(stringtest) < 0:
        ser.write(b"0\n")
        noBalance()


def withdraw():
    global keypadData

    json_object = json.dumps(data, indent=4)

    with open("/home/pi/atm/ATM CODE/out.json", "w") as outfile:
        outfile.write(json_object)
    
    my_request = urllib.request.urlopen("http://127.0.0.1:8443/pypin")

    stringtest = my_request.read().decode("utf8")
    print(stringtest)
    if not stringtest:
        ser.write(b"1\n")
        data["path"] = "/withdraw"
        aButton.configure(command=amount200)
        bButton.configure(command=amount300)
        cButton.configure(command=otherVal)
        dButton.configure(command=menu)
        withdrawFrame.tkraise()
        keypadData = ""
        threading.Thread(target=withdrawCheck).start()
    elif int(stringtest) < 0:
        ser.write(b"0\n")
        noBalance()


def withdrawCheck():
    global treadStop
    treadStop = False
    while True:
        if treadStop:
            print("=========================================")
            break
        elif keypadData == '1':
            treadStop = True
            print(treadStop)
            return amount20()
        elif keypadData == '4':
            treadStop = True
            return amount50()
        elif keypadData == '7':
            treadStop = True
            return amount100()
        elif keypadData == '*':
            treadStop = True
            return amount150()


def otherVal():
    global treadStop
    treadStop = True
    aButton.configure(command=vinput)
    bButton.configure(command=vundo)
    cButton.configure(command=amountOther)
    dButton.configure(command=menu)
    otherValInput.set(" 0")
    otherValFrame.tkraise()


def confirmAmount():
    ser.write(b"1\n")  # TODO make this proper
    global treadStop
    treadStop = True
    global withdrawString
    withdrawString = (str(withdrawAmount.get()).replace(" ", ""))
    aButton.configure(command="none")
    bButton.configure(command="none")
    cButton.configure(command=receipt)
    dButton.configure(command=menu)
    confirmFrame.tkraise()


def receipt():
    data["amount"] = withdrawString
    pinInput.set("")
    json_object = json.dumps(data, indent=4)

    with open("/home/pi/atm/ATM CODE/out.json", "w") as outfile:
        outfile.write(json_object)

    my_request = urllib.request.urlopen("http://127.0.0.1:8443/python")

    aButton.configure(command="none")
    bButton.configure(command="none")
    cButton.configure(command=wait)
    dButton.configure(command=wait)  # become deny
    receiptFrame.tkraise()


def wait():
    waitFrame.place(relwidth=1, relheight=1)
    waitFrame.tkraise()
    waitFrame.after(2000, final)


def final():
    finalFrame.place(relwidth=1, relheight=1)
    waitFrame.place_forget()
    finalFrame.tkraise()
    finalFrame.after(5000, cover)


def confirm():  # confirm pin input
    pinInput.set("")
    pinString = str(pinData.get()).replace(" ", "")
    pinData.set("")
    data["pin"] = pinString
    data["path"] = "/balance"
    json_object = json.dumps(data, indent=4)

    with open("/home/pi/atm/ATM CODE/out.json", "w") as outfile:
        outfile.write(json_object)

    my_request = urllib.request.urlopen("http://127.0.0.1:8443/pypin")

    stringtest = my_request.read().decode("utf8")
    if not stringtest or int(stringtest) < 0:
        ser.write(b"1\n")
        menu()
    elif int(stringtest) >= 0:
        ser.write(b"0\n")
        if int(stringtest) > 0:
            stringtest = int(stringtest) - 1
        attemptsLeft.set(stringtest)
        incorrectPin()


def pundo():
    pinInput.set(pinInput.get()[0:-2])
    pinData.set(pinData.get()[0:-1])


def vundo():
    otherValInput.set(otherValInput.get()[2:-2] + " 0")


def pinput(numberData):
    if len(pinInput.get()) <= 6:
        pinInput.set(pinInput.get() + " *")
    pinData.set(pinData.get() + numberData)
    print(pinData.get())


def vinput(numberData):
    if len(otherValInput.get()) <= 4:
        if len(otherValInput.get()) <= 2:
            otherValInput.set(" " + numberData + otherValInput.get())
        elif int(numberData) <= 2:
            otherValInput.set(" " + numberData + otherValInput.get())
        elif int(numberData) >= 3:
                otherValInput.set(" 3 0 0")



def cover():
    idleCover.place(relwidth=1, relheight=1)
    idleCover.tkraise()
    finalFrame.place_forget()
    pinInput.set("")


def removeCover():
    # data["acctNo"] = "GLODUO0000135700"
    data["toCtry"] = data["acctNo"][:2]
    data["toBank"] = data["acctNo"][2:6]
    idleCover.place_forget()
    pin()


def arduino():
    if __name__ == '__main__':
        global keypadData
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                if line[:1] == '+':
                    data["acctNo"] = line[1:]
                    removeCover()
                elif line == 'A':
                    aButton.invoke()
                elif line == 'B':
                    bButton.invoke()
                elif line == 'C':
                    cButton.invoke()
                elif line == 'D':
                    dButton.invoke()
                else:
                    keypadData = line
                    pinput(line)
                    vinput(line)
                print(line)


cover()
# otherVal()
startButton.configure(command=removeCover)
dButton.configure(command=cover)
threading.Thread(target=arduino).start()
root.mainloop()