

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
        # Gerar todos os movimentos
        moves = self.getAllPossibleMoves()
        # para cada movimento
        for i in range(len(moves)-1, -1, -1): # ir para trás para remover itens sem afetar o loop
            self.makeMove(moves[i])

            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) # movimento deixa o rei em cheque
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        
        return moves


#####
##
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # turno inimigo
        oppMove = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMove:
            if move.endRow == r and move.endCol == c: # se o movimento inimigo pode alcançar o rei
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
