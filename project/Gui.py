from main_game import *
import tkinter as tk
from tkinter import messagebox


                                                            # GUI part was coded in a separate class
class Gui :
    def __init__(self):
        self.root = tk.Tk()                                 # tkinter window
        self.root.resizable(height=False , width=False)     # disable the resizability
        self.root.title('Chess')                            # title
        self.chs = Chess()
                                                            #set turn
        self.turn = 'White'
        self.enemy = 'Black'
                                                            #import photo by their address
        self.KW=tk.PhotoImage( file ="kwhite.png")
        self.RW=tk.PhotoImage( file ="rwhite.png")
        self.BW=tk.PhotoImage( file ="bwhite.png")
        self.PW=tk.PhotoImage( file ="pwhite.png")
        self.NW=tk.PhotoImage( file ="nwhite.png")
        self.QW=tk.PhotoImage( file ="qwhite.png") 
        self.KB=tk.PhotoImage( file ="kblack.png")
        self.RB=tk.PhotoImage( file ="rblack.png")
        self.BB=tk.PhotoImage( file ="bblack.png")
        self.PB=tk.PhotoImage( file ="pblack.png")
        self.NB=tk.PhotoImage( file ="nblack.png")
        self.QB=tk.PhotoImage( file ="qblack.png") 
        self.EE=tk.PhotoImage( file ="empty.png")
        self.img = tk.PhotoImage(file='Icon.png')
        self.root.iconphoto(False, self.img) 
                                                            #calling the methods
        self.create_board()
        self.print_board()
        self.place_piece()

        self.window_check = False

    def create_board(self):
                                                            #create buttons and put them in a list by their rows and columns
        self.buttons = []
        for i in range(8):
            button_row = []
            for j in range(8):
                button = tk.Button(self.root, text ="",image=None )
                button.grid(row=i, column = j)
                button.bind("<Button-1>",self.left_click(i,j))
                button.color = None
                button.name = None
                button.image = None
                button_row.append(button)
            self.buttons.append(button_row)

                                                            # making labels that the window needs! 

        self.libel_turn=tk.Label(text=f'{self.turn} turn')
        self.libel_check=tk.Label(text=' ')
        self.label_pot=tk.Label(text=" ")
        self.libel_turn.grid(row=8 ,columnspan=3, sticky='w')
        self.libel_check.grid(row=9 ,columnspan=3,sticky='w')
        self.label_pot.grid(row=10, columnspan=3 , sticky="w")

    def place_piece(self):
                                                            #overwrite board from basic game
        for i in range(8):
            for j in range(8):
                if not self.chs.chess_set.board.board[i][j]==None:
                    if self.chs.chess_set.board.board[i][j].color == 'White':
                        if self.chs.chess_set.board.board[i][j].piece_type == 'king':
                            self.buttons[i][j].config(text='K', image=self.KW)
                            self.buttons[i][j].name='K'
                            self.buttons[i][j].image=self.KW
                        if self.chs.chess_set.board.board[i][j].piece_type == 'queen':
                            self.buttons[i][j].config(text='Q' ,image=self.QW)
                            self.buttons[i][j].name='Q'
                            self.buttons[i][j].image=self.QW
                        if self.chs.chess_set.board.board[i][j].piece_type == 'bishop':
                            self.buttons[i][j].config(text='B' ,image=self.BW)
                            self.buttons[i][j].name='B'
                            self.buttons[i][j].image=self.BW
                        if self.chs.chess_set.board.board[i][j].piece_type == 'rook':
                            self.buttons[i][j].config(text='R' ,image=self.RW)
                            self.buttons[i][j].name='R'
                            self.buttons[i][j].image=self.RW
                        if self.chs.chess_set.board.board[i][j].piece_type == 'knight':
                            self.buttons[i][j].config(text='N' ,image=self.NW)
                            self.buttons[i][j].name='N'
                            self.buttons[i][j].image=self.NW
                        if self.chs.chess_set.board.board[i][j].piece_type == 'pawn':
                            self.buttons[i][j].config(text='P' ,image=self.PW)
                            self.buttons[i][j].name='P'
                            self.buttons[i][j].image=self.PW
                    if self.chs.chess_set.board.board[i][j].color == 'Black':
                        if self.chs.chess_set.board.board[i][j].piece_type == 'king':
                            self.buttons[i][j].config(text='k' ,image=self.KB)
                            self.buttons[i][j].name='k'
                            self.buttons[i][j].image=self.KB
                        if self.chs.chess_set.board.board[i][j].piece_type == 'queen':
                            self.buttons[i][j].config(text='q' ,image=self.QB)
                            self.buttons[i][j].name='q'
                            self.buttons[i][j].image=self.QB
                        if self.chs.chess_set.board.board[i][j].piece_type == 'bishop':
                            self.buttons[i][j].config(text='b' ,image=self.BB)
                            self.buttons[i][j].name='b'
                            self.buttons[i][j].image=self.BB
                        if self.chs.chess_set.board.board[i][j].piece_type == 'rook':
                            self.buttons[i][j].config(text='r' ,image=self.RB)
                            self.buttons[i][j].name='r'
                            self.buttons[i][j].image=self.RB
                        if self.chs.chess_set.board.board[i][j].piece_type == 'knight':
                            self.buttons[i][j].config(text='n' ,image=self.NB)
                            self.buttons[i][j].name='n'
                            self.buttons[i][j].image=self.NB
                        if self.chs.chess_set.board.board[i][j].piece_type == 'pawn':
                            self.buttons[i][j].config(text='p' ,image=self.PB)
                            self.buttons[i][j].name='p'
                            self.buttons[i][j].image=self.PB
                else:
                                                            # sets the empty button image! 
                    self.buttons[i][j].config(image=self.EE)

    
    def print_board(self):
                                                            #paints the board like a chess board!
        for i in range(8):
            for j in range(8):
                if (i+j)%2==0:
                    self.buttons[i][j].config(bg='#DDB88C')
                    self.buttons[i][j].color='#DDB88C'
                else:
                    self.buttons[i][j].config(bg='#A66D4F')
                    self.buttons[i][j].color='#A66D4F'
        if self.chs.is_check(self.turn , self.chs.chess_set.board.board):
            self.king_endanger()
                                                            # takes the position of button and color , changes its color

    def change_button_color(self,pos,color):
        self.buttons[pos.row][pos.col].config(bg=color)
        self.buttons[pos.row][pos.col].color=color
                                                            # moves the piece by its image(changes its image)! 

    def move_piece_gui(self,row,col,piece,pictures):
        self.buttons[row][col].config(text=piece ,image=pictures)   # changes the pic of button which you can see!
        self.buttons[row][col].name=piece                          # changes the 'attribute' of button !  
        self.buttons[row][col].image=pictures                      # changes the 'attribute' of image !  


    def remove_piece_gui(self,row,col):                         # removes the piece by its image(changes its image to empty image [named EE])
        self.buttons[row][col].config(text=' ',image=self.EE)
        self.buttons[row][col].name=None
        self.buttons[row][col].image=self.EE

    def change_turn(self):                                      # changes the player's turn by two attributes named white & black!
        if self.turn == 'White': 
            self.turn = 'Black' 
            self.enemy = 'White'
            self.change_libel_text(self.libel_turn ,'Black turn')
        else: 
            self.turn = 'White'
            self.enemy = 'Black'
            self.change_libel_text(self.libel_turn ,'White turn')

    def check_turn(self,piece):                                  # checks who's turn is now!
        if piece!=None:
            if piece.islower():return 'Black'
            else:return 'White'

    def winner_message(self, player):                            # makes the winner message
        messagebox.showinfo('Chess',f'{player} win!!!!!!')

    def pot_message(self):                                       # makes the draw message
        messagebox.showinfo("chess", "Pot!!!!!!")
    
    def close_page(self,window):                                 # closes the window of game
        window.destroy()

    def change_libel_text(self, label, word):                    #changes the text of a label if we need!
        label.config(text=word)

    def in_transform(self,window,black_p,white_p,piece_b,piece_w):    #simulates the pawn transformation if it arrives to end of the board!
                                                                     #transform pawn to given piece
        for i in range(8):
            if self.chs.chess_set.board.board[0][i]!=None and self.chs.chess_set.board.board[0][i].piece_type=='pawn':
                self.move_piece_gui(0 ,i ,piece_b , black_p  )
                self.chs.chess_set.board.place_piece(piece_b,Position(0,i))
                self.chs.chess_set.board.board[0][i].has_moved = True
                self.window_check = False
                self.close_page(window)
            elif self.chs.chess_set.board.board[7][i]!=None and self.chs.chess_set.board.board[7][i].piece_type=='pawn':  
                self.move_piece_gui(7 ,i , piece_w , white_p)
                self.chs.chess_set.board.place_piece(piece_w,Position(7,i))
                self.chs.chess_set.board.board[7][i].has_moved = True
                self.window_check = False
                self.close_page(window)

                                                                    #functions for pawn transforming
    def queen_piece(self):
        self.in_transform(self.win,self.QB,self.QW,Queen("Black",self.chs.chess_set.board),Queen("White",self.chs.chess_set.board))
        self.check_when_transpawn()
    def bishop_piece(self):
        self.in_transform(self.win,self.BB,self.BW,Bishop("Black",self.chs.chess_set.board),Bishop("White",self.chs.chess_set.board))
        self.check_when_transpawn()
    def rook_piece(self):
        self.in_transform(self.win,self.RB,self.RW,Rook("Black",self.chs.chess_set.board),Rook("White",self.chs.chess_set.board))
        self.check_when_transpawn()
    def knight_piece(self):
        self.in_transform(self.win,self.NB,self.NW,Knight("Black",self.chs.chess_set.board),Knight("White",self.chs.chess_set.board))
        self.check_when_transpawn()

    def check_when_transpawn(self):                               #if the transformed piece checks the enemy king (or checkmate) this function executes!
        self.change_turn()
        if self.chs.is_check(self.turn ,self.chs.chess_set.board.board):
            self.king_endanger()
            if self.chs.is_pot(self.turn): 
                self.winner_message(self.turn)
                self.close_page(self.root)
        self.change_turn()
        
    def pawn_transform(self):
                                                                # create a window for pawn transforming(for taking the player choice between pieces!)
        self.win=tk.Toplevel()                                  # makes a window for user transforming choice
        self.window_check=True
        l1=tk.Label(self.win,text='which piece you wnat to transform:').pack()
        b1=tk.Button(self.win,text='Queen',command=self.queen_piece).pack(fill='x')
        b2=tk.Button(self.win,text='Bishop',command=self.bishop_piece).pack(fill='x')
        b3=tk.Button(self.win,text='Rook',command=self.rook_piece).pack(fill='x')
        b4=tk.Button(self.win,text='Knight',command=self.knight_piece).pack(fill='x')

                                                                # MAIN part of game

    def king_endanger(self):                                    # paints the king's background to red if it's check
        for k in range(8):
            for l in range(8):
                if self.chs.chess_set.board.board[k][l] != None:  # finds the position of king which is in check!
                    if self.chs.chess_set.board.board[k][l].piece_type == "king" and self.turn =="White" and self.chs.chess_set.board.board[k][l].color =="Black" :
                        self.buttons[k][l].config(bg="#cb2026")   # and now paints it! 
                        
                        self.change_libel_text(self.libel_check ,f'{self.turn} is check')
                    elif self.chs.chess_set.board.board[k][l].piece_type == "king" and self.turn =="Black" and self.chs.chess_set.board.board[k][l].color =="White" :
                        self.buttons[k][l].config(bg="#cb2026")
                        self.change_libel_text(self.libel_check, f'{self.enemy} is check')
                        

    def left_click(self,i,j):
        def inner(event):
            if not self.window_check:                            #check pawn window is close
                if not self.buttons[i][j].color=='#eeeed2':        #check button color
                    if self.turn == self.check_turn(self.buttons[i][j].name): #check turn
                        self.print_board()
                        if self.chs.is_check(self.enemy , self.chs.chess_set.board.board):
                            self.change_turn()
                            self.king_endanger()
                            self.change_turn()
                        if self.chs.chess_set.board.board[i][j]!=None: #check button type
                            start_pos=Position(i,j)
                            for pos in self.chs.chess_set.board.board[i][j].possible_moves(): #iterate in possible moves list
                                if self.chs.is_valid_for_king(pos , start_pos , self.turn):
                                    self.change_button_color(pos ,'#eeeed2') #change button color in possible move
                                self.change_button_color(Position(i,j),'#D6D6BD') #change pressed button color
                                # self.chs.chess_set.print_board(self.chs.chess_set.board.board)


                if self.buttons[i][j].color=='#eeeed2': #check button color
                        for roww in range(8):
                            for colmn in range(8):
                                if self.buttons[roww][colmn].color=='#D6D6BD': #define pressed button

                                    if not self.chs.check_dual_pawn_move(Position(roww , colmn),Position(i,j)):
                                        self.chs.undo_en_passant()

                                    if not self.chs.chess_set.board.move_king(Position(roww,colmn),Position(i,j)): #check special king move and move piece in base game
                                        self.place_piece() #overwrite gameboard
                                        self.print_board() #paint board
                                        
                                    else:
                                        self.chs.chess_set.board.move_piece(Position(roww,colmn),Position(i,j)) #move piece in base game
                                        self.place_piece() #overwrite gameboard
                                        self.print_board() #paint board

                                    if self.chs.is_pawn_transform(self.turn): #check pawn transforming
                                        self.pawn_transform()
                                        
                        
                                    if self.chs.check_only_king_left(self.turn): # first pot mode
                                        self.label_pot.config(text=f'{11 - self.chs.pat_counter} move left to pot')
                                        self.chs.pat_counter +=1
                                    if self.chs.pat_counter == 11:
                                        self.pot_message()
                                        self.close_page(self.root)
                                        
                                    if self.chs.check_only_two_king_left(): #check pot (for giving message to user)
                                        self.pot_message()
                                        self.close_page(self.root)



                                    if self.chs.is_pot(self.turn):        # checks for winner (for giving message to user)
                                        if self.chs.is_check(self.enemy ,self.chs.chess_set.board.board):
                                            self.winner_message(self.enemy)
                                            self.close_page(self.root)
                                        elif self.chs.is_check(self.turn ,self.chs.chess_set.board.board):
                                            self.winner_message(self.turn)
                                            self.close_page(self.root)
                                        else:
                                            self.pot_message()            # if king has no moves and also is not check, so it's pot!
                                            self.close_page(self.root)

                                    if self.chs.is_check(self.turn , self.chs.chess_set.board.board): #checking king check
                                        self.king_endanger()
                                    if self.chs.is_check(self.enemy , self.chs.chess_set.board.board):
                                        self.king_endanger()
                                                                          #clears the label of king check!
                                    if (not self.chs.is_check(self.enemy , self.chs.chess_set.board.board)) and (not self.chs.is_check(self.turn , self.chs.chess_set.board.board)): 
                                        self.change_libel_text(self.libel_check ,' ')

                                    self.change_turn()


        return inner
                                                                   # the mainloop of tkinter that lets the window of game stays open

    def start(self):
            self.root.mainloop()
            
if __name__ == "__main__":        
    game=Gui()
    game.start()
