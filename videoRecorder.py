import PIL
from PIL import Image,ImageTk
import cv2
from tkinter import *
import time

def videoRecorderMain(questionID, questionText, masterWindow):

    def releaseEverything(cap, out, root):
        out.release()
        cap.release()
        cv2.destroyAllWindows()
        root.quit()
        root.destroy()


    def show_frame():
        _, frame = cap.read()
        out.write(frame)
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = PIL.Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img.resize((camGuiWidth, camGuiHeight), resample=PIL.Image.Resampling.NEAREST))
        camVideoTK.imgtk = imgtk
        camVideoTK.configure(image=imgtk)
        camVideoTK.after(10, show_frame)

    width, height = 800, 600

    camGuiWidth, camGuiHeight = 200, 150

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    out = cv2.VideoWriter('content/videos/Question{}.mp4'.format(questionID), cv2.VideoWriter_fourcc(*'mp4v'), 25, (int(cap.get(3)), int(cap.get(4))))

    root = Toplevel(masterWindow)
    root.transient(masterWindow)
    root.title('Raven')
    root.configure(bg='white')
    root.iconbitmap(bitmap='content/icon.ico')
    root.attributes('-fullscreen', True)
    root.geometry('{}x{}'.format(int(root.winfo_screenwidth() - 25), int(root.winfo_screenheight() - 100)))

    root.grid_rowconfigure(1, weight=0)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(1, weight=1)

    camVideoTK = Label(root, width=camGuiWidth, height=camGuiHeight)
    camVideoTK.grid(row=0, column=1, sticky=NE)

    questionTK = Label(root, text='{}'.format(questionText), relief=RAISED, bd=0, font=12, wraplength=400)
    questionTK.grid(row=1, column=1)
    questionTK.configure(bg='white')


    submitButton = Button(root, text='SUBMIT',command=lambda: releaseEverything(cap,out,root), height=3, width=20)
    submitButton.grid(row=2,column=1)
    submitButton.configure(bg='white')

    show_frame()
    root.mainloop()

    return submitButton
