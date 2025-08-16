import random
import numpy as np
from termcolor import colored
#from ConnectState import ConnectState
#from mcts import MCTS
"""------------------------------------------------------------------------------------
🫩 on commente tout les trucs en rapport avec monte carlo pacque flemme 🧙‍♂️"""

# Définition des couleurs pour chaque valeur
colors = {0: "blue", 1: "red", -1: "yellow"}

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RESET = '\033[0m'  # retour à la couleur standard du terminal
CYAN  = '\033[36m'

situation_alerte = False
#state = ConnectState() # inititalisation du board (en cas de montecarlo)🫩


#mcts = MCTS(state)  # activer strategie montecarlo pour le board initial🫩
# Affichage de la matrice avec les couleurs
def printColoredMatrix(matrix):
    print("--------------------")
    for ligne in matrix:
        for item in ligne:
            if item in colors:
                colored_item = colored(str(item), colors[item])
                if item >= 0:
                    print(' ' + colored_item, end=' ')
                else:
                    print(colored_item, end=' ')
        print()  # Nouvelle ligne après chaque ligne de la matrice
    print("--------------------")
    print(" 1  2  3  4  5  6  7 ")

class Player:
    def __init__(self, name, piece, color):
        self.name = name
        self.piece = piece
        self.color = color

    def get_piece(self):
        return self.piece

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

playerONE = Player("playerOne", 1, RED)
playerTWO = Player("playerTWO", -1, YELLOW)
player_bot_1 = Player("playerBot", -1, GREEN)

def creer_matrice_vide(lignes, cols):  # matrice nulle (6,7)
    #print(" 1  2  3  4  5  6  7")
    return np.zeros((lignes, cols), dtype=int)

M = creer_matrice_vide(6, 7)
printColoredMatrix(M)

def colonne(M, col):  # renvoie la colonne :col
    return M[:, col]

def position_valide(M, col):  # return True s'il y a de la place
    return M[0][col] == 0

def simuler_jeu(M, col, gamer):
    assert isinstance(col, int)
    if  position_valide(M, col):
        for ligne in range(5, -1, -1):
            if M[ligne][col] == 0:
                M[ligne][col] = gamer.get_piece()
                return M
            

def jouerLaPiece(M, col, gamer):  # bah jouer la piece
    assert isinstance(col, int)
    if not position_valide(M, col):
        print(" ----la colonne sélectionnée est remplie!!-- ")
    else:
        for ligne in range(5, -1, -1):
            if M[ligne][col] == 0:
                M[ligne][col] = gamer.get_piece()
                break

def annulerLaPiece(M, col):  # annuler le coup
    for ligne in range(6):
        if M[ligne][col] != 0:
            M[ligne][col] = 0
            break

def verification_Horizontale(M):
    for ligne in range(6):
        for col in range(4):
            if np.abs(np.sum(M[ligne, col:col + 4])) == 4:
                return True
    return False

def verification_verticale(M):
    for col in range(7):
        for ligne in range(3):
            if np.abs(np.sum(M[ligne:ligne + 4, col])) == 4:
                return True
    return False

def verification_diagonnale(M):
    for ligne in range(3):
        for col in range(4):
            if np.abs(np.sum([M[ligne + i][col + i] for i in range(4)])) == 4:   # diagonnale droite
                return True
            if np.abs(np.sum([M[ligne + 3 - i][col + i] for i in range(4)])) == 4:  # diagonnal gauche
                return True
    return False

def verification_victoire(M):
    return verification_Horizontale(M) or verification_verticale(M) or verification_diagonnale(M)

def verifierEgalite(M):
    return np.all(M != 0)

def evaluer_fenetre(fenetre, gamer):    # renvoit un compteur de score pour chaque fenetre
    score = 0
    global situation_alerte 
    if gamer == playerONE:
        adversaire = playerTWO
    else:
        adversaire = playerONE

    if fenetre.count(adversaire.get_piece()) == 3 and fenetre.count(0) == 1:
        score -= 1000
        situation_alerte = True
    elif fenetre.count(adversaire.get_piece()) == 2 and fenetre.count(0) == 2:
        score -= 300
        #situation_alerte = True
    elif fenetre.count(adversaire.get_piece()) == 4 :
        score -= 100000



    if fenetre.count(gamer.get_piece()) == 4:
        score += 10000
    elif fenetre.count(gamer.get_piece()) == 3 and fenetre.count(0) == 1:
        score += 150
    elif fenetre.count(gamer.get_piece()) == 2 and fenetre.count(0) == 2:
        score += 5

    return score

def evaluer_matrice(M, gamer):  # renvoit un compteur de toutes les fenetres dans toutes les direction
    if gamer == playerONE:
        adversaire = playerTWO
    else:
        adversaire = playerONE    
    score = 0
    # Score colonne du milieu
    colonne_du_milieu = [int(i) for i in list(M[:, 3])]
    compte_colonne_du_milieu = colonne_du_milieu.count(gamer.get_piece())
    score += compte_colonne_du_milieu * 1

    # Score horizontale
    for ligne in range(6):
        ligne_array = [int(i) for i in list(M[ligne,:])]
        for col in range(4):
            fenetre = ligne_array[col:col + 4]
            score += evaluer_fenetre(fenetre, gamer)

    # Score verticale
    for col in range(7):
        col_array = [int(i) for i in list(M[:, col])]
        for ligne in range(3):
            fenetre = col_array[ligne:ligne + 4]
            score += evaluer_fenetre(fenetre, gamer)

    # Score diagonale droite
    for ligne in range(3):
        for col in range(4):
            fenetre = [M[ligne + i][col + i] for i in range(4)]
            score += evaluer_fenetre(fenetre, gamer)

    # Score diagonale gauche
    for ligne in range(3):
        for col in range(4):
            fenetre = [M[ligne + 3 - i][col + i] for i in range(4)]
            score += evaluer_fenetre(fenetre, gamer)
    return score

def score_chaque_coup(M, gamer):   # renvoie une liste des Poids de chaque coups
    localisation_valide_array = [col for col in range(7) if position_valide(M, col)]
    scores = []
    for col in localisation_valide_array:
        jouerLaPiece(M, col, gamer)
        score = evaluer_matrice(M, gamer)
        annulerLaPiece(M, col)
        scores.append((col, score))
    return scores

def botProfondeur_1(M, gamer, scores):  # rends la colonne avec le plus de poids
    global situation_alerte 
    situation_alerte = False
    l = []
    for col, score in scores:
        assert position_valide(M, col)
        l.append(score)
    leMax = max(l)
    for col ,score in scores:  # sort la la cle du poid max 
        if score == leMax:
            return col 
 

# Fonction minimax avec élagage alpha-bêta
def minimax(M, depth, alpha, beta, maximizingPlayer, gamer):  # retourne un tuple contenant la colonne et le poid
    valid_locations = [col for col in range(7) if position_valide(M, col)]
    is_terminal = verification_victoire(M) or verifierEgalite(M)
    print("depth      ", depth)
    if depth == 0 or is_terminal:
        if is_terminal:
            if verification_victoire(M):
                if  not maximizingPlayer :
                    return None, 1000000000
                else:
                    return None , -1000000000

            else: # Match nul
                return None, 0
        else: # Profondeur atteinte
            return (None, evaluer_matrice(M, gamer))
    if maximizingPlayer:
        print("maximazing")
        value = -np.inf
        colonne = random.choice(valid_locations)
        for col in valid_locations:
            jouerLaPiece(M, col, gamer)
            nouveau_score = minimax(M, depth-1, alpha, beta, False, playerONE if gamer == playerTWO else playerTWO)[1]
            #print( " score " ,nouveau_score , "col ",col )
            annulerLaPiece(M, col)
            if nouveau_score > value:
                value = nouveau_score
                colonne = col
            alpha = max(alpha, value)
            if alpha >= beta:
                print("elagage alpha")
                break
        print("col max  ----- :" , colonne + 1 , " maxscore" , value)    
        return colonne, value
    else: # Minimizing player
        print("             minimazing")
        value = np.inf
        colonne = random.choice(valid_locations)
        for col in valid_locations:
            jouerLaPiece(M, col, gamer)
            nouveau_score = minimax(M, depth-1, alpha, beta, True, playerONE if gamer == playerTWO else playerTWO)[1]
            
            annulerLaPiece(M, col)
            if nouveau_score < value:
                value = nouveau_score
                colonne = col
            beta = min(beta, value)
            if alpha >= beta:
                print("elagage beta")
                break
        print("col min :" , colonne + 1 , "min  score" , value)
        return colonne, value

#Play en mode MonteCarlo  eh bah non  🫩
"""def play():
    while not state.game_over():
        print(np.array(state.board))
        print("Current state:")
        state.print()    #imprime l'état de la matrice

        user_move = int(input("Enter a move: "))    # input colon
        while user_move not in state.get_legal_moves():
            print("Illegal move")
            user_move = int(input("Enter a move: ")) 

        state.move(user_move)
        mcts.move(user_move)
       

        state.print()

        if state.game_over():
            print("Player one won!")
            break

        print("Thinking...")

        mcts.search(8)
        num_rollouts, run_time = mcts.statistics()
        print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
        move = mcts.best_move()

        print("MCTS chose move: ", move)

        state.move(move)
        mcts.move(move)

        if state.game_over():
            print("Player two won!")
            break
"""



def simuler_un_jeu_aleatoire(M, gamer):
    while not (verification_victoire(M) or verifierEgalite(M)):
        localisation_valide_array = [col for col in range(7) if position_valide(M, col)]
        scores = []
        for col in localisation_valide_array:
            jouerLaPiece(M, col, gamer)
            score = evaluer_matrice(M, gamer)
            annulerLaPiece(M, col)
            scores.append((col, score))
        #localisation_valide_array = [col for col in range(7) if position_valide(M, col)]
        col = botProfondeur_1(M, gamer, scores)
        #col = random.choice(localisation_valide_array)
        print("      essai col ",col)
        jouerLaPiece(M, col, gamer)
        if gamer == playerTWO:
             gamer = playerONE
        else: gamer = playerTWO
        
    if verification_victoire(M):
        if gamer == playerTWO : 
             return 1
        else : return -5#-1  
    else: return 0

def evaluer_les_coups_montecarlo(M, gamer, simulations):
    scores = {col: 0 for col in range(7) if position_valide(M, col)}
    for col in scores.keys():
        for i in range(simulations):
            print(" simulation numero " , i)
            M_copy = M.copy()    # simuler le jeu sur une matrice virtuelle sans affecter l originale
            jouerLaPiece(M_copy, col, gamer)
            scores[col] += simuler_un_jeu_aleatoire(M_copy, playerONE if gamer == playerTWO else playerTWO)
            print("----- fin de simulation noumero ", i)
            print()
    return scores

def strategie_montecarlo(M, gamer, simulations):
    scores = evaluer_les_coups_montecarlo(M, gamer, simulations)
    best_col = max(scores, key=scores.get)
    return best_col

def strategie(difficulte, M, gamer) -> int:
    if situation_alerte  == True:
        return botProfondeur_1(M, gamer, scores)
    elif difficulte.lower() == "montecarlo":
        simulations = 100 # Vous pouvez ajuster le nombre de simulations pour Monte Carlo
        return strategie_montecarlo(M, gamer, simulations)
    elif difficulte.lower() == "moyen":
        return botProfondeur_1(M, gamer, scores)
    elif difficulte.lower() == "facile":
        depth = 1
    else:
        depth = 3    
    col, minimax_score = minimax(M, depth, -np.inf, np.inf, True, gamer)
    return col


#la boucle de jeu  ------------------------------------------------------------------------------------
Game_Over = False
while True:
    try:
        joueur = int(input('Sélectionnez soit 1 pour jouez contre un bot soit 2 pour jouer 1v1 :  '))
        if joueur == 1 or joueur == 2: 
            break

        else:
            print("Sélectionnez soit 1 pour jouez contre un bot soit 2 pour jouer 1v1")
    except ValueError:
        print('1 pour un BOT ,2 pour un humain')

if joueur == 2:
    print("Vous avez choisi de jouer a deux")
else:
    print('Vous avez choisi de jouer contre le bot')
    difficulte = input("choisi un niveau Facile, Moyen, Difficile ou MonteCarlo (apart montecarlo 🫩): ").lower()
    print("vous avez choisi niveau   ", difficulte)
   
while not Game_Over:
    s = np.sum(M)
    if s == 0:
        gamer = playerONE
    elif s != 0 and joueur == 2:
        gamer = playerTWO
    elif s != 0 and joueur == 1:
        gamer = player_bot_1

    print(GREEN + "C'est le tour de", gamer.get_name() + RESET)
    scores = score_chaque_coup(M, gamer)
    print("Scores pour chaque colonne :")
    l = []
    for col, score in scores:  # sort la liste des poids avec les indice associant la colonne
        l.append(score)
        print(f"Colonne {col+1}: Poids = {score}")    
    print(l)
    leMax = max(l)
    for col ,score in scores:  # sort la la cle du poid max 
        if score == leMax:
            cleMAX = col
            break
   
    
    if joueur == 1 and gamer == player_bot_1 and difficulte.lower() != "montecarlo":
        coloneChoisie = strategie(difficulte, M, gamer)
    #plus de monte carlo fhad le code   🫩
    # la y a le elif montecarlo de baaaase mais non  🫩
    else:
        print(CYAN +f"je te conseille la colonne : {cleMAX + 1} "+ RESET)
        print(gamer.get_color() + gamer.get_name() + RESET, "choisissez une colonne entre 1 et 7: ")
        while True:
            try:
                coloneChoisie = int(input()) - 1
                if 0 <= coloneChoisie < 7 and position_valide(M, coloneChoisie):
                    break
                else:
                    print("Sélectionnez une colonne valide.")
            except ValueError:
                print('Un entier seulement, réessayez:')
    
    jouerLaPiece(M, coloneChoisie, gamer)
    
   
    printColoredMatrix(M)
    
    if verification_victoire(M):
        Game_Over = True
        print(GREEN + "Victoire de", gamer.get_name() + RESET)
    elif verifierEgalite(M):
        Game_Over = True
        print(CYAN +"Match nul!" + RESET)


  
    """
    normalement ja avant le else  🫩
    elif difficulte.lower() == "montecarlo": 
        #play() montecarlo
        while not state.game_over():
            #print(np.array(state.board))
            
            print("Current state:")
            #state.print()    #imprime l'état de la matrice
            printColoredMatrix(M)
            #user_move = int(input("Enter a move: "))    # input colon
            print(gamer.get_color() + gamer.get_name() + RESET, "choisissez une colonne entre 1 et 7: ")
            while True:
                try:
                    coloneChoisie = int(input()) - 1
                    if 0 <= coloneChoisie < 7 and position_valide(M, coloneChoisie):
                        user_move = coloneChoisie
                        break
                    else:
                        print("Sélectionnez une colonne valide.")
                except ValueError:
                    print('Un entier seulement, réessayez:')
            ''' 
            while user_move not in state.get_legal_moves():
                print("Illegal move")
                user_move = int(input("Enter a move: ")) '''
            state.move(user_move)
            mcts.move(user_move)
            jouerLaPiece(M, user_move, gamer)
            #state.print()
            printColoredMatrix(M)
            

            if state.game_over():
                print("Player one won!")
                quit()
                break

            print("Thinking...")

            mcts.search(8)
            num_rollouts, run_time = mcts.statistics()
            print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
            move = mcts.best_move()

            print("MCTS chose move: ", move+1)

            state.move(move)
            mcts.move(move)
            jouerLaPiece(M,move, player_bot_1)

            if state.game_over():
                print("Player two won!")
                quit()
                break
        """



