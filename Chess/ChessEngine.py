

class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []

        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.pins = []
        self.checks = []
        



    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        # atualiza a localização do rei
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        #Promoção de peão não implementada

        if move.pieceMoved == 'wP' and move.endRow == 0:
            move.isPromotion = True
        elif move.pieceMoved == 'bP' and move.endRow == 7:
            move.isPromotion = True
        else:
            move.isPromotion = False



    def undoMove(self):
        if len(self.moveLog) != 0: # checa se há um movimento para desfazer
            move = self.moveLog.pop() # Remove o ultimo movimento
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # troca o turno de volta
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)            


    # considera que todos os movimentos são cheks
    def getValidMoves(self):
        """
        Gera movimentos e filtra os que deixam o rei que acabou de mover em cheque.
        Observação: assume que Move.pieceMoved foi preenchido corretamente na criação do Move.
        """
        moves = self.getAllPossibleMoves()
        validMoves = []
        for move in moves:
            # simula o movimento
            self.makeMove(move)

            # quem moveu? (pode usar move.pieceMoved[0])
            moverColor = move.pieceMoved[0]  # 'w' ou 'b'
            attackerColor = 'b' if moverColor == 'w' else 'w'
            # posição do rei da cor que acabou de mover
            kingRow, kingCol = (self.whiteKingLocation if moverColor == 'w'
                                else self.blackKingLocation)

            # se o rei do jogador que moveu NÃO estiver sob ataque do inimigo, o movimento é válido
            if not self.squareUnderAttack(kingRow, kingCol, attackerColor):
                validMoves.append(move)

            # desfaz a simulação
            self.undoMove()

        return validMoves


#####
##
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        

    def squareUnderAttack(self, r, c, attackerColor=None):
        """
        Retorna True se a casa (r, c) está atacada por alguma peça da cor attackerColor.
        Se attackerColor for None, assume o inimigo baseado em self.whiteToMove (fallback).
        """
        if attackerColor is None:
            attackerColor = "b" if self.whiteToMove else "w"

        # 1. Peões (ataques diagonais)
        if attackerColor == "w":
            pawnAttacks = [(1, -1), (1, 1)]  # brancos atacam pra cima (rei preto está acima)
        else:
            pawnAttacks = [(-1, -1), (-1, 1)]  # pretos atacam pra baixo (rei branco está abaixo)

        for d in pawnAttacks:
            endRow, endCol = r + d[0], c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if self.board[endRow][endCol] == attackerColor + "P":
                    return True

        # 2. Cavalo
        knightMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1)]
        for d in knightMoves:
            endRow, endCol = r + d[0], c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if self.board[endRow][endCol] == attackerColor + "N":
                    return True

        # 3. Torre e Dama (linhas e colunas)
        directions_straight = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        for d in directions_straight:
            for i in range(1, 8):
                endRow, endCol = r + d[0] * i, c + d[1] * i
                if not (0 <= endRow < 8 and 0 <= endCol < 8):
                    break
                piece = self.board[endRow][endCol]
                if piece != "--":
                    if piece[0] == attackerColor and (piece[1] == "R" or piece[1] == "Q"):
                        return True
                    else:
                        break

        # 4. Bispo e Dama (diagonais)
        directions_diag = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in directions_diag:
            for i in range(1, 8):
                endRow, endCol = r + d[0] * i, c + d[1] * i
                if not (0 <= endRow < 8 and 0 <= endCol < 8):
                    break
                piece = self.board[endRow][endCol]
                if piece != "--":
                    if piece[0] == attackerColor and (piece[1] == "B" or piece[1] == "Q"):
                        return True
                    else:
                        break

        # 5. Rei inimigo (uma casa de distância)
        kingMoves = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1),          (0, 1),
                    (1, -1), (1, 0),  (1, 1)]
        for d in kingMoves:
            endRow, endCol = r + d[0], c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if self.board[endRow][endCol] == attackerColor + "K":
                    return True

        return False





    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # chama a função apropriada baseado na peça
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: # movimento do peão branco
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c), (r-1,c), self.board))
                if r ==6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c), (r-2,c), self.board))
            if c - 1 >= 0:#captura para esquerda
                if self.board[r-1][c-1][0] == 'b': #peça inimiga
                    moves.append(Move((r,c), (r-1,c-1), self.board))
            if  c + 1 <= 7: #captura para direita
                if self.board[r-1][c+1][0] == 'b': #peça inimiga
                    moves.append(Move((r,c), (r-1,c+1), self.board))
        else: # movimento do peão preto
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c), (r+2,c), self.board))
            if c - 1 >= 0:#captura para esquerda
                if self.board[r+1][c-1][0] == 'w': #peça inimiga
                    moves.append(Move((r,c), (r+1,c-1), self.board))
            if  c + 1 <= 7: #captura para direita
                if self.board[r+1][c+1][0] == 'w': #peça inimiga
                    moves.append(Move((r,c), (r+1,c+1), self.board))

    
    def getKnightMoves(self, r, c, moves):
        knigthMoves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knigthMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8: #limites do tabuleiro
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #casa vazia ou inimigo
                    moves.append(Move((r,c), (endRow, endCol), self.board))

        

    def getSlidingMoves(self, r, c, moves, directions, maxSteps = 8):
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, maxSteps + 1): # limite de casa
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #limites do tabuleiro
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #casa vazia
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #inimigo valido
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else: # peça amiga
                        break
                else: # fora do tabuleiro
                    break

    def getRookMoves(self, r, c, moves):
        directions = ((-1,0), (0,-1), (1,0), (0,1))
        self.getSlidingMoves(r, c, moves, directions)

    def getBishopMoves(self, r, c, moves):
        directions = ((-1,-1), (-1,1), (1, -1), (1,1))
        self.getSlidingMoves(r, c, moves, directions)

    def getQueenMoves(self, r, c, moves):
        directions = ((-1,0), (0,-1), (1,0), (0,1),(-1,-1), (-1,1), (1, -1), (1,1))
        self.getSlidingMoves(r, c, moves, directions, maxSteps=8)

    def getKingMoves(self, r, c, moves):
        directions = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
        self.getSlidingMoves(r, c, moves, directions, maxSteps=1) # o rei se move apenas uma casa




class Move():

    # mapas de linhas e colunas para notação algébrica
    ranksToRows = {"1":7, "2":6, "3":5, "4":4,
                    "5":3, "6":2, "7":1, "8":0} 
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d":3,
                    "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    
    def getChessNotation(self):
        # pode ser melhorado com notação algébrica
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
