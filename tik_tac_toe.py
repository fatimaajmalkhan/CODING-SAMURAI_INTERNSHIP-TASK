import pygame
import sys
import random
pygame.init()
#window setting...
width=600
height=600
fps=60
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Famma's Tic Tac Toe")
font=pygame.font.SysFont("comicsans",40)
small_font=pygame.font.SysFont("comicsans",30)
#colors i'll be using...
bg_color = (230, 240, 255)  #powder blue
menu_bg_color = (235, 225, 255)  #lavender mist
line_color = (200, 190, 230)  #pale lilac
circle_color = (170, 200, 170)  #sage green
cross_color = (215, 155, 170)  #dusty rose
text_color = (60, 60, 60)  #charcoal gray
#board settings...
board=[]
for i in range(3):
    row=[]
    for j in range(3):
        row.append('')
    board.append(row)
square_size=width//3
circle_radius=square_size//3
circle_width=15
cross_width=25
space=square_size//4
#game state variables...
state="menu"
player_turn=True
game_over=False
ai_delay=False
ai_delay_start=0
#text drawing function...
def draw_text(text,x,y,font,color=text_color,center=True):
    label=font.render(text,True,color)
    rect=label.get_rect()
    rect.center=(x,y) if center else (x,y)
    screen.blit(label,rect)
    return rect
#it resets the game...
def reset_game():
    global board
    global player_turn
    global game_over
    global ai_delay
    board=[]
    for i in range(3):
        row=[]
        for j in range(3):
            row.append('')
        board.append(row)
    player_turn=True
    game_over=False
    ai_delay=False
#board drawing function...
def draw_board():
    screen.fill(bg_color)
    for i in range(1,3):
        pygame.draw.line(screen,line_color,(0,i*square_size),(width,i*square_size),10)
        pygame.draw.line(screen,line_color,(i*square_size,0),(i*square_size,height),10)
#draws 2 vertical and horizontal lines to make a 3x3 grid...
def draw_figures():
    for row in range(3):
        for col in range(3):
            if board[row][col]=='O':
                pygame.draw.circle(screen,circle_color,(col*square_size+square_size//2,row*square_size+square_size//2),circle_radius,circle_width)
            elif board[row][col]=='X':
                start1=(col*square_size+space,row*square_size+space)
                end1=(col*square_size+square_size-space,row*square_size+square_size-space)
                pygame.draw.line(screen,cross_color,start1,end1,cross_width)
                start2=(col*square_size+space,row*square_size+square_size-space)
                end2=(col*square_size+square_size-space,row*square_size+space)
                pygame.draw.line(screen,cross_color,start2,end2,cross_width)
#marking the cells...
def mark_square(row,col,player):
    board[row][col]=player
#check of the cell is empty...
def is_empty(row,col):
    return board[row][col]==''
#check horizontal,vertical and diagonal for the winner...
def check_winner():
    for row in board:
        if row[0]==row[1]==row[2]!='':
            return row[0]
    for col in range(3):
        if board[0][col]==board[1][col]==board[2][col]!='':
            return board[0][col]
    if board[0][0]==board[1][1]==board[2][2]!='':
        return board[0][0]
    if board[0][2]==board[1][1]==board[2][0]!='':
        return board[0][2]
    return None
#checks if the mtch is draw...
def is_draw():
    for row in board:
        for cell in row:
            if cell=='':
                return False
    return True
#minimax ai..ai tries to maximize the score and human tries to minimize the score...
def minimax(board_state,depth,is_max):
    winner=check_winner()
    if winner=='O':
        return 1
    elif winner=='X':
        return -1
    elif is_draw():
        return 0
    if is_max:
        best=float('-inf')
        for i in range(3):
            for j in range(3):
                if board_state[i][j]=='':
                    board_state[i][j]='O'
                    score=minimax(board_state,depth+1,False)
                    board_state[i][j]=''
                    best=max(best,score)
        return best
    else:
        best=float('inf')
        for i in range(3):
            for j in range(3):
                if board_state[i][j]=='':
                    board_state[i][j]='X'
                    score=minimax(board_state,depth+1,True)
                    board_state[i][j]=''
                    best=min(best,score)
        return best
#for ai moves..finds the best move and then calls it...
def ai_move():
    best_score=float('-inf')
    move=None
    for i in range(3):
        for j in range(3):
            if board[i][j]=='':
                board[i][j]='O'
                score=minimax(board, 0, False)
                board[i][j]=''
                if score>best_score:
                    best_score=score
                    move=(i,j)
    if move:
        mark_square(move[0],move[1],'O')
#for menu...
def show_menu():
    screen.fill(menu_bg_color)
    start_btn=draw_text("Start",width//2,250,font)
    instr_btn=draw_text("Instructions",width//2,320,font)
    exit_btn=draw_text("Exit",width//2,390,font)
    draw_text("FAMMA'S TIC TAC TOE",width//2,100,font)
    return {"start":start_btn,"instructions":instr_btn,"exit":exit_btn}
#for instructions...
def show_instructions():
    screen.fill(menu_bg_color)
    draw_text("How to Play",width//2,80,font)
    draw_text("You are X, AI is O.",60,160,small_font,center=False)
    draw_text("Click a cell to make your move.",60,200,small_font,center=False)
    draw_text("First to 3 in a row wins!",60,240,small_font,center=False)
    back_btn=draw_text("Back",width//2,500,font)
    return {"back":back_btn}
#to play again...
def show_play_again():
    draw_text("Do you want to play again?",width//2,height//2+50,font)
    yes_btn=draw_text("Yes",width//2-100,height//2+120,font)
    no_btn=draw_text("No",width//2+100,height//2+120,font)
    return {"yes":yes_btn,"no":no_btn}
#my game loop
clock=pygame.time.Clock()
buttons={}
play_again_buttons={}
while True:
    clock.tick(fps)
    mouse=pygame.mouse.get_pos()
    if state=="menu":
        buttons=show_menu()
    elif state=="instructions":
        buttons=show_instructions()
    elif state=="game":
        draw_board()
        draw_figures()
        if not game_over and not player_turn:
            if not ai_delay:
                ai_delay=True
                ai_delay_start=pygame.time.get_ticks()
            elif pygame.time.get_ticks()-ai_delay_start>300:
                ai_move()
                player_turn=True
                ai_delay=False
                if check_winner() or is_draw():
                    game_over=True
        if game_over:
            winner=check_winner()
            result="It's a Draw!" if winner is None else f"{winner} Wins!"
            draw_text(result,width//2,height//2-50,font)
            play_again_buttons=show_play_again()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            if state=="menu":
                if buttons["start"].collidepoint(mouse):
                    reset_game()
                    state="game"
                elif buttons["instructions"].collidepoint(mouse):
                    state="instructions"
                elif buttons["exit"].collidepoint(mouse):
                    pygame.quit()
                    sys.exit()
            elif state=="instructions":
                if buttons["back"].collidepoint(mouse):
                    state="menu"
            elif state=="game":
                if not game_over and player_turn:
                    x,y=mouse
                    row=y//square_size
                    col=x//square_size
                    if is_empty(row,col):
                        mark_square(row,col,'X')
                        player_turn=False
                        if check_winner() or is_draw():
                            game_over=True
                elif game_over:
                    if play_again_buttons["yes"].collidepoint(mouse):
                        reset_game()
                    elif play_again_buttons["no"].collidepoint(mouse):
                        pygame.quit()
                        sys.exit()
    pygame.display.update()
