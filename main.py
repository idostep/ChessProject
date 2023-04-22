from chess import Echiquier
from graphicsPyGame import Graphics

import chess 

#------boucle main------
def main():
    echiquier = Echiquier()
    echiquier.setup()
    echiquier.game = True #la partie est en jeu

    state = 'INIT'

    g = Graphics()
    g.setup()

    g.updateDisplay(echiquier)
    quitGame = False

    while not quitGame:
            quitGame = g.pygame_events()

            match state:
                case 'INIT':
                    if g.clicktest():
                        coordCase1 =  g.GetMouseCase()
                        piece = echiquier.getPieceOnCoord(coordCase1)
                        if piece != None and piece.team == echiquier.WhoseTurn():
                            g.updateDisplay(echiquier, coordCase1)
                            highlighted_case = None
                            state = 'ONECLICK'
                        
                case 'ONECLICK':
                    if g.clicktest():
                        coordCase2 =  g.GetMouseCase()
                        if echiquier.TestValidMove(coordCase1+coordCase2):
                            echiquier.move_piece(echiquier.translate_moves(coordCase1 + coordCase2))
                            g.updateDisplay(echiquier)
                            state = 'INIT'

            """ 
            if echiquier.clicktest():
                if echiquier.selected_case==None: #selection de la case 1 
                    x,y=echiquier.translate_move(echiquier.mouse_on_case())
                    if echiquier.board[x+y*8] != '':
                        echiquier.selected_case = echiquier.mouse_on_case()
                        case1color = echiquier.pieces[echiquier.board[x+y*8]].team
                elif  echiquier.selected_case == echiquier.mouse_on_case(): #selection d'une case deja selectionnée click n°2
                    echiquier.selected_case = None
                else: #deplacement click n°2
                    x,y=echiquier.translate_move(echiquier.mouse_on_case())
                    if echiquier.board[x+y*8] == "":
                        echiquier.move_piece(echiquier.translate_moves(echiquier.selected_case + echiquier.mouse_on_case()))
                        echiquier.selected_case = None
                    elif case1color != echiquier.pieces[echiquier.board[x+y*8]].team:
                        echiquier.move_piece(echiquier.translate_moves(echiquier.selected_case + echiquier.mouse_on_case()))
                        echiquier.selected_case = None
                    
             """
            g.waitALittle()


main()