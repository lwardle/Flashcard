import pickle, datetime, random, os
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

    def markRight(self):
        self.review_flag = False
        self.last_review = datetime.datetime.now()
        if len(all_boxes) > (self.location + 1):
            self.location += 1

    def markWrong(self):
        print("We'll send that back to box one so you can practice it tomorrow.")
        self.review_flag = False
        self.last_review = datetime.datetime.now()
        self.location = 0

class Box(object):
    def __init__(self, name, review_delay):
        self.name = name
        self.review_delay = datetime.timedelta(days=review_delay)
        self.contents = None

    def assignReviewDate(self):
        pass
    
#TODO: save/load functions
def save():
    input("Are you sure? hit ctrl-c to cancel, or press enter to continue.")
    pickle_out = open("flashcard_data.pickle", "wb")
    pickle.dump(all_cards, pickle_out)
    pickle_out.close()

def load():
    global all_cards
    input("Are you sure? hit ctrl-c to cancel, or press enter to continue.")
    try:
        pickle_in = open("flashcard_data.pickle", "rb")
        all_cards = pickle.load(pickle_in)
    except:
        print("I couldn't load your cards properly. Just a guess: is there a 'flashcard_data.pickle' file in the same folder as the flashcard app? There should be.")

#TODO: button functions

def finalizeCard(card_prompt, card_response, creation_window):
    new_card = Flash_Card(card_prompt.get(), card_response.get())
    all_cards.append(new_card)
    creation_window.destroy()

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
    side_one_entry.grid(row = 0, column = 1)
    side_two_entry.grid(row = 1, column = 1)
    finalize_button.grid(row = 2, column = 0, columnspan = 2)

def deletionPopup():
    deletion_window = Toplevel()
    warning = Label(deletion_window, text = "Are you sure?")
    affirm_button = Button(deletion_window, text = "Yes", callback = None)
    cancel_button = Button(deletion_window, text = "No", callback = None)

    warning.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 10)
    affirm_button.grid(row = 1, column = 0)
    cancel_button.grid(row = 1, column = 1)

#TODO: create variables
all_boxes = []
for i in range(1, 7):
    all_boxes.append(Box(i, (2 ** (i-1)) )) #creates boxes to be reviewed every 1|2|4|8|16|32 days

all_cards = []
study_stack = []
index_card_image = PhotoImage(file = os.path.abspath(".") + "\index_card.gif")

#TODO: create GUI elements
card_front = Label(root, text = "In what year did Colombus set sail for the Americas?", wraplength = 350, font = ("Arial", 24, "bold"), image = index_card_image, compound = CENTER)
card_back = Label(root, text = "1492", wraplength = 350, font = ("Arial", 24, "bold"), image = index_card_image, compound = CENTER)
generate_stack = Button(root, text = "Generate Stack")
mark_right = Button(root, text = "Mark Correct")
mark_wrong = Button(root, text = "Mark Incorrect")
show_answer = Button(root, text = "Show Answer")
create_new_card = Button(root, text = "Create New Card", command = creationPopup)
cards_left = Label(root, text = "Number of cards left:")
total_cards = Label(root, text = "Total number of cards:")
delete_card = Button(root, text = "Delete This Card", command = deletionPopup)

#TODO: arrange GUI elements
card_front.grid(row = 0, column = 0, rowspan = 2, columnspan = 2, padx = 10, pady = 10)
card_back.grid(row = 0, column = 2, rowspan = 2, columnspan = 2, padx = 10, pady = 10)
delete_card.grid(row = 0, column = 5)
create_new_card.grid(row = 0, column = 4)
generate_stack.grid(row = 2, column = 0)
cards_left.grid(row = 1, column = 4)
show_answer.grid(row = 2, column = 1)
mark_right.grid(row = 2, column = 2)
mark_wrong.grid(row = 2, column = 3)
total_cards.grid(row = 2, column = 4)

root.mainloop()
