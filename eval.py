import random

# Global variable
global plateau, players, loosers

# Changer ses variables pour modifier le déroulement de la partie
base_money = 50  # > 0
boost = 10  # silver bonus quand les joueurs passe sur la case départ
nbr_player = 2  # Min 1 | Max 26
max_money_on_cell = 10  # 0 < ? < 100 silver bonus ou malus sur chaque case maximal
illimited_turn = True  # Définie si le jeux joue jusqu'a ce que quelqu'un soit seul avec de l'argent ou si il joue jusqu'a un nombre maximum de tour
max_turn = 10  # > 0 Nombre de tour limite quand illimited_turn est False

# Case
class Case:
    def __init__(self, cost):
        self.cost = cost

    def __str__(self):
        return str(self.cost)


# Plateau
class Plateau:
    def __init__(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.caseWidth = 5 + nbr_player
        self.Create()
        print("Le jeux commence, tout les joueurs sont placé sur la case de départ!")
        self.Show()

    def Create(self):
        self.size = (2 * self.sizeX) + (2 * self.sizeY) - 4
        self.plateau = [
            Case(random.randint(-max_money_on_cell * 2, max_money_on_cell))
            for i in range(self.size)
        ]

    def PrintValue(self, index):
        global players

        return "[%s%3s]" % (
            "".join(
                [
                    player.name if player.pos == index and not player.poor else "."
                    for player in players
                ]
            ),
            self.plateau[index],
        )

    def Show(self):
        index = 0
        backindex = 0
        for _ in range(self.sizeX):
            print(self.PrintValue(index), end="")
            index += 1
        print("")
        for _ in range(self.sizeY - 2):
            for x in range(self.sizeX):
                if x == 0:
                    print(
                        self.PrintValue(len(self.plateau) - (1 + backindex)), end="",
                    )
                elif x == self.sizeX - 1:
                    print(self.PrintValue(index), end="")
                else:
                    print(
                        "".join([" " for _ in range(self.caseWidth)]), end="",
                    )
            index += 1
            backindex += 1
            print("")
        for _ in range(self.sizeX):
            print(
                self.PrintValue(len(self.plateau) - (1 + backindex)), end="",
            )
            backindex += 1
        print("")


# Joueur
class Joueur:
    def __init__(self, name):
        self.poor = False
        self.pos = 0
        self.name = name
        self.money = base_money

    def Show(self, cost, dice1, dice2, lastPos):
        global plateau

        # Affichage des informations du tour
        print("".join(["=" for _ in range(plateau.sizeX * plateau.caseWidth)]))
        print("'%s' joue :" % self.name)
        print(
            "Il lance les dès et bouge de [%d] [%d] => %d cases"
            % (dice1, dice2, dice1 + dice2)
        )
        if lastPos > self.pos:
            print(
                f"'{self.name}' passe par la case départ, il gagne donc {boost} silver!"
            )
        plateau.Show()
        print("---")
        print(
            "En se déplaçant il tombe sur une case [%d] et %s"
            % (
                cost,
                f"gagne {cost} silver."
                if cost > 0
                else f"perd {abs(cost)} silver."
                if cost < 0
                else "ne gagne rien.",
            )
        )
        print("Joueur '%s' à désormais %s silver." % (self.name, self.money))

    def Move(self):
        global plateau, loosers

        # Le joueur se déplace
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        lastPos = self.pos
        self.pos = (self.pos + dice1 + dice2) % plateau.size

        # Si le joueur passe par la case départ il gagne un bonus
        if lastPos > self.pos:
            self.money += boost

        # Le joueur gagne / perd de l'argent
        cost = plateau.plateau[self.pos].cost
        self.money += cost
        self.Show(cost, dice1, dice2, lastPos)
        if self.money <= 0:
            self.poor = True
            print(f"'{self.name}' est à court de silver. Il quitte la partie!")
            loosers.insert(0, [self.name, self.money if not self.money < 0 else 0])
            return

        if dice1 == dice2:
            print(
                f"Wow coup de chance, '{self.name}' à fait un double [{dice1}] = [{dice2}]! il peut rejouer."
            )
            self.Move()


# Fonction d'affichage du classement de la partie
def showClassement():
    global loosers, plateau

    print("".join(["=" for _ in range(plateau.sizeX * plateau.caseWidth)]))
    print(
        f"La partie est terminé, nos {nbr_player} joueurs ce sont bien battu. Voici le classement :"
    )
    for i in range(len(loosers)):
        print(f"{i+1}: {loosers[i][0]} - {loosers[i][1]} silver")


# Main
def main():
    global plateau, players, loosers

    # Création des joueurs
    players = []
    loosers = []
    for i in range(nbr_player):
        players.append(Joueur(chr(65 + i)))

    # Création du plateau
    plateau = Plateau(10, 5)

    # Déroulement du jeu
    if illimited_turn:
        isPlaying = True
        while isPlaying:
            for player in players:
                if len(loosers) == nbr_player - 1:
                    for player in players:
                        if player.money > 0:
                            loosers.insert(0, [player.name, player.money])
                            break
                    isPlaying = False
                if not player.poor and isPlaying:
                    player.Move()
    else:
        for _ in range(max_turn):
            for player in players:
                if not player.poor:
                    player.Move()
        if len(loosers) != nbr_player:
            player_in_game = []
            for player in players:
                if not player.poor:
                    player_in_game.append([player.name, player.money])
            player_in_game.sort(key=lambda x: x[1])
            for player in player_in_game:
                loosers.insert(0, player)

    showClassement()


if __name__ == "__main__":
    main()
