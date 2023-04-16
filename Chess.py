#------imports------
import re
import pygame
import math


#------class piece------
class Piece:
    def __init__(self, team, icon,image : pygame.Surface,type):
        self.team = team
        self.type = type
        self.image = image
        self.icon = icon
        

class Echiquier:
    def __init__(self):
        #------settings------
        self.taille_case = 75
        self.board = [ '' for i in range(64)]
        self.pieces={}
        self.turns = 0

        #------pygame initialisation------
        pygame.init()
        pygame.display.set_caption("Chess display")

        self.window = pygame.display.set_mode((8*self.taille_case,8*self.taille_case))

        self.all_pieces_img = pygame.transform.scale(pygame.image.load("chess_pieces.png").convert_alpha(),(6*self.taille_case,2*self.taille_case))

    def setup(self):
        self.initPieces()
        self.setupPiecesOrder()

    def addPiece(self,code,Piece):
        self.pieces[code] = Piece

    def initPieces(self):
        #------initialisation des pieces------
        self.addPiece('nP', Piece('n','♟ ',self.get_image(5,1), 'p'))
        self.addPiece('bP', Piece('b','♙ ',self.get_image(5,0), 'p'))
        self.addPiece('nT', Piece('n','♜ ',self.get_image(4,1), 't'))
        self.addPiece('bT', Piece('b','♖ ',self.get_image(4,0), 't'))
        self.addPiece('nC', Piece('n','♞ ',self.get_image(3,1), 'c'))
        self.addPiece('bC', Piece('b','♘ ',self.get_image(3,0), 'c'))
        self.addPiece('nF', Piece('n','♝ ',self.get_image(2,1), 'f'))
        self.addPiece('bF', Piece('b','♗ ',self.get_image(2,0), 'f'))
        self.addPiece('nD', Piece('n','♛ ',self.get_image(1,1), 'd'))
        self.addPiece('bD', Piece('b','♕ ',self.get_image(1,0), 'd'))
        self.addPiece('nR', Piece('n','♚ ',self.get_image(0,1), 'r'))
        self.addPiece('bR', Piece('b','♔ ',self.get_image(0,0), 'r'))
        
        #------initialisation de l'ordre------
        self.Norder = 'nT','nC','nF','nD','nR','nF','nC','nT'
        self.Border = 'bT','bC','bF','bD','bR','bF','bC','bT'

        #------application de l'ordre de pieces------
    def setupPiecesOrder(self):
        for i in range(8):
            self.board[i] = self.Norder[i]
            self.board[i+8+8*6]=self.Border[i]
            self.board[i+8]='nP'
            self.board[i+8+8*5]='bP'
            



    #------get sprite from sprite sheet------
    def get_image(self,row,collumn):
        img = pygame.Surface((self.taille_case,self.taille_case)).convert_alpha()
        img.fill((0,0,0,0))
        img.blit(self.all_pieces_img,(0,0),(self.taille_case*row,self.taille_case*collumn,self.taille_case*(row+1),self.taille_case*(collumn+1)))
        return img

#------requete input du coup a jouer-------
    def turn(self,status):
        if self.turns % 2 == 0:
            who_is_playing = "Whites"
        else:
            who_is_playing = "Blacks"
        if status :
            return input(who_is_playing +" turn \n")
        else:
            return input("incorrect move " +who_is_playing +" turn \n")

    
#------verification du coup------    
    def check_move(self,x): 
        reponse = re.match(r'^[a-h][1-8][a-h][1-8]$', x.lower())
        return bool(reponse)
 
#------visualisation texuelle du board------
    def showboard(self):
        for i in range(8):
            for j in range (8):
                if self.board[j+i*8] == '':
                    if ((j+i*8)%2 == 0 and i%2==0) or ((j+i*8)%2 != 0 and i%2==1):
                        print("⬜", end='')
                    else:
                        print("⬛", end='')
                else:
                    print(self.board[j+i*8].icon, end = '')
            print('\n')

        #------visualisation pygame du board------
    def drawBGboard(self):
        for i in range(64):
            white_case=(240,217,183)
            black_case=(180,136,102)
            if i%2==0 and i//8%2==0 or i%2==1 and i//8%2==1:
                case_color=white_case
            else:
                case_color=black_case
            pygame.draw.rect(self.window,case_color, (self.taille_case*(i%8), self.taille_case*(i//8) , self.taille_case, self.taille_case))

    def drawPiecesPosition(self):
        for i in range(64):
            if self.board[i] != '':
                self.draw_piece(self.board[i],self.taille_case*(i%8),self.taille_case*(i//8))

    #------dessin d'une piece au coordonées x y------
    def draw_piece(self, pieceCode,x,y):
        image = self.pieces[pieceCode].image
        self.window.blit(image,(x,y))


    #------deplacement d'une piece sur le board------ 
    def piece_move(self,played):
        values = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
        from_ = int(values[played[0].lower()])+((8-int(played[1]))*8)
        to_ = int(values[played[2].lower()])+((8-int(played[3]))*8)
        return [from_,to_]
    




#------mouse on case------
    def mouse_on_case(self):
        values = {1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h'}
        pos_x, pos_y = pygame.mouse.get_pos()
        if pos_x > 0 and pos_y > 0 and pos_x < self.taille_case*8 and pos_y < self.taille_case*8:
            case_y = 9-math.ceil(pos_y/self.taille_case)
            case_x = values[math.ceil(pos_x/self.taille_case)]
            return case_x ,case_y

#------boucle main------
def main():
    echiquier = Echiquier()
    echiquier.setup()
    




    game = True #la partie est en jeu 
    while game == True:
            pygame.time.delay(10)
            echiquier.drawBGboard()
            echiquier.drawPiecesPosition()
            #echiquier.draw_piece('nP',7,6)



            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game = False
            
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_LCTRL] and keys[pygame.K_q]:
                game = False
            
            print(echiquier.mouse_on_case())

            pygame.display.update()




            ''' window.blit(all_pieces_img,(0,0))
            showboard()
            played = turn(turns,True)
            while not check_move(played):
                played = turn(turns,False)
            turns += 1
            movement_coords = piece_move(played)
            board[movement_coords[1]]=board[movement_coords[0]]
            board[movement_coords[0]]='' '''

main()
