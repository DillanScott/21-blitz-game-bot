from game import Blitz21GameAI
from helper import plot

from gym.wrappers import FlattenObservation
	
from collections import deque
import numpy as np
import random

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import adam_v2 


# Class for the RL agent
class DQNAgent():
    
    def __init__(self, env, episodes, epsilon_decay=0.995,
                 state_size=None, action_size=None, epsilon=1.0, epsilon_min=0.01, 
                 gamma=1, alpha=0.01, alpha_decay=0.01, batch_size=16, render = False):

        # Create agent's memory
        self.memory = deque(maxlen = 100000)

        # Sets up the environment
        self.env = env

        # Sets size to be used for the input layer later
        if state_size is None:
            self.state_size = self.env.observation_space.shape[0]
        else:
            self.state_size = state_size

        # Sets size to be used for the output layer later
        if action_size is None:
            self.action_size = self.env.action_space.n
        else:
            self.action_size = action_size

        self.episodes = episodes
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.gamma = gamma
        self.alpha = alpha
        self.alpha_decay = alpha_decay
        self.batch_size = batch_size
        self.render = render


        self.model = self._build_model()


    # Build the neural net
    def _build_model(self):
        model = Sequential()
        # Creates an input layer the size of the state space and a hidden layer with 256 nodes
        model.add(Dense(256, input_dim=self.state_size, activation='relu'))
        # Creates a second hidden layer with 256 nodes
        model.add(Dense(256, activation='relu'))
        # Creates an output layer the size of the action space
        model.add(Dense(self.action_size, activation='linear'))
        # Compilation step with mean squared error as loss and Adam optimiser
        model.compile(loss='mse', optimizer=adam_v2.Adam(learning_rate=self.alpha, decay=self.alpha_decay))
        return model


    # Takes in the state and outputs a random action or the action with the highest Q-value
    # Decision depends on the epilson parameter which provides the exploration/exploitation trade-off
    def act(self, state):
        if (np.random.random() <= self.epsilon):
            return self.env.action_space.sample()
        return np.argmax(self.model.predict(state))


    # Agent uses experience replay, by training on a batch of previous data
    # This function stores said data in a deque
    def remember(self, state, action, reward, next_state, done):      
        self.memory.append((state, action, reward, next_state, done))


    # This is the replay function talked about above
    def replay(self, batch_size):
        x_batch, y_batch = [], []
        minibatch = random.sample(
            self.memory, min(len(self.memory), batch_size))
        for state, action, reward, next_state, done in minibatch:
            y_target = self.model.predict(state)
            y_target[0][action] = reward if done else reward + self.gamma * np.max(self.model.predict(next_state)[0])
            x_batch.append(state[0])
            y_batch.append(y_target[0])
            
        self.model.fit(np.array(x_batch), np.array(y_batch), batch_size=len(x_batch), verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


# Code to actaully train an agent
if __name__ == "__main__":

    # Initialize gym environment
    env = Blitz21GameAI()
    # Flattens the observation space from a Dict to a Box
    env = FlattenObservation(env)
    # Initialises the agent to play through 10000 steps
    agent = DQNAgent(env, 10000)
    agent.model.summary()

    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    

    # Iterate through games
    for e in range(agent.episodes):

        # Reset state in the beginning of each game
        state = agent.env.reset()
        state = np.reshape(state, [1, 296])
        done = False


        # done will become False when an individual game ends
        while not done:

            if agent.render:
                env.render()

            # Decide on an action
            action = agent.act(state)

            # Carry out said action and progresses the game
            next_state, reward, done, _ = agent.env.step(action)
            next_state = np.reshape(next_state, [1, 296])

            # Memorize the previous state, action, reward, and done
            agent.remember(state, action, reward, next_state, done)

            # Make next_state the new current state for the next frame.
            state = next_state


        # Print the score
        print(f"episode: {e}/{agent.episodes}, score: {agent.env.gameBoard.points}")

        # Train the agent with the experience of the episode
        agent.replay(10)

        # Plot the score on the interactive graph
        plot_scores.append(agent.env.gameBoard.points)
        total_score += agent.env.gameBoard.points
        mean_score = total_score / (e+1)
        plot_mean_scores.append(mean_score)
        plot(plot_scores, plot_mean_scores)