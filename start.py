
from tkinter import *
import tkinter.font as tkFont
from threading import Thread
import time, random
from coord_xy_xy import Coord_XY_XY
from ennemi import Ennemi
import os

WIDTH = 450
HEIGHT = 500
FONT = "Comic Sans MS"

TAB_BG = ["#FF5733", "#33FFE6", "#3371FF", "#AF33FF", "#FF33DD", "#0CC20F", "#E21F1F"]
COLOR_BLACK = "#000000"
COLOR_WHITE = "#FFFFFF"
COLOR_YELLOW = "#FFFF00"
COLOR_RED = "#FF0000"
COLOR_GREEN = "#00FF00"

X0_CARRE = 150
Y0_CARRE = 150
X1_CARRE = X0_CARRE * 2
Y1_CARRE = Y0_CARRE * 2

SPEED = 50

class Game:
    
    def __init__(self):
        self.points = 0
        self.game_over = True
        self.id_text_game_over = None
        self.creer_fenetre()
        self.creer_canvas_game()
        self.dessiner_carre_jeu()
        self.dessiner_lignes()
        self.dessiner_boule_joueur()
        self.initialiser_cases_coin()
        self.dessiner_coin()
        self.creer_ennemis()
        self.autres_options()
    
    def creer_fenetre(self):
        self.root = Tk()
        self.w = self.root.winfo_screenwidth()
        self.h = self.root.winfo_screenheight()
        x = (self.w - WIDTH) // 2
        y = (self.h - HEIGHT) // 2
        self.root.geometry('{}x{}+{}+{}'.format(WIDTH, HEIGHT, x, y))
    
    def lancer_jeu(self):
        self.root.mainloop()

    def creer_canvas_game(self):
        self.couleur_choisi = random.randrange(len(TAB_BG))
        self.can = Canvas(self.root, width=WIDTH, height=HEIGHT-50, bg=TAB_BG[self.couleur_choisi])
        self.can.grid(row=0)
    
    def dessiner_carre_jeu(self):
        self.can.create_rectangle(X0_CARRE, Y0_CARRE, X1_CARRE, Y1_CARRE, outline=COLOR_BLACK, width=4)
    
    def dessiner_lignes(self):
        for i in range(1,3):
            space = (X0_CARRE / 3) * i
            space += X0_CARRE
            self.can.create_line(space, Y0_CARRE, space, Y1_CARRE, fill=COLOR_BLACK, width=2)
        for i in range(1,3):
            space = (Y0_CARRE / 3) * i
            space += Y0_CARRE
            self.can.create_line(X0_CARRE, space, X1_CARRE, space, fill=COLOR_BLACK, width=2)
    
    def dessiner_boule_joueur(self):
        x0 = (WIDTH/2) - 10
        y0 = x0
        x1 = x0 + 20
        y1 = x1
        self.boule_position = {'x0' : x0, 'y0' : y0, 'x1' : x1, 'y1' : y1}
        self.boule = self.can.create_oval(x0, y0, x1, y1, fill=COLOR_WHITE, outline=COLOR_WHITE)
        self.root.bind('<Key>', self.deplacer_boule)

    def deplacer_boule(self, action):
        if self.game_over:
            return

        if action.keysym == 'Down':
            self.boule_position['y0'] += SPEED
            self.boule_position['y1'] += SPEED
            if self.est_deplacable():
                self.can.move(self.boule, 0, SPEED)
            else:
                self.boule_position['y0'] -= SPEED
                self.boule_position['y1'] -= SPEED
        elif action.keysym == "Up":
            self.boule_position['y0'] -= SPEED
            self.boule_position['y1'] -= SPEED
            if self.est_deplacable():
                self.can.move(self.boule, 0, -SPEED)
            else:
                self.boule_position['y0'] += SPEED
                self.boule_position['y1'] += SPEED
        elif action.keysym == "Left":
            self.boule_position['x0'] -= SPEED
            self.boule_position['x1'] -= SPEED
            if self.est_deplacable():
                self.can.move(self.boule, -SPEED, 0)
            else:
                self.boule_position['x0'] += SPEED
                self.boule_position['x1'] += SPEED
        elif action.keysym == "Right":
            self.boule_position['x0'] += SPEED
            self.boule_position['x1'] += SPEED
            if self.est_deplacable():
                self.can.move(self.boule, SPEED, 0)
            else:
                self.boule_position['x0'] -= SPEED
                self.boule_position['x1'] -= SPEED
            
        if self.collision_coin():
            self.can.delete(self.coin)
            self.dessiner_coin()
            self.points += 1
            self.score['text'] = 'Votre Score : %i' % self.points

            self.couleur_choisi = random.randrange(len(TAB_BG))
            self.can['bg'] = TAB_BG[self.couleur_choisi]
    
    def est_deplacable(self):
        A = Coord_XY_XY(X0_CARRE, Y0_CARRE, X1_CARRE, Y1_CARRE)
        B = self.boule_position
        B = Coord_XY_XY(B['x0'], B['y0'], B['x1'], B['y1'])
        return A.in_limite(B)

    def collision_coin(self):
        A = self.boule_position
        A = Coord_XY_XY(A['x0'], A['y0'], A['x1'], A['y1'])
        B = self.coin_position
        B = Coord_XY_XY(B['x0'], B['y0'], B['x1'], B['y1'])
        return A.collision(B)
    
    def initialiser_cases_coin(self):
        self.cases_coin = [ 
            {'x0' : 170, 'y0' : 170, 'x1' : 180, 'y1' : 180}, #case 1
            {'x0' : 220, 'y0' : 170, 'x1' : 230, 'y1' : 180}, #case 2
            {'x0' : 270, 'y0' : 170, 'x1' : 280, 'y1' : 180}, #case 3
            {'x0' : 170, 'y0' : 220, 'x1' : 180, 'y1' : 230}, #case 4
            {'x0' : 220, 'y0' : 220, 'x1' : 230, 'y1' : 230}, #case 5
            {'x0' : 270, 'y0' : 220, 'x1' : 280, 'y1' : 230}, #case 6
            {'x0' : 170, 'y0' : 270, 'x1' : 180, 'y1' : 280}, #case 7
            {'x0' : 220, 'y0' : 270, 'x1' : 230, 'y1' : 280}, #case 8
            {'x0' : 270, 'y0' : 270, 'x1' : 280, 'y1' : 280}, #case 9
        ]

    def dessiner_coin(self):
        find = False
        #verifier si le coin n'est pas généré au même endroit que la boule
        while not find:
            v = random.randrange(9)
            self.coin_position = self.cases_coin[v]
            if not self.collision_coin():
                find = True
        
        x0 = self.coin_position['x0']
        y0 = self.coin_position['y0']
        x1 = self.coin_position['x1']
        y1 = self.coin_position['y1']
        self.coin = self.can.create_oval(x0, y0, x1, y1, fill=COLOR_YELLOW, outline=COLOR_YELLOW)

    def creer_ennemis(self):
        self.tab_ennemi = [
            Ennemi(-100, 170, -90, 180, 5, 0, "enemy1"),
            Ennemi(-50, 220, -40, 230, 5, 0, "enemy2"),
            Ennemi(-200, 270, -190, 280, 5, 0, "enemy3"),

            Ennemi(170, -10, 180, 0, 0, 5, "enemy4"),
            Ennemi(220, -250, 230, -240, 0, 5, "enemy5"),
            Ennemi(270, -150, 280, -140, 0, 5, "enemy6"),
        ]

        for e in self.tab_ennemi:
            e.draw(self.can)
        self.t = Thread(target=self.deplacer_ennemis)
        self.t.daemon = True
        self.t.start()

    def deplacer_ennemis(self):
        while True:
            if not self.game_over:
                for e in self.tab_ennemi:
                    a, b, c = e.moving_around(-350, -350, WIDTH + 250, HEIGHT + 250)
                    self.can.move(a, b, c)
                    self.collision_ennemi()
                time.sleep(0.035)
            

    def collision_ennemi(self):
        for e in self.tab_ennemi:
            coord_ennemi = Coord_XY_XY(e.x0, e.y0, e.x1, e.y1)
            A = self.boule_position
            coord_joueur = Coord_XY_XY(A['x0'], A['y0'], A['x1'], A['y1'])
            if coord_ennemi.collision(coord_joueur):
                self.game_over = True
                self.enregistrer_meilleur_score(self.points)

    def autres_options(self):
        c = Frame(self.root)
        c.grid(row=1)
        self.bouton_jouer = Button(c,text="Jouer", command=self.start)
        self.bouton_jouer.grid(row=1,column=0, pady=10, padx=10)
        self.meilleur_score = Label(c, text='Meilleur Score : %i' % self.get_meilleur_score()) 
        self.meilleur_score.grid(row=1, column=1, pady=10, padx=10)
        self.score = Label(c, text='Votre Score : 0')
        self.score.grid(row=1, column=2, pady=10)
        Button(c,text="Quitter",command=self.root.destroy).grid(row=1,column=3,pady=10, padx=10)

    def start(self):
        self.game_over = False
        self.points = 0
        self.meilleur_score['text'] = 'Meilleur Score : %i' % self.get_meilleur_score()
        self.score['text'] = 'Votre Score : %i' % self.points
        print(self.can.delete(self.id_text_game_over))
        self.bouton_jouer['text'] = "Recommencer"
        self.init_ennemis()
    
    def afficher_texte(self, texte):
        self.id_text_game_over = self.can.create_text(WIDTH//2,30,text=texte, fill=COLOR_BLACK, activefill=COLOR_YELLOW, justify="center")
        

    def init_ennemis(self):
        for e in self.tab_ennemi:
            if e.speedx != 0:
                a = - (e.x0 - e.x_origin0)
                b = 0
                c = e.tag
                self.can.move(c, a, b)
                e.retour_origin()
                e.speedx = 5
            else:
                a = 0
                b = - (e.y0 - e.y_origin0)
                c = e.tag
                self.can.move(c, a, b)
                e.retour_origin()
                e.speedy = 5
    
    def get_meilleur_score(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path_file = os.path.join(dir_path, 'score.txt')
        score = 0
        with open(path_file, 'r') as f:
            content = f.readlines()
            score = int(content[0])
        return score
    
    def enregistrer_meilleur_score(self, new_meilleur_score):
        if self.get_meilleur_score() < new_meilleur_score:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            path_file = os.path.join(dir_path, 'score.txt')
            score = 0
            with open(path_file, 'w') as f:
                f.write(str(new_meilleur_score))
            

if __name__ == '__main__':   
    
    g = Game()
    g.lancer_jeu()
    


