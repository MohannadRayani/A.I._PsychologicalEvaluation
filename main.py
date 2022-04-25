import videoRecorder
import videoAnalyzer
import csv
from tkinter import *
import time

emotionalValues = {'Positive': 0, 'Negative': 0}
count = 0

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
    return page, pageButton, pageText

def introductionPageButton(introductionPage, questions):
    global count
    question = next(questions)[0]
    recordVideoQuestion(count,question, introductionPage)
    destroyPage(introductionPage)
    count = count + 1
    nextQuestionPageText = 'Thank you for your Submission!\n We understand that the evaluation may be demanding\n\n Please take a minute to rest'
    nextQuestionPage, nextQuestionButton, nextQuestionText = createPromptPage(nextQuestionPageText, 'CONTINUE')
    nextQuestionButton.configure(command =lambda: nextQuestionPageButton(nextQuestionPage, questions))
    nextQuestionPage.mainloop()

def nextQuestionPageButton(nextQuestionPage, questions):
    global count
    try:
        question = next(questions)[0]

    except StopIteration:
        destroyPage(nextQuestionPage)
        finalPage(count, None)
        return

    recordVideoQuestion(count, question, nextQuestionPage)
    destroyPage(nextQuestionPage)
    count = count + 1
    nextQuestionPageText = 'Thank you for your Submission!\n We understand that the evaluation may be demanding\n\n Please take a minute to rest'
    nextQuestionPage, nextQuestionButton, nextQuestionText = createPromptPage(nextQuestionPageText, 'CONTINUE')
    nextQuestionButton.configure(command =lambda: nextQuestionPageButton(nextQuestionPage, questions))

def recordVideoQuestion(questionID, questionPage, page):
    videoRecorder.videoRecorderMain(questionID, questionPage, page)


def finalPage(count, page):
    global emotionalValues
    if page != None:
        destroyPage(page)

    if count != 0:
        loadingPage, loadingPageButton, loadingPageText = createPromptPage('\n\n Please wait while we load your video', 'Waiting')
        loadingPageButton.destroy()
        loadingPage.update()

        videoEmotion, validity = videoAnalyzer.videoAnalyzerMain(count)
        loadingPage.destroy()

        scanPage, scanButton, scanText = createPromptPage(
            '\n\n Your results for question {} are {}\n\n Most Prominent Emotion: {}\n\n Demonstration Complete, Scan next video?'.format(
                count, validity, videoEmotion), 'SCAN')
        count-=1
        scanButton.configure(command = lambda: finalPage(count, scanPage))
        if validity == 'Negative':
            emotionalValues['Negative']+=1
        elif validity == 'Positive':
            emotionalValues['Positive']+=1
    elif count == 0:
        resultPage()

def resultPage():
    resultPage, resultPageButton, resultPageText = createPromptPage('\n\n Your Psychological Evaluation Final Result: ', 'Waiting')
    resultPageButton.destroy()
    resultPass = Label(resultPage, text='PASS', width=100, height=20, bg='#7cfe00', font=20)
    resultFail = Label(resultPage, text='FAIL', width=100, height=20, bg='#fe1100', font=20)
    if emotionalValues['Positive']  >= emotionalValues['Negative']:
        resultPass.grid(row=1, column=1)
        resultPage.update()
        time.sleep(7)
        resultPage.destroy()
    else:
        resultFail.grid(row=1, column=1)
        resultPage.update()
        time.sleep(7)
        resultPage.destroy()

def main():
    count = 1
    with open('content/questions.csv', 'r') as reader:

        questions = csv.reader(reader)

        introductionPageText='Welcome to Project Raven!\n We will be taking your psychological evaluation using your emotional state\n\n Click ready to start'
        introductionPage, button, text = createPromptPage(introductionPageText, 'READY')
        button.configure(command= lambda: introductionPageButton(introductionPage, questions))

        introductionPage.mainloop()

main()