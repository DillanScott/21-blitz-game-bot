from typing import Dict
from board import Board
import random
import numpy as np

import gym
from gym import spaces


class Blitz21GameAI(gym.Env):
    metadata = {'render.modes': ['console']}

    def __init__(self):
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Dict({
                    'cardValue': spaces.Box(np.array([1]), np.array([12]), dtype = int),    
                    'carColour': spaces.Discrete(2),           
                    'c1Total': spaces.Discrete(30),          
                    'c2Total': spaces.Discrete(30),          
                    'c3Total': spaces.Discrete(30),         
                    'c4Total': spaces.Discrete(30),         
                    'streak': spaces.Discrete(53),
                    'busts': spaces.Discrete(4),
                    'cardsLeft': spaces.Discrete(53),       
                    'aces': spaces.Discrete(5),
                    'twos': spaces.Discrete(5),
                    'threes': spaces.Discrete(5),
                    'fours': spaces.Discrete(5),
                    'fives': spaces.Discrete(5),
                    'sixes': spaces.Discrete(5),
                    'sevens': spaces.Discrete(5),
                    'eights': spaces.Discrete(5),
                    'nines': spaces.Discrete(5),
                    'tens': spaces.Discrete(15),
                    'blackjacks': spaces.Discrete(3)})


        self.colours = ['r', 'r', 'b', 'b']
        self.reset()



    def reset(self):
        self.gameOver = False
        self.deck = []
        
        for colour in self.colours:
            self.deck.append(('A', colour))   
            
            for value in range(2, 11):
                self.deck.append((value,colour))
            
            self.deck.append(('J', colour))
            self.deck.append(('Q', colour))
            self.deck.append(('K', colour))

        
        # Shuffles the deck of cards
        self.shuffledDeck = self.deck
        random.shuffle(self.shuffledDeck)
        self.topCard = self.shuffledDeck[0]

        # Instantiates the Board class, outputs it for the 1st time and starts the 3min timer
        self.gameBoard = Board()
        
        return self.get_obs()



    def step(self, action):
        reward = 0
        self.topCard = self.shuffledDeck[0]
        # print(self.topCard)

        chosenColumn = action

        bust = None
        if chosenColumn == 0:
            self.gameBoard.col1.addCard(self.topCard)
            bust = self.check_column(self.gameBoard.col1)

        elif chosenColumn == 1:
            self.gameBoard.col2.addCard(self.topCard)
            bust = self.check_column(self.gameBoard.col2)

        elif chosenColumn == 2:
            self.gameBoard.col3.addCard(self.topCard)
            bust = self.check_column(self.gameBoard.col3)

        elif chosenColumn == 3:
            self.gameBoard.col4.addCard(self.topCard)
            bust = self.check_column(self.gameBoard.col4)

        self.shuffledDeck.pop(0)

        if self.gameBoard.streak > 0:
            streakReward = 50 * (2**(self.gameBoard.streak-1))
            columnReward = 50
        else:
            streakReward = 0
            columnReward = 0
        if bust == True:
            bustReward = -100
        else:
            bustReward = 0

        reward = self.gameBoard.points + streakReward + columnReward + bustReward

        for column in self.gameBoard.columns:
            if column.total == 11:
                reward += 25
            if column.total > 11 and column.total != 21:
                reward -= 10
            elif column.total > 15 and column.total != 21:
                reward -= 25

        info = {}
        # self.gameBoard.output()

        if self.gameBoard.busts >= 3:
            self.gameOver = True
            reward = -200
        
        if len(self.shuffledDeck) <= 0:
            self.gameOver = True
            reward = 200

        return self.get_obs(), reward, self.gameOver, info
        


    def render(self, mode = 'console'):
        if mode != 'console':
            raise NotImplementedError()

        print(self.topCard)
        self.gameBoard.output()



    def close(self):
        pass



    def get_obs(self):
        if self.topCard[0] == 'A':
            topCardValue = 11
        elif type(self.topCard[0]) == str:
            topCardValue = 10
        else:
            topCardValue = self.topCard[0]
        
        if self.topCard[1] == 'b':
            topCardColour = 1
        else:
            topCardColour = 0

        observation = {'cardValue': np.array([topCardValue]), 
                       'carColour': topCardColour,
                       'c1Total': self.gameBoard.col1.total, 
                       'c2Total': self.gameBoard.col2.total, 
                       'c3Total': self.gameBoard.col3.total, 
                       'c4Total': self.gameBoard.col4.total,
                       'streak': self.gameBoard.streak,
                       'busts': self.gameBoard.busts,
                       'cardsLeft': len(self.shuffledDeck),
                       'aces': sum(1 for card in self.shuffledDeck if card[0] == 'A'),
                       'twos': sum(1 for card in self.shuffledDeck if card[0] == 2),
                       'threes': sum(1 for card in self.shuffledDeck if card[0] == 3),
                       'fours': sum(1 for card in self.shuffledDeck if card[0] == 4),
                       'fives': sum(1 for card in self.shuffledDeck if card[0] == 5),
                       'sixes': sum(1 for card in self.shuffledDeck if card[0] == 6),
                       'sevens': sum(1 for card in self.shuffledDeck if card[0] == 7),
                       'eights': sum(1 for card in self.shuffledDeck if card[0] == 8),
                       'nines': sum(1 for card in self.shuffledDeck if card[0] == 9),
                       'tens': sum(1 for card in self.shuffledDeck if card[0] == 10 or card[0] == 'Q' or card[0] == 'K' or card == ('J', 'r')),
                       'blackjacks': sum(1 for card in self.shuffledDeck if card == ('J', 'b'))}
        
        return observation



    def check_column(self,column):
        if column.cards[4] == ('J', 'b'):
            self.gameBoard.points += 200
            self.gameBoard.streak += 1
            column.cards = [None,None,None,None,None]
            column.total = 0
            column.acesUsed = 0

        elif column.isBust():
            self.gameBoard.busts += 1
            if self.gameBoard.streak > 0:
                self.gameBoard.points += (125 * (self.gameBoard.streak - 1) ** 2 + 125 * (self.gameBoard.streak - 1))
            self.gameBoard.streak = 0
            return True

        elif column.isFull21():
            self.gameBoard.points += 1000
            self.gameBoard.streak += 1

        elif column.is21():
            self.gameBoard.points += 400
            self.gameBoard.streak += 1

        elif column.isFull():
            self.gameBoard.points += 600
            self.gameBoard.streak += 1

        elif self.gameBoard.streak > 0:
            self.gameBoard.points += (125 * (self.gameBoard.streak - 1) ** 2 + 125 * (self.gameBoard.streak - 1))
            self.gameBoard.streak = 0
        else:
            pass  



#from stable_baselines3.common.env_checker import check_env



env = Blitz21GameAI()

#check_env(env)

