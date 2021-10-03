# A class for the columns within the board
class Column:

    def __init__(self):
        self.total = 0
        self.cards = [None,None,None,None,None]
        self.aces = 0
        self.acesUsed = 0


    # Adds a card to the column
    def addCard(self, card):
        # Allows aces to be placed as either 1 or 11
        if card[0] == 'A':
            if self.total + 11 > 21:
                cardValue = 1
                self.acesUsed += 1
            else:
                cardValue = 11

        elif card[0] == 'Q' or card[0] == 'K' or (card[0] == 'J' and card[1] == 'r'):
            cardValue = 10
        
        elif card[0] == 'J' and card[1] == 'b':
            cardValue = 21 - self.total

        else:
            cardValue = card[0]
        self.total = self.total + int(cardValue)
        
        # Allows aces in a column to update from an 11 to a 1
        self.aces = self.cards.count(('A', 'b')) + self.cards.count(('A', 'r'))
        while self.total > 21 and self.aces > self.acesUsed:            
            self.total -= 10
            self.acesUsed += 1

        # Adds new card and removes a blank placeholder
        self.cards.insert(5,card)
        self.cards.pop(0)
    

    # Checks if a column is bust (>21)
    def isBust(self):
        if self.total > 21:
            self.cards = [None,None,None,None,None]
            self.total = 0
            self.acesUsed = 0
            return True
        else:
            return False


    # Checks if a full column adds to 21
    def isFull21(self):
        if len(self.cards) == 5 and not (None in self.cards) and self.total == 21:
            self.cards = [None,None,None,None,None]
            self.total = 0
            self.acesUsed = 0
            return True
        else:
            return False            


    # Checks if a cloumn adds to 21
    def is21(self):
        if self.total == 21:
            self.cards = [None,None,None,None,None]
            self.total = 0
            self.acesUsed = 0            
            return True
        else:
            return False


    # Checks if a column is full
    def isFull(self):
        if len(self.cards) == 5 and not (None in self.cards):
            self.cards = [None,None,None,None,None]
            self.total = 0
            self.acesUsed = 0
            return True
        else:
            return False



# A class for the game board
class Board:

    def __init__(self):
        self.busts = 0
        self.points = 0
        self.streak = 0
    
        self.col1 = Column()
        self.col2 = Column()
        self.col3 = Column()
        self.col4 = Column()

        self.columns = [self.col1, self.col2, self.col3, self.col4]


    # Outputs the board to the terminal
    def output(self):
        print('\n')
        print('|{}|             |{}|             |{}|             |{}|'.format(self.col1.total, self.col2.total, self.col3.total, self.col4.total))
        print('|{}|          |{}|          |{}|          |{}|'.format(self.col1.cards[0], self.col2.cards[0], self.col3.cards[0], self.col4.cards[0]))
        print('|{}|          |{}|          |{}|          |{}|'.format(self.col1.cards[1], self.col2.cards[1], self.col3.cards[1], self.col4.cards[1]))
        print('|{}|          |{}|          |{}|          |{}|'.format(self.col1.cards[2], self.col2.cards[2], self.col3.cards[2], self.col4.cards[2]))
        print('|{}|          |{}|          |{}|          |{}|'.format(self.col1.cards[3], self.col2.cards[3], self.col3.cards[3], self.col4.cards[3]))
        print('|{}|          |{}|          |{}|          |{}|'.format(self.col1.cards[4], self.col2.cards[4], self.col3.cards[4], self.col4.cards[4])) 

        print('\nBusts:', self.busts)
        print('Points:', self.points, '\n')


