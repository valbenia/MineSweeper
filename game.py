#  keo - bua - bao
# 1. User input
# 2. Random choice
# 3. Compare
# 4. Score

import random
plays = ['rock', 'paper', 'scissors']
while True:
    userInput = input("Enter choice: ")
    if userInput in plays:
        break

autoInput = random.choice(plays)



# def compare(userInput, autoInput):
#     if userInput == autoInput:
#         return 'Draw!'
#     elif (userInput == 'rock' and autoInput == 'scissors') or (userInput == 'scissors' and autoInput == 'paper') or (userInput == 'paper' and autoInput == 'rock'):
#         return 'You win!'
#     else:
#         return 'You lose!'

# def compare(userInput, autoInput):
#     ruleMatrix = {'rock':-1, 'paper':0, 'scissors':1}
#     if userInput == autoInput:
#         return 'Draw!'
#     if ((userInput == 'rock' and autoInput == 'scissors') 
#         or (userInput == 'scissors' and autoInput == 'paper') 
#         or (userInput == 'paper' and autoInput == 'rock')):
#         return 'You win!'
#     else:
#         return 'You lose!'
def compare(userInput, autoInput):
    ruleMatrix = {'rock':-1, 'paper':0, 'scissors':1}
    decision = ruleMatrix[userInput] - ruleMatrix[autoInput]
    
    if decision == 0:
        return 'Draw!'
    elif decision == 1 or decision == -2:
        return 'You win!'
    else:
        return 'You lose!'


print(f"AI's pick: {autoInput}")
print(compare(userInput, autoInput))



