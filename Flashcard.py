import pickle, datetime, random, os, csv
from tkinter import filedialog
from tkinter import *

root = Tk()

#TODO: define classes
class Flash_Card(object):
    def __init__(self, side_1, side_2):
        self.side_1 = side_1
        self.side_2 = side_2
        self.location = 0 #refers to index location of current box within all_boxes
        self.review_flag = True #cards are created with the last review set as the date of creation, but the review flag on.
        self.last_review = datetime.datetime.now()
    
class Box(object):
    def __init__(self, name, review_delay):
        self.name = name
        self.review_delay = datetime.timedelta(days=review_delay)

    def assignReviewDate(self):
        pass
    
#TODO: save/load functions
def saveFunction():
    pickle_out = open(filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("PICKLE files","*.pickle"),("all files","*.*"))), "wb")
    pickle.dump(all_cards, pickle_out)
    pickle_out.close()

def loadPrompt():
    load_window = Toplevel()
    warning = Label(load_window, text = "Are you sure you want to load?\nThis will discard the current data.")
    affirm_button = Button(load_window, text = "Yes", command = lambda: loadFunction(load_window))
    cancel_button = Button(load_window, text = "No", command = lambda: load_window.destroy())

    warning.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 10)
    affirm_button.grid(row = 1, column = 0)
    cancel_button.grid(row = 1, column = 1)

def loadFunction(load_window):
    global all_cards
    pickle_in = open(filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("PICKLE files","*.pickle"),("all files","*.*"))), "rb")
    all_cards = pickle.load(pickle_in)
    generateStack()
    cards_left_count.set(len(study_stack))
    cards_total_count.set(len(all_cards))

#TODO: button functions
def markCorrect():
    if len(study_stack) == 0:
        return
    study_stack[0].review_flag = False
    study_stack[0].location += 1
    card_back.config(text = "")
    study_stack[0].last_review = datetime.datetime.now()
    study_stack.remove(study_stack[0])
    cards_left_count.set(len(study_stack))
    if len(study_stack) == 0:
        card_back.config(text = "Don't forget to save!")
        card_front.config(text = "Congrats! You're done for today!")
        return
    new_prompt = study_stack[0].side_1
    card_front.config(text = new_prompt)

def markIncorrect():
    if len(study_stack) == 0:
        return
    study_stack[0].location = 0
    card_back.config(text = "")
    study_stack[0].last_review = datetime.datetime.now()
    study_stack.remove(study_stack[0])
    cards_left_count.set(len(study_stack))
    if len(study_stack) == 0:
        card_back.config(text = "Don't forget to save!")
        card_front.config(text = "Congrats! You're done for today!")
        return
    new_prompt = study_stack[0].side_1
    card_front.config(text = new_prompt)

def showAnswer():
    if len(study_stack) == 0:
        return
    new_text = study_stack[0].side_2
    card_back.config(text = new_text)

def setReviewFlags():
    for card in all_cards:
        review_delay = all_boxes[card.location].review_delay
        last_review = card.last_review
        if last_review + review_delay < datetime.datetime.now():
            card.review_flag = True

def deleteCard(window, card):
    all_cards.remove(card)
    study_stack.remove(card)
    cards_left_count.set(len(study_stack))
    cards_total_count.set(len(all_cards))
    window.destroy()
    card_back.config(text = "")
    if len(study_stack) == 0:
        card_front.config(text = "Congrats! You're done for today!")
        card_back.config(text = "Don't forget to save!")
        return
    else:
        new_prompt = study_stack[0].side_1
        card_front.config(text = new_prompt)
        return

def generateStack():
    global study_stack
    setReviewFlags()
    for card in all_cards:
        if card.review_flag == True:
            study_stack.append(card)
    random.shuffle(study_stack)
    if len(study_stack) == 0:
        card_front.config(text = "Congrats! You're done for today!")
        card_back.config(text = "Don't forget to save!")
        return
    else:
        new_prompt = study_stack[0].side_1
        card_front.config(text = new_prompt)

def flipStack():
    for card in all_cards:
        old_front = card.side_1
        old_back = card.side_2
        card.side_1 = old_back
        card.side_2 = old_front
    card_front.config(text = study_stack[0].side_1)

def finalizeCard(card_prompt, card_response, creation_window):
    new_card = Flash_Card(card_prompt.get(), card_response.get())
    all_cards.append(new_card)
    creation_window.destroy()
    cards_total_count.set(len(all_cards))

def creationPopup():
    creation_window = Toplevel()
    side_one_prompt = Label(creation_window, text = "Prompt: ")
    side_two_prompt = Label(creation_window, text = "Response: ")
    card_prompt = StringVar()
    card_response = StringVar()
    side_one_entry = Entry(creation_window, textvariable = card_prompt)
    side_two_entry = Entry(creation_window, textvariable = card_response)
    finalize_button = Button(creation_window, text = "Finalize Card", command = lambda: finalizeCard(card_prompt, card_response, creation_window))

    side_one_prompt.grid(row = 0, column = 0)
    side_two_prompt.grid(row = 1, column = 0)
    side_one_entry.grid(row = 0, column = 1, columnspan = 3)
    side_two_entry.grid(row = 1, column = 1, columnspan = 3)
    finalize_button.grid(row = 2, column = 0, columnspan = 2)

def deletionPopup():
    deletion_window = Toplevel()
    warning = Label(deletion_window, text = "Are you sure?")
    affirm_button = Button(deletion_window, text = "Yes", command = lambda: deleteCard(deletion_window, study_stack[0]))
    cancel_button = Button(deletion_window, text = "No", command = lambda: deletion_window.destroy())

    warning.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 10)
    affirm_button.grid(row = 1, column = 0)
    cancel_button.grid(row = 1, column = 1)

def importCards():
    incoming_cards_file = open(filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("TEXT files","*.txt"),("all files","*.*"))))
    incoming_cards_reader = csv.reader(incoming_cards_file)
    incoming_card_data = []
    for row in incoming_cards_reader:
        incoming_card_data.append(row)
    for card in incoming_card_data:
        all_cards.append(Flash_Card(card[0], card[1]))
    generateStack()
    cards_left_count.set(len(study_stack))
    cards_total_count.set(len(all_cards))
    
def exportCards():
    outputFile = open(filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("TEXT files","*.txt"),("all files","*.*"))), 'w', newline='')
    card_data = []
    for card in all_cards:
        card_data.append([card.side_1, card.side_2])
    outputWriter = csv.writer(outputFile)
    for card in card_data:
        outputWriter.writerow(card)
    outputFile.close()

#TODO: create variables

all_boxes = []

for i in range(1, 7):
    all_boxes.append(Box(i, (2 ** (i-1)) )) #creates boxes to be reviewed every 1|2|4|8|16|32 days

all_cards = []
study_stack = []
try:
    index_card_image = PhotoImage(file = "index_card.gif")
except:
    image_failure_prompt = Toplevel()
    warning = Label(image_failure_prompt, text = "I couldn't find index_card.gif. Could you please find it for me?")
    warning.pack()
    index_card_image = PhotoImage(file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("GIF files","*.gif"),("all files","*.*"))))
    image_failure_prompt.destroy()

cards_left_count = IntVar()
cards_left_count.set(len(study_stack))
cards_total_count = IntVar()
cards_total_count.set(len(all_cards))

#TODO: create GUI elements
card_front = Label(root, text = "", wraplength = 350, font = ("Arial", 24, "bold"), image = index_card_image, compound = CENTER)
card_back = Label(root, text = "", wraplength = 350, font = ("Arial", 24, "bold"), image = index_card_image, compound = CENTER)
mark_right = Button(root, text = "Mark Correct", command = markCorrect)
mark_wrong = Button(root, text = "Mark Incorrect", command = markIncorrect)
show_answer = Button(root, text = "Show Answer", command = showAnswer)
flip_stack = Button(root, text = "Flip Stack", command = flipStack)
create_new_card = Button(root, text = "Create New Card", command = creationPopup)
cards_left = Label(root, text = "Number of cards left:")
total_cards = Label(root, text = "Total number of cards:")
cards_left_counter = Label(root, textvariable = cards_left_count)
total_cards_counter = Label(root, textvariable = cards_total_count)
delete_card = Button(root, text = "Delete This Card", command = deletionPopup)
save_button = Button(root, text = "Save", command = saveFunction)
load_button = Button(root, text = "Load", command = loadPrompt)
import_cards = Button(root, text = "Import Cards From .TXT File", command = importCards)
export_cards = Button(root, text = "Export Cards To .TXT File", command = exportCards)

#TODO: arrange GUI elements
card_front.grid(row = 0, column = 0, rowspan = 6)
card_back.grid(row = 0, column = 1, rowspan = 6)
delete_card.grid(row = 4, column = 3)
create_new_card.grid(row = 4, column = 2)
cards_left.grid(row = 2, column = 2)
show_answer.grid(row = 0, column = 2)
flip_stack.grid(row = 0, column = 3)
cards_left_counter.grid(row = 2, column = 3)
total_cards_counter.grid(row = 3, column = 3)
mark_right.grid(row = 1, column = 2)
mark_wrong.grid(row = 1, column = 3)
total_cards.grid(row = 3, column = 2)
save_button.grid(row = 5, column = 2)
load_button.grid(row = 5, column = 3)
export_cards.grid(row = 6, column = 2)
import_cards.grid(row = 6, column = 3)

root.mainloop()
