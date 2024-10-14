import copy as co

current_format_alfa=['a','b','c','d','e','f','g','h']
current_format_num=['0','1','2','3','4','5','6','7']

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def match(self,list_pos): #checking given position is in input list or not
        for pos in list_pos:
            if self.row == pos.row and self.col == pos.col and pos!=None:
                return True
        return False
    
    def equal(self,pos): #checking equalation between two position 
        if self.row == pos.row and self.col== pos.col:
            return True
        return False
    
    def __str__(self):
        return f'({self.row},{self.col})'

class Piece:
    def __init__(self, color, board, position=None):
        self.color = color
        self.board = board
        self.has_moved = False 
        self.position = position

    def possible_moves(self): #turn a list of possible moves for piece
        pass

    def __str__(self):
        pass

class King(Piece):
    def __init__(self,color,board,position=None):
        super().__init__(color,board,position)
        self.piece_type = "king"
        
    def possible_moves(self):
        moves = []
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1),
                   (1, 1), (-1, 1), (1, -1), (-1, -1)]
        #making position
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
        #castling
        if not self.board.board[self.position.row][self.position.col].has_moved:
            # Check kingside castling
            if self.board.board[self.position.row][7] and not self.board.board[self.position.row][7].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in range(self.position.col + 1, 7)):
                    moves.append(Position(self.position.row, self.position.col + 2))
            # Check queenside castling
            if  self.board.board[self.position.row][0] and not self.board.board[self.position.row][0].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in range(1, self.position.col)):
                    moves.append(Position(self.position.row, self.position.col - 2))
        return moves
    
    def __str__(self):
        if self.color == "White":
            return "K"
        return "k" 
    
class Pawn(Piece):
    def __init__(self,color,board,position=None):
        super().__init__(color,board,position)
        self.piece_type = "pawn"
        self.en_passant = False
        self.done_passant_l_wb = False
        self.done_passant_r_wb =False
        self.done_passant_l_bw =False
        self.done_passant_r_bw = False

    def possible_moves(self):
        moves = []
        offsets_w_e=[(1,-1),(1,1)]
        offsets_b_e=[(-1,-1),(-1,1)]
        #making position when color piece is white
        if self.color=='White':
            if not self.has_moved:
                new_pos=Position(self.position.row + 2 ,self.position.col)
                if self.board.is_inside_board(new_pos) and self.board.is_square_empty(new_pos) :
                    if self.board.board[self.position.row + 1][self.position.col]==None:
                        moves.append(new_pos)
                        self.en_passant_white= True

            new_pos_1=Position(self.position.row + 1 ,self.position.col)
            if self.board.is_inside_board(new_pos_1) and self.board.is_square_empty(new_pos_1) :
                moves.append(new_pos_1)
                
            for dr, dc in offsets_w_e:
                new_pos_2 = Position(self.position.row + dr, self.position.col + dc)
                if self.board.is_inside_board(new_pos_2) and self.board.is_enemy_piece(new_pos_2, self.color):
                    moves.append(new_pos_2)

        #making position when color piece is black
        if self.color=='Black':
            if not self.has_moved:
                new_pos=Position(self.position.row - 2 ,self.position.col)
                if self.board.is_inside_board(new_pos) and self.board.is_square_empty(new_pos) :
                    if self.board.board[self.position.row - 1][self.position.col]==None:
                        moves.append(new_pos)
                        self.en_passant_black=True
                    
            new_pos_1=Position(self.position.row - 1 ,self.position.col)
            if self.board.is_inside_board(new_pos_1) and self.board.is_square_empty(new_pos_1) :
                moves.append(new_pos_1)

            for dr, dc in offsets_b_e:
                new_pos_2 = Position(self.position.row + dr, self.position.col + dc)
                if self.board.is_inside_board(new_pos_2) and self.board.is_enemy_piece(new_pos_2, self.color):
                    moves.append(new_pos_2)

    # en passant move
    # right _ white -> black   
        if self.color =="White":
            if self.position.row == 4:
                en_passant_target1=Position(4,self.position.col +1)
                if self.board.is_inside_board(en_passant_target1):
                    if self.board.board[4][self.position.col +1] != None:
                        if self.board.board[4][self.position.col +1].piece_type == "pawn" and self.board.board[4][self.position.col+1].color == "Black":
                            if self.board.board[4][self.position.col +1].en_passant:
                                en_passant_pos1=Position(5,self.position.col+1)
                                moves.append(en_passant_pos1)
                                self.done_passant_r_wb = True
    # left _ white -> black   
                en_passant_target2=Position(4,self.position.col -1)
                if self.board.is_inside_board(en_passant_target2):
                    if self.board.board[4][self.position.col -1] != None:
                        if self.board.board[4][self.position.col -1].piece_type == "pawn" and self.board.board[4][self.position.col-1].color == "Black":
                            if self.board.board[4][self.position.col -1].en_passant:
                                en_passant_pos2=Position(5,self.position.col -1)
                                moves.append(en_passant_pos2)
                                self.done_passant_l_wb = True
    # right _ black -> white 
        if self.color =="Black":  
            if self.position.row == 3:
                en_passant_target3=Position(3,self.position.col +1)
                if self.board.is_inside_board(en_passant_target3):
                    if self.board.board[3][self.position.col +1] != None:
                        if self.board.board[3][self.position.col +1].piece_type == "pawn" and self.board.board[3][self.position.col +1].color == "White":
                            if self.board.board[3][self.position.col +1].en_passant:
                                en_passant_pos3=Position(2,self.position.col +1)
                                moves.append(en_passant_pos3)
                                self.done_passant_r_bw = True
        # left _ black -> white 
                en_passant_target4=Position(3,self.position.col -1)
                if self.board.board[3][self.position.col -1] != None:
                    if self.board.is_inside_board(en_passant_target4):
                        if self.board.board[3][self.position.col -1].piece_type == "pawn" and self.board.board[3][self.position.col -1].color == "White":
                            if self.board.board[3][self.position.col -1].en_passant:
                                en_passant_pos4=Position(2,self.position.col -1)
                                moves.append(en_passant_pos4)
                                self.done_passant_l_bw = True

        return moves

    
    def __str__(self):
        if self.color == "White":
            return "P"
        return "p" 
    
class Knight(Piece):
    def __init__(self,color,board,position=None):
        super().__init__(color,board,position)
        self.piece_type = "knight"
    
    def possible_moves(self):
        #making position
        moves = []
        offsets = [(2, 1), (2, -1), (1, 2), (1, -2),
                   (-2, 1), (-2, -1), (-1, 2), (-1, -2)]
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
        return moves
    
    def __str__(self):
        if self.color == "White":
            return "N"
        return "n" 
            
class Rook(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "rook"

    def possible_moves(self):
        #making position
        moves = []
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        for dr, dc in directions:
            current_pos = self.position
            while True:
                new_pos_r = current_pos.row + dr
                new_pos_c = current_pos.col + dc
                new_pos = Position(new_pos_r, new_pos_c)
                if not self.board.is_inside_board(new_pos):
                    break 
                if self.board.board[new_pos.row][new_pos.col] is None:
                    moves.append(new_pos)
                    current_pos = new_pos
                elif (not self.board.board[new_pos.row][new_pos.col].color == self.color) or (self.color == "Black" and new_pos.row == 0) or (self.color == "White" and new_pos.row == 7):
                    moves.append(new_pos)
                    break
                else:
                    break
        return moves

    def __str__(self):
        if self.color == "White":
            return "R"
        return "r"
     
class Queen(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "queen"

    def possible_moves(self):
        #making position
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dr, dc in directions:
            current_pos = self.position
            while True:
                new_pos_r = current_pos.row + dr
                new_pos_c = current_pos.col + dc
                new_pos = Position(new_pos_r, new_pos_c)
                if not self.board.is_inside_board(new_pos):
                    break
                if self.board.board[new_pos.row][new_pos.col] is None:
                    moves.append(new_pos)
                    current_pos = new_pos
                elif self.board.board[new_pos.row][new_pos.col].color != self.color:
                    moves.append(new_pos)
                    break
                else:
                    break
        return moves
    
    def __str__(self):
        if self.color == "White":
            return "Q"
        return "q" 
    
class Bishop(Piece):
    def __init__(self, color, board, position=None):
        super().__init__(color, board, position)
        self.piece_type = "bishop"

    def possible_moves(self):
        #making position
        moves = []
        for dr, dc in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
            pos = self.position.row + dr
            col = self.position.col + dc
            while 0 <= pos < 8 and 0 <= col < 8:
                if self.board.board[pos][col] is None:
                    moves.append(Position(pos, col))
                    pos += dr
                    col += dc
                elif self.board.board[pos][col].color != self.color:
                    moves.append(Position(pos, col))
                    break
                else:
                    break
        return moves
    
    def __str__(self):
        if self.color == "White":
            return "B"
        return "b" 

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)] #initialize the board
        
    def place_piece(self, piece, position): #place given piece in the board at the given position
        self.board[position.row][position.col]=piece
        piece.position = position
        
    def remove_piece(self, piece): #remove given position
        self.board[piece.row][piece.col] = None

    def move_king(self, start_pos, end_pos): #castle move
        if self.board[start_pos.row][start_pos.col] :
            if self.board[start_pos.row][start_pos.col].has_moved == False:

                if self.board[start_pos.row][start_pos.col].piece_type == "king" and (self.board[end_pos.row][end_pos.col - 2] == self.board[start_pos.row][start_pos.col] or self.board[end_pos.row][end_pos.col + 2] == self.board[start_pos.row][start_pos.col]): 
                    if self.board[end_pos.row][end_pos.col + 2] == self.board[start_pos.row][start_pos.col]:
                        self.move_piece(start_pos ,Position(start_pos.row,start_pos.col - 2))
                        self.move_piece(Position(start_pos.row,0) ,Position(start_pos.row,start_pos.col - 1))
                        return False   
                    if self.board[end_pos.row][end_pos.col - 2] == self.board[start_pos.row][start_pos.col]:
                        self.move_piece(start_pos ,Position(start_pos.row,start_pos.col + 2))
                        self.move_piece(Position(start_pos.row,7) ,Position(start_pos.row,start_pos.col + 1))
                        return False  
        return True

    def move_piece(self, start_pos, end_pos): #move the piece to given pos 
        piece=self.board[start_pos.row][start_pos.col]
        self.place_piece(piece ,end_pos)
        self.remove_piece(start_pos)
        self.board[end_pos.row][end_pos.col].has_moved = True

        if piece and piece.piece_type == "pawn": #pawn removing for en_passant move
            if piece.done_passant_l_wb or piece.done_passant_r_wb:
                self.remove_piece(Position(piece.position.row - 1,piece.position.col))
            elif piece.done_passant_r_bw or piece.done_passant_l_bw: 
                self.remove_piece(Position(piece.position.row + 1,piece.position.col))
               
    def is_square_empty(self, position): #check given position is empty
        return self.board[position.row][position.col] == None

    def is_enemy_piece(self, position, color): #check given position is for enemy piece
        piece=self.board[position.row][position.col] #identify piece
        if piece == None: pass
        else:
            if piece.color==color: return False
            else: return True

    def is_inside_board(self, position): #check given position is inside board
        ROW_COl=[0,1,2,3,4,5,6,7]
        if position.row in ROW_COl and position.col in ROW_COl: return True 
        else: return False

    def print_board(self , board): #makes board obvious
        print(" | a b c d e f g h")
        print("------------------")
        for i, row in enumerate(board):
            row_str = str(i) + "| "
            for piece in row:
                if piece: row_str += f"{piece} "
                else: row_str += ". "
            print(row_str)
        print("\n")

class ChessSet:
    def __init__(self):
        self.board = Board()
        self.setup_board()

    def setup_board(self): #put piece in their position
        # placing white pieces
        self.board.place_piece(Rook("White",self.board), Position(0, 0)) 
        self.board.place_piece(Bishop("White",self.board), Position(0, 2))
        self.board.place_piece(Knight("White",self.board), Position(0, 1))
        self.board.place_piece(King("White",self.board), Position(0, 3))
        self.board.place_piece(Queen("White",self.board), Position(0, 4))
        self.board.place_piece(Knight("White",self.board), Position(0, 6))
        self.board.place_piece(Bishop("White",self.board), Position(0, 5))
        self.board.place_piece(Rook("White",self.board), Position(0, 7))
        self.board.place_piece(Pawn("White",self.board), Position(1, 0))
        self.board.place_piece(Pawn("White",self.board), Position(1, 1))
        self.board.place_piece(Pawn("White",self.board), Position(1, 2))
        self.board.place_piece(Pawn("White",self.board), Position(1, 3))
        self.board.place_piece(Pawn("White",self.board), Position(1, 4))
        self.board.place_piece(Pawn("White",self.board), Position(1, 5))
        self.board.place_piece(Pawn("White",self.board), Position(1, 6))
        self.board.place_piece(Pawn("White",self.board), Position(1, 7))
        # Placing black pieces
        self.board.place_piece(Rook("Black",self.board), Position(7, 0)) 
        self.board.place_piece(Bishop("Black",self.board), Position(7, 2))
        self.board.place_piece(Knight("Black",self.board), Position(7, 1))
        self.board.place_piece(King("Black",self.board), Position(7, 3))
        self.board.place_piece(Queen("Black",self.board), Position(7, 4))
        self.board.place_piece(Knight("Black",self.board), Position(7, 6))
        self.board.place_piece(Bishop("Black",self.board), Position(7, 5))
        self.board.place_piece(Rook("Black",self.board), Position(7, 7))
        self.board.place_piece(Pawn("Black",self.board), Position(6, 0))
        self.board.place_piece(Pawn("Black",self.board), Position(6, 1))
        self.board.place_piece(Pawn("Black",self.board), Position(6, 2))
        self.board.place_piece(Pawn("Black",self.board), Position(6, 3))
        self.board.place_piece(Pawn("Black",self.board), Position(6, 4))
        self.board.place_piece(Pawn("Black",self.board), Position(6, 5))
        self.board.place_piece(Pawn("Black",self.board), Position(6, 6))
        self.board.place_piece(Pawn("Black",self.board), Position(6, 7))
        
    def print_board(self,board):
        self.board.print_board(board)

class Chess:
    def __init__(self):
        self.chess_set = ChessSet()
        self.current_player=None
        self.pat_counter = 0 # a counter for pat mode

    def start_game(self): #stard game
        print("Welcome to Chess!\n")
        self.chess_set.print_board(self.chess_set.board.board)
        self.current_player = "White"
        while True: # main game cycle 
            enemy = "Black" if self.current_player == "White" else "White" # define enemy
            print(f"\n{self.current_player}'s turn:") # print turn for user

            if self.check_only_king_left(self.current_player): # check that only one king left for one side 
                print(f'{11 - self.pat_counter} move left to pot') 
                self.pat_counter+=1
 
            while True: # get input
                start_pos = input("Enter the position of the piece you want to move (e.g., 'a2'): ")
                end_pos = input("Enter the position to move the piece to (e.g., 'a4'): ")
                if self.is_valid_input(start_pos,end_pos,self.current_player): break # check starting pos and ending pos are valid

            if not self.check_dual_pawn_move(self.from_algebraic(start_pos) , self.from_algebraic(end_pos)): 
                self.undo_en_passant()

            if self.chess_set.board.move_king(self.from_algebraic(start_pos) , self.from_algebraic(end_pos)): #checking input for castle mode and move piece 
                self.chess_set.board.move_piece(self.from_algebraic(start_pos) , self.from_algebraic(end_pos)) #moveing pice

            self.chess_set.board.print_board(self.chess_set.board.board) #print game

            if self.is_pot(self.current_player):
                if self.is_check(self.current_player ,self.chess_set.board.board):
                    print(f'{self.current_player} is winner!!!')
                    break
                elif self.is_check(enemy,self.chess_set.board.board):
                    print(f'{enemy} is winner!!!')
                    break
                print('draw!!!')
                break

            if self.check_only_two_king_left() : #checking only kings left 
                print('draw!!!')
                break

            if self.pat_counter == 11: #checking pat counter 
                print('draw!!!')
                break

            if self.is_pawn_transform(self.current_player): # checking pawn transform
                i=self.is_pawn_transform(self.current_player)-1 # give pawns row
                self.pawn_transforming(i ,self.current_player ,self.chess_set.board)
            
            if self.is_check(self.current_player ,self.chess_set.board.board): #checking check for current player
                self.game_when_check(self.current_player)

            elif self.is_check(enemy,self.chess_set.board.board): #checking check for enemy 
                self.game_when_check(enemy)

            # self.undo_en_passant(start_pos)

            

            self.current_player = "Black" if self.current_player == "White" else "White" #cheing turn



    def check_dual_pawn_move(self, start_pos , end_pos):
        if self.chess_set.board.board[start_pos.row][start_pos.col] and self.chess_set.board.board[start_pos.row][start_pos.col].piece_type == "pawn":
            if end_pos.row == start_pos.row+2 or end_pos.row == start_pos.row -2 :
                self.chess_set.board.board[start_pos.row][start_pos.col].en_passant = True
                return True
        return False

    def undo_en_passant(self):
        for i in range(8):
            for j in range(8):
                if self.chess_set.board.board[i][j] and self.chess_set.board.board[i][j].piece_type == 'pawn':
                    self.chess_set.board.board[i][j].en_passant= False

    def check_only_two_king_left(self): # checkin only kingpieces left
        for i in range(8):
            for j in range(8):
                if self.chess_set.board.board[i][j] and not self.chess_set.board.board[i][j].piece_type == 'king':
                    return False
        return True
    
    def check_only_king_left(self,current_player): # checkin only kings piece left for a side
        for i in range(8):
            for j in range(8):
                if self.chess_set.board.board[i][j] and not self.chess_set.board.board[i][j].piece_type == 'king' and self.chess_set.board.board[i][j].color == current_player:
                    return False
        return True

    def pawn_transforming(self ,i ,current_player ,board):
        new_piece=new_piece=input('which piece you wnat to transform: \n 1.Queen \n 2.Bishop \n 3.Knight \n 4.Rook \n enter your choise:  ' ) # get input
        while not (new_piece=='1' or new_piece=='2' or new_piece =='3' or new_piece =='4'): # check input is valid 
            new_piece=input('incorrect input,try again : ')
        # transforming
        if self.current_player == 'White': 
            if new_piece == '1':self.chess_set.board.place_piece(Queen(current_player,board),Position(7,i))
            if new_piece == '2':self.chess_set.board.place_piece(Bishop(current_player,board),Position(7,i))
            if new_piece == '3':self.chess_set.board.place_piece(Knight(current_player,board),Position(7,i))
            if new_piece == '4':self.chess_set.board.place_piece(Rook(current_player,board),Position(7,i))
            self.chess_set.board.board[7][i].has_moved = True
        elif self.current_player == 'Black':
            if new_piece == '1':self.chess_set.board.place_piece(Queen(current_player,board),Position(0,i))
            if new_piece == '2':self.chess_set.board.place_piece(Bishop(current_player,board),Position(0,i))
            if new_piece == '3':self.chess_set.board.place_piece(Knight(current_player,board),Position(0,i))
            if new_piece == '4':self.chess_set.board.place_piece(Rook(current_player,board),Position(0,i))
            self.chess_set.board.board[0][i].has_moved = True 
        self.chess_set.board.print_board(board.board) # print board

    '''
    this fanction simulates the game if it is check .
    if the piece moves and the king isnt already in check
    the moveing procces will be done.    
    '''

    def game_when_check(self ,current_player):
        current_player_t = "Black" if current_player == "White" else "White" # define current player
        enemy_t = "Black" if current_player_t == "White" else "White" # define enemy
        print(f'{current_player_t} is check') # pirnt turn

        while True: # main game cycrle 
            test_game=co.deepcopy(self.chess_set.board.board) # make a copy of nested list of game
            while True: # getting input
                start_pos_t = input("Enter the position of the piece you want to move (e.g., 'a2'): ")
                end_pos_t = input("Enter the position to move the piece to (e.g., 'a4'): ")
                if self.is_valid_input(start_pos_t,end_pos_t,current_player_t): break # check its valied
            test_game[self.from_algebraic(end_pos_t).row][self.from_algebraic(end_pos_t).col]=test_game[self.from_algebraic(start_pos_t).row][self.from_algebraic(start_pos_t).col] #moveing piece to ending position
            test_game[self.from_algebraic(end_pos_t).row][self.from_algebraic(end_pos_t).col].position = Position(self.from_algebraic(end_pos_t).row,self.from_algebraic(end_pos_t).col) #chegeing positon attrebiute of piece
            test_game[self.from_algebraic(start_pos_t).row][self.from_algebraic(start_pos_t).col]= None #removeing piece from starting position
            if not self.is_check(enemy_t ,test_game): 
                #applying moves to main game
                self.chess_set.board.move_piece(self.from_algebraic(start_pos_t) , self.from_algebraic(end_pos_t)) 
                self.chess_set.board.print_board(test_game)
                self.current_player = "Black" if self.current_player == "White" else "White" #chainge turn
                return
            else:
                print('your king is check .')

    '''
    this function gets starting and ending position and 
    checks for those posiotions that game will be check 
    or not. 
    '''

    def is_valid_for_king(self, end_pos_t, start_pos_t ,current_player):
        enemy_t = "Black" if current_player == "White" else "White" #define enemy
        test_game=co.deepcopy(self.chess_set.board.board) #make a copy of nested list of game
        test_game[end_pos_t.row][end_pos_t.col]=test_game[start_pos_t.row][start_pos_t.col] #doing changes
        test_game[end_pos_t.row][end_pos_t.col].position = Position(end_pos_t.row,end_pos_t.col)
        test_game[start_pos_t.row][start_pos_t.col]= None
        if not self.is_check(enemy_t ,test_game): #checking game is check or not
            return True
        else:
            return False

    def is_valid_input(self, start_pos, end_pos, current_player):
        #check each of the inputs have length of two elements and the first letter is an alphabet and the second one is a digit
            if len(start_pos)==2 and (start_pos[0] in current_format_alfa) and (start_pos[1] in current_format_num) and len(end_pos)==2 and (end_pos[0] in current_format_alfa) and (end_pos[1] in current_format_num) :
                #check start_pos input isnt empty
                if self.chess_set.board.board[self.from_algebraic(start_pos).row][self.from_algebraic(start_pos).col]!=None :
                    #check turn
                    if self.chess_set.board.board[self.from_algebraic(start_pos).row][self.from_algebraic(start_pos).col].color == current_player :
                        # check end_pos input is in list of move of piece 
                        if self.from_algebraic(end_pos).match(self.chess_set.board.board[self.from_algebraic(start_pos).row][self.from_algebraic(start_pos).col].possible_moves()):
                            # checking move doesnt causes game check 
                            if self.is_valid_for_king(self.from_algebraic(end_pos) ,self.from_algebraic(start_pos) ,self.current_player):
                                return True
                            print('incurrect move for king.')
                            return False
                        print('incurrect end position')    
                        return False
                    else: 
                        print(f'you choose inccurect piece, its {current_player} turn')
                        return False
                else:
                    print('incurrect end position')
                    return False
            else: 
                print('incurrct input! try again.') 
                return False

    def is_check(self, current_player ,board):
        #find current_player's king on the board  
        king_piece = False
        enemy = "Black" if current_player == "White" else "White"
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece and piece.piece_type == "king" and piece.color == enemy:
                    king_piece = piece
        if not king_piece:
            return False
        #check if the king is in check
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece:
                    if king_piece.position.match(piece.possible_moves()):
                        return True          
        return False

    '''
    for all moves in possible_move list for all of pieces
    if move can do something that king wont check
    '''

    def is_checkmate(self, current_player):
        for i in range(8):
            for j in range(8):
                piece = self.chess_set.board.board[i][j] # define piece
                if piece and piece.color == current_player: # check the color
                    for pos in piece.possible_moves(): # itterates in list of position
                        if self.is_valid_for_king(pos,piece.position ,current_player): # checking given move
                            return True
        return False
    
    def is_pot(self, current_player):
        current_player = 'Black' if current_player == 'White' else 'White'
        
        for i in range(8):
            for j in range(8):
                piece = self.chess_set.board.board[i][j] #define piece
                if piece and piece.color == current_player: #check the color
                    for pos in piece.possible_moves(): #itterates in list of position
                        if self.is_valid_for_king(pos,piece.position ,current_player): #checking given move
                            return False
        return True

    def is_pawn_transform(self,player): #check pawn is in end of board to transform it to other piece
        for i in range(8):
            if player=="White":
                    if self.chess_set.board.board[7][i]!=None: 
                        if self.chess_set.board.board[7][i].piece_type=='pawn':
                            return i+1
            if player=="Black":
                    if self.chess_set.board.board[0][i]!=None: 
                        if self.chess_set.board.board[0][i].piece_type=='pawn':
                            return i+1
        return 0
            
    def from_algebraic(self,algebraic_notation): # turn standard input to algebratic form
        col = ord(algebraic_notation[0]) - ord('a')
        row = int(algebraic_notation[1])
        return Position(row,col)
    
if __name__ == "__main__":
    chess= Chess()
    chess.start_game()

