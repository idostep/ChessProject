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
                            state = 'ONECLICK'
                        
                case 'ONECLICK':
                    if g.clicktest():
                        coordCase2 =  g.GetMouseCase()                        
                        if coordCase1 == coordCase2:
                            # select same case
                            coordCase1 = None
                            state = 'INIT'
                            g.updateDisplay(echiquier)
                        elif echiquier.getPieceOnCoord(coordCase2) != None and echiquier.getPieceOnCoord(coordCase2).team == echiquier.WhoseTurn():
                            #select another piece
                            coordCase1 = coordCase2
                            coordCase2 = None
                            g.updateDisplay(echiquier, coordCase1)
                        elif echiquier.TestValidMove(coordCase1+coordCase2):
                            #selct movement
                            echiquier.move_piece(echiquier.translate_moves(coordCase1 + coordCase2,'number'))
                            g.updateDisplay(echiquier)
                            ########echiquier.switchTurn()
                            state = 'INIT'

            g.waitALittle()


main()