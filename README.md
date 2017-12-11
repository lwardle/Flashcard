# Flashcard
A simple python 3.6.3 flashcard manager

Author: Lawrence Wardle

This is a small first project for the purpose of:
  1) Practicing relatively simple python code
  2) Creating a useful educational tool

The program will allow users to create, label, and save/load flashcards that persist between sessions. Individual cards will be automatically marked for review at specific times, described in more detail below. The cards will be displayed front side (question/prompt) first, then both sides, then manually marked correct/incorrect. The cards will be saved via the pickle module, and the interface will be designed with tKinter.

The educational value of this simple program is in the way it manages the flashcards, based on the Leitner system. In the Leitner system of flashcards, cards are kept in a series of boxes. Each box carries a progressively increasing review delay, e.g. the first box is reviewed every day, the second box every other day, the third box once a week, etc. If a card is marked correct, it progresses to a box of less frequent review. A card marked incorrect will be sent back to the first box. Through this method, the user reviews everything regularly, but spends the vast majority of their time working on the items that actually need work. Also, there are thought to be benefits to reviewing material just before it is forgotten (as opposed to when the material is still remembered clearly, or after forgetting it). The incremental spacing of repetition may serve as another benefit of using this system of flashcard management.

This program will be a small improvement over the Leitner system. The Leitner system reviews whole boxes at a time out of necessity; it is a system designed for physical flashcards. This program can iterate over flashcards individually, marking them for review based on the time they entered their current box.

Additional features to put in later:

  Ability to tag cards and ability to sort by tag
  
  Statistics about individual flashcards and overall performance
  
  Allow image/sound input for flashcards
  
  Allow for multi-sided flashcards
  
  Allow for reversible flashcards
  
  Nicer GUI and animated graphics
  
  Make into a mobile app
