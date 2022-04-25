import videoRecorder
import csv
from tkinter import *


def main():
    def destroyPage(page):
        page.destroy()

    def createPromptPage(text, buttonText):
        page = Tk()
        page.title('Raven')
        page.attributes('-fullscreen', True)
        page.iconbitmap(bitmap='content/icon.ico')
        page.geometry('500x500')
        page.grid_columnconfigure(1, weight=1)
        page.grid_rowconfigure(1, weight=1)
        page.grid_rowconfigure(0, weight=1)
        page.configure(bg='white')

        pageText = Label(page, text=text, relief=RAISED, bd=0, font=12, wraplength=400)
        pageText.grid(row=0, column=1)
        pageText.configure(bg='white')

        pageButton = Button(page, text=buttonText, command=lambda: destroyPage(page),height=3, width=20)
        pageButton.grid(row=1, column=1)
        pageButton.configure(bg='white')
        return page

    def beginQuestionnaire(introductionPage):

        count = 0

        with open('content/questions.csv', 'r') as reader:
            # pass the file object to reader() to get the reader object
            questions = csv.reader(reader)
            # Iterate over each row in the csv using reader object
            line = next(questions)
            print(line[0])
            #
            # for question in questions:
            #     # row variable is a list that represents a row in csv
            #     count += 1
            videoRecorder.videoRecorderMain('Question{}'.format(count), '{}'.format(line[0]), nextQuestionPage)
    #
    # introductionPage = Tk()
    # introductionPage.title('Raven')
    # introductionPage.attributes('-fullscreen', True)
    # introductionPage.iconbitmap(bitmap='content/icon.ico')
    # introductionPage.geometry('500x500')
    # introductionPage.grid_columnconfigure(1,weight=1)
    # introductionPage.grid_rowconfigure(1,weight=1)
    # introductionPage.grid_rowconfigure(0,weight=1)
    # introductionPage.configure(bg='white')
    #
    introString='Welcome to Project Raven!\n We will be taking your psychological evaluation using your emotional state\n\n Click ready to start'
    # introductionText = Label(introductionPage, text='{}'.format(introString), relief=RAISED, bd=0, font=12, wraplength=400)
    # introductionText.grid(row=0, column=1)
    # introductionText.configure(bg='white')

    introductionPage= createPromptPage(introString, 'READY')

    # lambda: buttonOnClick()
    # readyButton = Button(introductionPage, text='READY',command=lambda: beginQuestionnaire(introductionPage), height=3, width=20)
    # readyButton.grid(row=1,column=1)
    # readyButton.configure(bg='white')

    introductionPage.mainloop()

main()