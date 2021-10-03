# 21 Blitz Game Bot

An RL agent that learns to play the game 21 Blitz.

## Issues

Currently plays the game, but doesn't learn it very well. The average score tops out at around 500-600, which a human can achieve with a few simple moves.

So, I need to tweak the neural net configuration and see if it changes the performance.


## Changes to game

~ The timer was removed, as a computer can play rounds almost instantaneously anyway

~ Doesn't output game screens unless it is set to

~ The code was reformatted to be an OpenAI Gym environment so that it can be played by an AI
