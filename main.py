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
ser = serial.Serial(port='COM14', baudrate=9600, timeout=1)  # TODO change this for pi
ser.reset_input_buffer()

root = tk.Tk()
root.title("ODUO GUI")
root.geometry("1024x600+100+0") # should be 1024 x 600
root.configure(bg="#f5721b")

# root.attributes("-fullscreen", True)
pinData = tk.StringVar()
otherValData = tk.StringVar()

pinInput = tk.StringVar()
otherValInput = tk.StringVar()
balanceVal = tk.StringVar()
balanceVal.set("¤ ....")

mainFrameDesign = tk.PhotoImage(file='Frames/Resized/mainFrame.png')
label = tk.Label(root, image=mainFrameDesign, borderwidth=0)
label.pack()
pinFrameDesign = tk.PhotoImage(file='Frames/Resized/pin-invoer.png')
incorrectPinFrameDesign = tk.PhotoImage(file='Frames/Resized/wrong-pin.png')
menuFrameDesign = tk.PhotoImage(file='Frames/Resized/main-menu.png')
balanceFrameDesign = tk.PhotoImage(file='Frames/Resized/balance.png')
withdrawFrameDesign = tk.PhotoImage(file='Frames/Resized/pin-amount.png')
otherValFrameDesign = tk.PhotoImage(file='Frames/Resized/ander-bedrag.png')
quickFrameDesign = tk.PhotoImage(file='Frames/Resized/snel-pin.png')
receiptFrameDesign = tk.PhotoImage(file='Frames/Resized/bon-scherm.png')
waitFrameDesign = tk.PhotoImage(file='Frames/Resized/wacht-scherm.png')
finalFrameDesign = tk.PhotoImage(file='Frames/Resized/end-screen.png')


aButtonDesign = tk.PhotoImage(file='Buttons/Abutton.png')
bButtonDesign = tk.PhotoImage(file='Buttons/Bbutton.png')
cButtonDesign = tk.PhotoImage(file='Buttons/Cbutton.png')
dButtonDesign = tk.PhotoImage(file='Buttons/Dbutton.png')
startButtonDesign = tk.PhotoImage(file='Frames/Resized/home-screen.png')


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
pinField = tk.Label(pinFrame, textvariable=pinInput, borderwidth=0, bg="#bababa", font=('Helvatical bold', 86))  # was 100
pinField.place(relx=0.2067, rely=0.39)

incorrectPinFrame = tk.Frame(root, bg="blue", borderwidth=0, highlightthickness=-1)
incorrectPinFrame.place(relwidth=0.7, relheight=0.94, relx=0.03, rely=0.03)
label = tk.Label(incorrectPinFrame, image=incorrectPinFrameDesign, borderwidth=0)
label.pack()

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

quickFrame = tk.Frame(root, bg="yellow")
quickFrame.place(relwidth=0.7, relheight=0.94, relx=0.03, rely=0.03)
label = tk.Label(quickFrame, image=quickFrameDesign, borderwidth=0)
label.pack()

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
    aButton.configure(command=pinput)
    bButton.configure(command=pundo)
    cButton.configure(command=confirm)
    pinData.set("")
    pinFrame.tkraise()


def incorrectPin():
    aButton.configure(command="none")
    bButton.configure(command="none")
    cButton.configure(command=pin)
    incorrectPinFrame.tkraise()
    incorrectPinFrame.after(3000, pin)

def menu():
    aButton.configure(command=balance)
    bButton.configure(command=withdraw)
    cButton.configure(command=quick)
    dButton.configure(command=cover)
    menuFrame.tkraise()


def balance():
    data["path"] = "/balance"
    json_object = json.dumps(data, indent=4)

    with open("out.json", "w") as outfile:
        outfile.write(json_object)

    my_request = urllib.request.urlopen("http://localhost:443/python")
    balanceVal.set("¤ " + my_request.read().decode("utf8"))
    print(balanceVal.get())
    aButton.configure(command=withdraw)
    bButton.configure(command="none")
    cButton.configure(command="none")
    dButton.configure(command=menu)
    balanceFrame.tkraise()


def withdraw():
    data["path"] = "/withdraw"

    aButton.configure(command="none")
    bButton.configure(command="none")
    cButton.configure(command=otherVal)
    dButton.configure(command=menu)
    withdrawFrame.tkraise()


def otherVal():
    aButton.configure(command=vinput)
    bButton.configure(command=vundo)
    cButton.configure(command=receipt)
    dButton.configure(command=menu)
    otherValInput.set("")
    otherValFrame.tkraise()


def quick():
    aButton.configure(command="none")
    bButton.configure(command="none")
    cButton.configure(command=receipt)
    dButton.configure(command=menu)
    quickFrame.tkraise()


def receipt():
    otherValString = str(otherValInput.get()).replace(" ", "")
    data["amount"] = otherValString
    pinInput.set("")
    json_object = json.dumps(data, indent=4)

    with open("out.json", "w") as outfile:
        outfile.write(json_object)

    my_request = urllib.request.urlopen("http://localhost:443/python")

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

    with open("out.json", "w") as outfile:
        outfile.write(json_object)

    my_request = urllib.request.urlopen("http://localhost:443/pypin")

    stringtest = my_request.read().decode("utf8")
    if not stringtest:
        ser.write(b"1\n")
        menu()
    else:
        ser.write(b"0\n")
        incorrectPin()


def pundo():
    pinInput.set(pinInput.get()[0:-2])
    pinData.set(pinData.get()[0:-1])


def vundo():
    otherValInput.set(otherValInput.get()[0:-2])


def pinput(numberData):
    if len(pinInput.get()) <= 6:
        pinInput.set(pinInput.get() + " *")
    pinData.set(pinData.get() + numberData)
    print(pinData.get())


def vinput(numberData):
    if len(otherValInput.get()) <= 4:
        otherValInput.set(otherValInput.get() + " " + numberData)


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
                    pinput(line)
                    vinput(line)
                print(line)


cover()
# otherVal()
startButton.configure(command=removeCover)
dButton.configure(command=cover)
threading.Thread(target=arduino).start()
root.mainloop()



