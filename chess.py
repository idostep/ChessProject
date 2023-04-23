#------imports-------
import re

import math
from enum import Enum

class Couleur(Enum):
    WHITE = 0
    BLACK = 1

class Tour:
    def __init__(self, whoseTurn=Couleur.WHITE):
        self.whoseTurn = whoseTurn

    def switch(self):
        if self.whoseTurn == Couleur.WHITE:
            self.whoseTurn = Couleur.BLACK
        else:
            self.whoseTurn = Couleur.WHITE

#------class piece------
class Piece:
    def __init__(self, team, icon, type):
        self.team = team
        self.type = type
        self.icon = icon        

class Echiquier:
    def __init__(self):
        #------settings------
    
        self.board = [ '' for i in range(64)]
        self.pieces={}
        self.turn = Tour()

    def setup(self):
        self.initPieces()
        self.setupPiecesOrder()

    def addPiece(self,code,Piece):
        self.pieces[code] = Piece
    
    def initPieces(self):
        #------initialisation des pieces------
        self.addPiece('nP', Piece(Couleur.BLACK, '♟ ', 'p'))
        self.addPiece('bP', Piece(Couleur.WHITE, '♙ ', 'p'))
        self.addPiece('nT', Piece(Couleur.BLACK, '♜ ', 't'))
        self.addPiece('bT', Piece(Couleur.WHITE, '♖ ', 't'))
        self.addPiece('nC', Piece(Couleur.BLACK, '♞ ', 'c'))
        self.addPiece('bC', Piece(Couleur.WHITE, '♘ ', 'c'))
        self.addPiece('nF', Piece(Couleur.BLACK, '♝ ', 'f'))
        self.addPiece('bF', Piece(Couleur.WHITE, '♗ ', 'f'))
        self.addPiece('nD', Piece(Couleur.BLACK, '♛ ', 'd'))
        self.addPiece('bD', Piece(Couleur.WHITE, '♕ ', 'd'))
        self.addPiece('nR', Piece(Couleur.BLACK, '♚ ', 'r'))
        self.addPiece('bR', Piece(Couleur.WHITE, '♔ ', 'r'))
        
        #------initialisation de l'ordre------
        self.Norder = 'nT','nC','nF','nD','nR','nF','nC','nT'
        self.Border = 'bT','bC','bF','bD','bR','bF','bC','bT'

        #------application de l'ordre de pieces------
    '''def setupPiecesOrder(self):
        for i in range(8):
            self.board[i] = self.Norder[i]
            self.board[i+8+8*6]=self.Border[i]
            self.board[i+8]='nP'
            self.board[i+8+8*5]='bP'''
        
    def WhoseTurn(self) -> Couleur:
        """
        Returns the color of the player whose turn it is.

        :return: A `Couleur` object representing the color of the player whose turn it is.
        """
        return self.turn.whoseTurn

    def switchTurn(self):
        self.turn.switch()

#------requete input du coup a jouer-------
    def turn(self,status):
        """
        @TODO@: REMOVE OLD
        """
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

    #------deplacement d'une piece sur le board------ input E3e4 outpout 52,36
    def translate_moves(self,played,type):
        values = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
        if type == 'number':
            from_ = int(values[played[0].lower()])+((8-int(played[1]))*8)
            to_ = int(values[played[2].lower()])+((8-int(played[3]))*8)
        
        if type == 'coord':
            from_ = int(values[played[0].lower()]),((8-int(played[1])))
            to_ = int(values[played[2].lower()]),((8-int(played[3])))
        return from_, to_

    def translate_move(self,played,type):
        values = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
        if type == 'coord':
            played = int(values[played[0].lower()]), ((8-int(played[1])))
        if type == 'number':
            played = int(values[played[0].lower()])+ ((8-int(played[1]))*8)
        return played
    
#------piecemove------
    def move_piece(self,from_to):
        from_ = from_to[0]
        to_ = from_to[1]
        self.board[to_] = self.board[from_]
        self.board[from_] = ''

    def convertCoordCaseToXY(self,coordCase):
        x,y=self.translate_move(coordCase, 'coord')
        return x,y
        
    def getPieceOnCoord(self, coordCase):
        x,y = self.convertCoordCaseToXY(coordCase)
        if self.board[x+y*8] in self.pieces:
            return self.pieces[self.board[x+y*8]]
        return None
    
    def getPieceOnBiCoord(self, x,y):
        if x <= 7 and y <= 7 and x >= 0 and y >= 0 and self.board[x+y*8] in self.pieces:
            return self.pieces[self.board[x+y*8]]
        return None
    

    def TestValidMove(self, fromto):
        piece = self.getPieceOnCoord(fromto[0]+fromto[1]).type
        from_ , to_ = self.translate_moves(fromto,'coord')
        
        print (f"{self.board[from_[0]+from_[1]*8]} from {from_} to {to_} {self.board[to_[0]+to_[1]*8]}")
        if piece == 'p':
            pawncolor = self.getPieceOnCoord(fromto[0]+fromto[1]).team

            if pawncolor == Couleur.WHITE:
                if from_[0] == to_[0] and from_[1] == to_[1]+1 and self.board[to_[0]+to_[1]*8] == '':
                    return True

                if from_[1] == 6 and from_[0] == to_[0] and to_[1] == 4 and self.board[5*8 + from_[0]] == '':
                    return True
                if self.getPieceOnCoord(fromto[2]+fromto[3]) != None:
                    eatcolor = self.getPieceOnCoord(fromto[2]+fromto[3]).team
                    if eatcolor != Couleur.WHITE and from_[1] == to_[1]+1 and (from_[0] == to_[0]+1 or from_[0] == to_[0]-1):
                        return True
                return False

            elif pawncolor == Couleur.BLACK:
                if from_[0] == to_[0] and from_[1] == to_[1]-1 and self.board[to_[0]+to_[1]*8] == '':
                    return True
                if from_[1] == 1 and from_[0] == to_[0] and to_[1] == 3 and self.board[2*8 + from_[0]] == '':
                    return True
                if self.getPieceOnCoord(fromto[2]+fromto[3]) != None:
                    eatcolor = self.getPieceOnCoord(fromto[2]+fromto[3]).team
                    if eatcolor != Couleur.BLACK and from_[1] == to_[1]-1 and (from_[0] == to_[0]+1 or from_[0] == to_[0]-1):
                        return True
            return False

        if piece == 'r':
            if abs(from_[0]-to_[0]) in [0,1]  and abs(from_[1]-to_[1]) in [0,1]:
                return True
            return False
        
        if piece == 'c':
            if abs(from_[0]-to_[0]) in [2,1]  and abs(from_[1]-to_[1]) in [2,1] and abs(from_[1]-to_[1])-abs(from_[0]-to_[0]):
                return True
            return False

        if piece == 't' or piece == 'd':
            possiblemoves = []


            for i in range(1,8):
                if from_[1]+i >= 0 and self.board[from_[0]+(from_[1]-i)*8] == '':
                    possiblemoves.append((from_[0],from_[1]-i))
                else:
                    if from_[0]+(from_[1]-i)*8 >= 0 and self.getPieceOnBiCoord(from_[0],(from_[1]-i)) != None and self.getPieceOnBiCoord(from_[0],(from_[1]-i)).team != self.getPieceOnBiCoord(from_[0],from_[1]).team:
                                possiblemoves.append((from_[0],from_[1]-i))
                    break
            
            for i in range(1,8):
                if from_[1]+i <= 7 and self.board[from_[0]+(from_[1]+i)*8] == '':
                    possiblemoves.append((from_[0],from_[1]+i))
                else:
                    if from_[0]+(from_[1]+i)*8 <= 64 and self.getPieceOnBiCoord(from_[0],(from_[1]+i)) != None and self.getPieceOnBiCoord(from_[0],(from_[1]+i)).team != self.getPieceOnBiCoord(from_[0],from_[1]).team:
                                possiblemoves.append((from_[0],from_[1]+i))
                    break

            for i in range(1,8):
                if from_[0]-i >= 0 and self.board[from_[0]-i+from_[1]*8] == '':
                    possiblemoves.append((from_[0]-i,from_[1]))
                else:
                    if from_[0]-i+from_[1]*8 >= 0 and self.getPieceOnBiCoord(from_[0]-i,(from_[1])) != None and self.getPieceOnBiCoord(from_[0]-i,from_[1]).team != self.getPieceOnBiCoord(from_[0],from_[1]).team:
                                possiblemoves.append((from_[0]-i,from_[1]))
                    break
            
            for i in range(1,8):
                if from_[0]+i <= 7 and self.board[from_[0]+i+from_[1]*8] == '':
                    possiblemoves.append((from_[0]+i,from_[1]))
                else:
                    if from_[0]+i+from_[1]*8 <= 64 and self.getPieceOnBiCoord(from_[0]+i,(from_[1])) != None and self.getPieceOnBiCoord(from_[0]+i,from_[1]).team != self.getPieceOnBiCoord(from_[0],from_[1]).team:
                                possiblemoves.append((from_[0]+i,from_[1]))
                    break


        
            if (to_[0] , to_[1]) in possiblemoves:
                return True

        if piece == 'f' or piece == 'd':
            return True



        return False
    


    def setupPiecesOrder(self):
        for i in range(8):
            self.board[i] = self.Norder[i]
            self.board[i+8+8*6]=self.Border[i]
            self.board[i+8]='nP'
            self.board[i+8+8*5]='bP'
