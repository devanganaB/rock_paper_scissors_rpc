from xmlrpc.server import SimpleXMLRPCServer

# Store choices of both players
choices = {}

def submit_choice(player, choice):
    choices[player] = choice
    if len(choices) == 2:
        return determine_winner()
    return "Waiting for the other player..."

def determine_winner():
    player1, player2 = list(choices.keys())
    choice1 = choices[player1].lower()
    choice2 = choices[player2].lower()

    if choice1 == choice2:
        result = "It's a tie!"
    elif (choice1 == "rock" and choice2 == "scissors") or \
         (choice1 == "paper" and choice2 == "rock") or \
         (choice1 == "scissors" and choice2 == "paper"):
        result = f"{player1} wins!"
    else:
        result = f"{player2} wins!"

    # Clear choices for next round
    choices.clear()
    return result

server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
print("RPS Server running on port 8000...")
server.register_function(submit_choice, "submit_choice")

server.serve_forever()
