#------imports------
import re
import pygame

#------settings------
taille_case = 100
board = [ '' for i in range(64)]

#------pygame initialisation------
pygame.init()
pygame.display.set_caption("Chess display")
window = pygame.display.set_mode((8*taille_case,8*taille_case))
all_pieces_img = pygame.transform.scale(pygame.image.load("chess_pieces.png").convert_alpha(),(6*taille_case,2*taille_case))



#------get sprite from sprite sheet------
def get_image(row,collumn):
    img = pygame.Surface((taille_case,taille_case)).convert_alpha()
    img.fill((0,0,0,0))
    img.blit(all_pieces_img,(0,0),(taille_case*row,taille_case*collumn,taille_case*(row+1),taille_case*(collumn+1)))
    return img

#------class piece------
class piece:
    def __init__(self, team, icon,image,type):
        self.team = team
        self.type = type
        self.image = image
        self.icon = icon
        
#------initialisation des pieces------
nP = piece('n','♟ ',get_image(5,0), 'p')
bP = piece('b','♙ ',get_image(5,1), 'p')
nT = piece('n','♜ ',get_image(4,0), 't')
bT = piece('b','♖ ',get_image(4,1), 't')
nC = piece('n','♞ ',get_image(3,0), 'c')
bC = piece('b','♘ ',get_image(3,1), 'c')
nF = piece('n','♝ ',get_image(2,0), 'f')
bF = piece('b','♗ ',get_image(2,1), 'f')
nD = piece('n','♛ ',get_image(1,0), 'd')
bD = piece('b','♕ ',get_image(1,1), 'd')
nR = piece('n','♚ ',get_image(0,0), 'r')
bR = piece('b','♔ ',get_image(0,1), 'r')

#------initialisation de l'ordre------
Norder = nT,nC,nF,nD,nR,nF,nF,nC,nT
Border = bT,bC,bF,bD,bR,bF,bF,bC,bT

#------application de l'ordre de pieces------
def setup():
    for i in range(8):
        board[i] = Norder[i]
        board[i+8]=nP
        board[i+8+8*5]=bP
        board[i+8+8*6]=Border[i]
setup()




#------requete input du coup a jouer-------
def turn(turns,status):
    if turns % 2 == 0:
        who_is_playing = "Whites"
    else:
        who_is_playing = "Blacks"
    if status :
        return input(who_is_playing +" turn \n")
    else:
        return input("incorrect move " +who_is_playing +" turn \n")

    
#------verification du coup------    
def check_move(x): 
     reponse = re.match(r'^[a-h][1-8][a-h][1-8]$', x.lower())
     return bool(reponse)
 


#------deplacement d'une piece sur le board------ 
def piece_move(played):
    values = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    from_ = int(values[played[0].lower()])+((8-int(played[1]))*8)
    to_ = int(values[played[2].lower()])+((8-int(played[3]))*8)
    return [from_,to_]
    

#------visualisation texuelle du board------
def showboard():
    for i in range(8):
        for j in range (8):
            if board[j+i*8] == '':
                if ((j+i*8)%2 == 0 and i%2==0) or ((j+i*8)%2 != 0 and i%2==1):
                    print("⬜", end='')
                else:
                    print("⬛", end='')
            else:
                print(board[j+i*8].icon, end = '')
        print('\n')

#------visualisation pygame du board------
def drawboard():
    for i in range(64):
        white_case=(240,217,183)
        black_case=(180,136,102)
        if i%2==0 and i//8%2==0 or i%2==1 and i//8%2==1:
            case_color=white_case
        else:
            case_color=black_case
        pygame.draw.rect(window,case_color, (taille_case*(i%8), taille_case*(i//8) , taille_case, taille_case))

#------dessin d'une piece au coordonées x y------
def draw_piece(piece,x,y):
    window.blit(piece.image,(x*100,y*100))
    

#------boucle main------
def main():
    game = True #la partie est en jeu
    turns = 0 


    while game == True:
            pygame.time.delay(10)
            drawboard()



            
            
            draw_case = 0
            for i in board:
                if i != '':
                    draw_piece(i,draw_case%8,draw_case//8)
                draw_case += 1
            #window.blit(bC.image,(0,0))


            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game = False
            
            keys = pygame.key.get_pressed()

            

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
