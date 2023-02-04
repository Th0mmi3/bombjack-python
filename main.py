from game import Game

name = None

while True:
    name = input("Player name: ")

    if len(name) > 16:
        print("Your name has to be 16 characters or less")
    else:
        break

game = Game(name)

game.run()
