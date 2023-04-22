import pygame
import math


class Graphics:
    def __init__(self):
        self.taille_case = 75
        self.oldclick=False


    def setup(self):
        #------pygame initialisation------
        pygame.init()
        pygame.display.set_caption("Chess display")

        self.window = pygame.display.set_mode((8*self.taille_case,8*self.taille_case))

        self.all_pieces_img = pygame.transform.smoothscale(pygame.image.load("chess_pieces.png").convert_alpha(),(6*self.taille_case,2*self.taille_case))

        self.piecesImages = {
            'nP': self.get_image(5,1),
            'bP': self.get_image(5,0),
            'nT': self.get_image(4,1),
            'bT': self.get_image(4,0),
            'nC': self.get_image(3,1),
            'bC': self.get_image(3,0),
            'nF': self.get_image(2,1),
            'bF': self.get_image(2,0),
            'nD': self.get_image(1,1),
            'bD': self.get_image(1,0),
            'nR': self.get_image(0,1),
            'bR': self.get_image(0,0)
        }
    

    def updateDisplay(self, echiquier, highlighted_case=None):
        self.echiquier = echiquier

        self.drawBGboard()
        
        if highlighted_case != None:
            self.draw_hilight(highlighted_case)

        self.drawPiecesPosition()
        pygame.display.update()

    #------get sprite from sprite sheet------
    def get_image(self,row,collumn):
        img = pygame.Surface((self.taille_case,self.taille_case)).convert_alpha()
        img.fill((0,0,0,0))
        img.blit(self.all_pieces_img,(0,0),(self.taille_case*row,self.taille_case*collumn,self.taille_case*(row+1),self.taille_case*(collumn+1)))
        return img

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

    #------dessin d'une piece au coordonées x y------
    def draw_piece(self, pieceCode, x, y):
        image = self.piecesImages[pieceCode]
        self.window.blit(image,(x,y))


    def drawPiecesPosition(self):
        for i in range(64):
            if self.echiquier.board[i] != '':
                self.draw_piece(self.echiquier.board[i],self.taille_case*(i%8),self.taille_case*(i//8))

#----sousligne la case selectionée----
    def draw_hilight(self, postition):
        values = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8}
        y = int(postition[1])
        x = int(values[postition[0].lower()])
        pygame.draw.rect(self.window,(255,30,120), (self.taille_case*(x-1), self.taille_case*(8-y) , self.taille_case, self.taille_case))


#------mouse on case------
    def GetMouseCase(self):
        values = {1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h'}
        pos_x, pos_y = pygame.mouse.get_pos()
        if pos_x > 0 and pos_y > 0 and pos_x < self.taille_case*8 and pos_y < self.taille_case*8:
            case_y = 9-math.ceil(pos_y/self.taille_case)
            case_x = values[math.ceil(pos_x/self.taille_case)]
            return case_x + str(case_y)

#------pygame events------
    def pygame_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click=True
                else:
                    self.click=False
        self.mouse_presses = pygame.mouse.get_pressed()
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LCTRL] and self.keys[pygame.K_q]:
            return True
        
        return False

    #---------click test------
    def clicktest(self):   # RENAME TO MOUSETRIGGER
        if self.click == False and self.oldclick == True:
             self.oldclick = self.click
             return True
        
        self.oldclick = self.click
        return False
    

    def waitALittle(self):
        pygame.time.delay(20)