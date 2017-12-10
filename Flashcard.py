import pickle, datetime, random
from tkinter import *

root = Tk()

#TODO: define classes
class Flash_Card(object):
    def __init__(self, side_1, side_2, subject):
        self.side_1 = side_1
        self.side_2 = side_2
        self.subject = subject
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

#TODO: create variables
all_boxes = []
for i in range(1, 7):
    all_boxes.append(Box(i, (2 ** (i-1)) )) #creates boxes to be reviewed every 1|2|4|8|16|32 days

all_cards = []
study_stack = []

#TODO: create GUI elements

#TODO: arrange GUI elements



root.mainloop()
