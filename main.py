import random

moves = ['rock', 'paper', 'scissors']


class Player:  # Parent class for all players / always play "Rock"
    def __init__(self):
        self.score = 0

    def move(self):
        return "rock"

    def learn(self, my_move, their_move):
        pass

    def get_point(self):
        self.score += 1


class RandomPlayer(Player):  # Plays randomly. Subclass
    def move(self):
        return random.choice(moves)


class HumanPlayer(Player):  # Stands for user interaction. Subclass
    def move(self):
        while True:
            Responce = input("Rock, paper, scissors? - ").lower()
            if "rock" in Responce:
                return "rock"
            elif "paper" in Responce:
                return "paper"
            elif "scissors" in Responce:
                return "scissors"


class ReflectPlayer(Player):  # Copy last user action. First step -
    # - random choice. Subclass
    def __init__(self):
        super().__init__()
        self.RandomPlayer = RandomPlayer()
        self.ReflectPlayer = ReflectPlayer

    def learn(self, my_move, their_move):
        self.their_move = their_move

    def move(self):
        return self.RandomPlayer.move()

    def move_Reflect(self, move):
        return move


class CyclePlayer(Player):  # Cycle player. Subclass
    def __init__(self):
        super().__init__()
        self.CycleCounter = -1

    def move(self):
        self.CycleCounter = (self.CycleCounter + 1) % 3
        return moves[self.CycleCounter]


class NonRepetitiveRandomPlayer(Player):  # Non-repetitive, random based player
    # First step - random choice. Subclass
    def __init__(self):
        super().__init__()
        self.RandomPlayer = RandomPlayer()
        self.CyclePlayer = CyclePlayer

    def learn(self, my_move, their_move):
        self.my_move = my_move

    def move(self):
        return self.RandomPlayer.move()

    def move_cycle(self, my_move):
        cycle_list = moves
        cycle_list.remove(my_move)
        cycle_choice = random.choice(cycle_list)
        cycle_list.append(my_move)
        return cycle_choice


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def play_round(self):
        move1 = self.p1.move()
        if isinstance(self.p2, ReflectPlayer) is True:
            if self.round == 0:
                move2 = self.p2.move()
            else:
                move2 = self.p2.move_Reflect(self.p2.their_move)
        elif isinstance(self.p2, NonRepetitiveRandomPlayer) is True:
            if self.round == 0:
                move2 = self.p2.move()
            else:
                move2 = self.p2.move_cycle(self.p2.my_move)
        else:
            move2 = self.p2.move()
        self.Score_check(move1, move2)
        print(f" You play      : {move1}\n"
              f" Computer play : {move2}\n")
        print(""
              f"Score: {self.p1.score} (You) / {self.p2.score} (Computer)")
        print("_____________________________________________________________")
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

    def play_game(self):
        print(" *** Game start! *** ")
        while True:
            response = input("How many rounds would you like to play?\n"
                             "1. 3 rounds\n"
                             "2. 6 rounds\n"
                             "3. 9 rounds\n")
            if response in ["1", "2", "3"]:
                round_amount = int(response)*3
                break
            else:
                pass
        for round in range(round_amount):
            self.round = round
            print(f"Round {round}:")
            self.play_round()
        self.final_check()
        print(" *** Game over! *** ")

    def Score_check(self, move1, move2):
        if move1 != move2:
            if move1 == "rock" and move2 == "scissors":
                self.p1.get_point()
            elif move1 == "rock" and move2 == "paper":
                self.p2.get_point()
            elif move1 == "paper" and move2 == "rock":
                self.p1.get_point()
            elif move1 == "paper" and move2 == "scissors":
                self.p2.get_point()
            elif move1 == "scissors" and move2 == "paper":
                self.p1.get_point()
            elif move1 == "scissors" and move2 == "rock":
                self.p2.get_point()
        else:
            pass

    def final_check(self):
        print(f"The final score is: {self.p1.score} (You) / "
              f"{self.p2.score} (Computer)\n")
        if self.p1.score > self.p2.score:
            print("You won!\n")
        elif self.p1.score < self.p2.score:
            print("Computer won!\n")
        else:
            print("Draw game\n")


if __name__ == '__main__':
    def select_game_mode():
        while True:
            response = input("Hey there? Woud you like to play?\n"
                             "Please select the computer mode:\n"
                             "1. Rock Player mode (always plays rock)\n"
                             "2. RandomPlayer mode\n"
                             "3. ReflectPlayer mode\n"
                             "4. CyclePlayer mode\n"
                             "5. NonRepetitiveRandomPlayer mode\n"
                             "Use numbers to select the game mode\n")
            if response in ["1", "2", "3", "4", "5"]:
                break
            else:
                print("Use numbers to select game mode. Please, try again!\n")
        game_modes = [Player(), RandomPlayer(), ReflectPlayer(), CyclePlayer(),
                      NonRepetitiveRandomPlayer()]
        return game_modes[int(response)-1]

    game = Game(HumanPlayer(), select_game_mode())
    game.play_game()
