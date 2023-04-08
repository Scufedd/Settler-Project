import os
import pygame
import random
import math
import time
from colour import Color
from hexgrid import legal_tile_ids
from pprint import pprint
from pygame.locals import *
from Tiles import GameTile, ResourceTile
from utils import ASSET_DIR, TILE_CARDS_DIR
from player import Player
from button import *



# Initialize pygame
pygame.init()

DISPLAY_WIDTH, DISPLAY_HEIGHT = 1450, 800
NUM_FONT = pygame.font.SysFont('Palatino', 40)
WORD_FONT = pygame.font.SysFont('Palatino', 25)
GAME_LOG_FONT = pygame.font.SysFont('calibri', 25)




screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
bg_img = pygame.image.load(os.path.join(ASSET_DIR, "tile_order.png"))
bg_img.convert()
bg_rect = bg_img.get_rect()
num_players = 6
player_names = ['Eddie', 'Morgan', 'Ryan', 'Noah', 'Yash', 'Nelson']
node_buttons = [] #list of ButtonHex objects for nodes
tile_buttons = [] #list of ButtonHex object for tiles
game_log = [] # list for storing game events as strings

settlement_img = pygame.image.load('src\\assets\\buildings\\s_img.png')
settlement_img = pygame.transform.scale(settlement_img, (50, 50))
city_img = pygame.image.load('src\\assets\\buildings\\c_img.png')
city_img = pygame.transform.scale(city_img, (50, 50))

WHITE = (255,255,255)
RED = (255,0,0)
colors = [(255,0,0), (25, 255,25) , (255,255,77), (255,153,51), (0,0,0), (35, 219, 222)] #colors r g y o b c
# maps the tile_id to the x, y, coordinates for the screen
board_mapping = {'tiles': {
        1: (236, 98),
        2: (162, 233),
        3: (81, 364),
        4: (162, 494),
        5: (239, 630),
        6: (393, 629),
        7: (545, 631),
        8: (622, 496),
        9: (703, 362),
        10: (623, 229),
        11: (547, 96),
        12: (391, 95),
        13: (314, 229),
        14: (236, 363),
        15: (317, 495),
        16: (469, 496),
        17: (545, 363),
        18: (468, 230),
        19: (392, 362)
    }, 'nodes': {


        1011: (621, 318),
        1013: (699, 187),
        105: (392, 714),
        107: (472, 589),
        109: (546, 450),
        1110: (622, 410),
        1112: (700, 279),
        116: (468, 671),
        118: (547, 542),
        1211: (696, 450),
        1213: (774, 318),
        127: (546, 719),
        129: (619, 586),
        1310: (699, 540),
        1312: (775, 408),
        138: (625, 675),
        23: (10, 320),
        25: (82, 186),
        27: (163, 55),
        32: (7, 408),
        34: (86, 274),
        36: (162, 140),
        38: (235, 10),
        43: (83, 451),
        45: (160, 316),
        47: (237, 183),
        49: (311, 53),
        510: (389, 11),
        52: (84, 539),
        54: (161, 408),
        56: (236, 276),
        58: (312, 142),
        611: (469, 56),
        63: (161, 579),
        65: (236, 448),
        67: (314, 318),
        69: (391, 185),
        710: (467, 140),
        712: (542, 9),
        72: (159, 672),
        74: (239, 539),
        78: (389, 274),
        811: (546, 185),
        813: (618, 52),
        83: (235, 717),
        85: (314, 589),
        910: (548, 274),
        912: (623, 144),
        94: (318, 673),
        96: (392, 538),
        76: (315, 407),
        87: (393, 449),
        98: (468, 408),
        89: (467, 317),

    }}

def setup():
    """
    Sets up the initial catan board positions and the ids for each tile

    Returns:
        board: List of tile objects
        tile_sprites: list of images for each tile
        board_mapping: dictionary that maps the tile object to an id and nodes to respective coordinates.
    """
    # maps the tile_id to the x, y, coordinates for the screen
    
    # Create the board as a list of GameTile Objects
    board = [GameTile(random.randint(0, 12),
                      random.randint(1,12),
                      random.choice(list(ResourceTile)), 4,
                      tile_id) for tile_id in legal_tile_ids()]

    # fill the tile_sprites list with the correct Gametile assets
    tile_sprites = []
    for gametile in board:
        image = pygame.image.load(gametile.tile.asset())
        image = pygame.transform.scale(image, (image.get_rect().width / 2.5,
                                               image.get_rect().height / 2.5))

        image.convert()
        rect = image.get_rect()
        rect.center = board_mapping['tiles'][gametile.tile_id]
        tile_sprites.append((image, rect))


    players = []

    for i in range(num_players):
        player = Player(player_names[i], colors[i] )
        print(player.name)
        players.append(player)

    return tile_sprites, board, board_mapping, players


def main_game_loop(**kwargs):
    GAME_RUNNING = True
    player_turn_index= 0
    current_player = players[player_turn_index]
      
    pprint(board)
    # GAME LOOP
    #1 LOOP THROUGH PLAYERS AND INITIALISE STARTING POSITIONS.
    #2 BEGIN MAIN TURN BASED LOOP.
    #2.1 PLAYER HAS CHOICE OF BUILDING AND

    while GAME_RUNNING:
        for event in pygame.event.get():
            if event.type == QUIT:
                GAME_RUNNING = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if player_turn_index == len(players)-1:
                    player_turn_index = 0
                    current_player = players[player_turn_index]
                else:
                    player_turn_index+=1
                    current_player = players[player_turn_index]

                dice_roll1, dice_roll2 = current_player.roll_dice(2)
                draw_dice(screen, dice_roll1, dice_roll2)
                

                for game_tile in board:
                    if dice_roll1+dice_roll2 == game_tile.real_number:
                        current_player.add_resources(game_tile)
                        game_log.append(f'{current_player.name} just rolled a {dice_roll1+dice_roll2}. Added {game_tile.tile.generate_resource().name()} to inventory')


            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_event(event, current_player) # handles clicking events
               
        

                
                
            elif event.type == pygame.MOUSEMOTION:
                mouse_motion_event() # function handles mouse motion events 
            
            

        if check_player_won():
            # draw_end_screen() # TODO
            GAME_RUNNING = False 
        
        draw(player_turn=current_player)
        pygame.display.update()
    pygame.quit()
    # this is a comment)

def mouse_motion_event():
    mouse_pos = pygame.mouse.get_pos()
    for button in node_buttons:
        button.is_hovered_over(mouse_pos)
    for button in tile_buttons:
        button.is_hovered_over(mouse_pos)

    build_road_button.is_hovered_over(mouse_pos)
    build_city_button.is_hovered_over(mouse_pos)
    build_settlement_button.is_hovered_over(mouse_pos)
    make_trade_button.is_hovered_over(mouse_pos)
    other_button_1.is_hovered_over(mouse_pos)
    other_button_2.is_hovered_over(mouse_pos)

    

        
    
def click_event(event, player):
    mouse_pos = pygame.mouse.get_pos()
    
            
    for button in tile_buttons:
        if button.is_clicked(mouse_pos):
            print(print(f'{button.x}, {button.y} clicked!'))
            break
    
    if build_road_button.is_clicked(mouse_pos):
       
        start_node = build_road()
        end_node = build_road()
        pygame.draw.line(screen, player.color,
                         board_mapping['nodes'][convert_to_nodeid(start_node.x, start_node.y)],
                         board_mapping['nodes'][convert_to_nodeid(end_node.x, end_node.y)],
                         5)
        pygame.display.update()
        
        game_log.append((f'{player.name} built road!'))


    elif build_settlement_button.is_clicked(mouse_pos):
    
        settlement_img = pygame.image.load('src\\assets\\buildings\\s_img.png')
        settlement_img = pygame.transform.scale(settlement_img, (50, 50))
        print(settlement_img)
        print("settlement build!")
        x, y = build_settlement()
    
        screen.blit(settlement_img, (x-30, y-20))
        game_log.append(f'{player.name} built settlement!')
        


    elif build_city_button.is_clicked(mouse_pos):
        print('city build')
    elif make_trade_button.is_clicked(mouse_pos):
        print('Trade Clicked')
    elif other_button_1.is_clicked(mouse_pos):
        print('other button 1 clicked')
    elif other_button_2.is_clicked(mouse_pos):
        print('other button 2 clicked')

    pygame.display.flip()

    

def build_settlement():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in node_buttons:
                    if button.is_clicked(mouse_pos):
                        return mouse_pos

def build_road():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in node_buttons:
                    if button.is_clicked(mouse_pos):
                        return button


def check_player_won():
    for player in players:
        if player.victory_points==10:
            return True
        
    return False
    
def calc_mouse_node(mouse_pos):
    '''
    calculates and returns the node mouse is hovering over

    Args:
        mouse_pos: x, y coordinates of the mouse click

    Returns:
        Node_id
    '''
    for node_id, node_point in board_mapping['nodes'].items():
                if ((node_point[0] - mouse_pos[0])**2 + (node_point[1] - mouse_pos[1])**2)**0.5 < 10 :
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    return node_id
    else:
         pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)



def calc_mouse_pos_tile(mouse_pos):
    """
    returns the tile that the mouse has clicked in

    Args:
        mouse_pos: x, y coordinates of the mouse click

    Returns:
        tile object from the Tiles class
    """
    x, y = mouse_pos
    hex_length = math.dist((621, 318), (699, 187))

    for tile_id in board_mapping['tiles']:
        coords = board_mapping['tiles'][tile_id]
        dist = math.sqrt((coords[0] - x)**2 + (coords[1] - y)**2) # dist between mouse click and center of tile
        radius = hex_length * math.sqrt(3) / 2
    
         # if the distance is less than or equal to the radius, the mouse click falls within the tile
        if dist <= radius:
            return board[tile_id-1]

def convert_to_nodeid( x, y):
        # converts the x, y coords of the node button to the nodeid stored in board_mapping
        for node_id, node_points in board_mapping['nodes'].items():
            if node_points[0] == x and node_points[1] == y:
                return node_id
        
        return None          
            

def draw(player_turn):
    """
    Draws the pygame display
    """
    screen.fill(Color("grey"))

    for img, rect in tile_sprites:
            screen.blit(img, rect)
        # screen.blit(bg_img, bg_rect)

    draw_lines() # draws game board lines
    
        
    for tile_number, coordinates in board_mapping['tiles'].items():
        # Create text surface
        text_surface = NUM_FONT.render(str(board[tile_number-1].real_number), True, WHITE)
    
        # Get size of text surface
        text_width, text_height = text_surface.get_size()
    
        # Calculate position to center text on tile
        x = coordinates[0] - text_width // 2
        y = coordinates[1] - text_height // 2
    
        # Draw text on screen
        screen.blit(text_surface, (x, y))

    
    draw_scoreboard(player_turn)
    draw_buttons()
    
    popup()


def draw_lines():
    for index in range(len(board)):
        
        pygame.draw.line(screen, 'white', board_mapping['nodes']
                            [board[index].node_coord_N], board_mapping['nodes'][board[index].node_coord_NW], 5)
        
        pygame.draw.line(screen, 'white', board_mapping['nodes']
                            [board[index].node_coord_N], board_mapping['nodes'][board[index].node_coord_NE], 5)
        
        pygame.draw.line(screen, 'white', board_mapping['nodes']
                            [board[index].node_coord_NW], board_mapping['nodes'][board[index].node_coord_SW], 5)

        pygame.draw.line(screen, 'white', board_mapping['nodes']
                            [board[index].node_coord_SW], board_mapping['nodes'][board[index].node_coord_S], 5)

        pygame.draw.line(screen, 'white', board_mapping['nodes']
                            [board[index].node_coord_S], board_mapping['nodes'][board[index].node_coord_SE], 5)
        
        pygame.draw.line(screen, 'white', board_mapping['nodes']
                            [board[index].node_coord_SE], board_mapping['nodes'][board[index].node_coord_NE], 5)

    

def draw_buttons():
    button_radius = [10, 22]
    GRAY = (158, 153, 134)
    RED = (255,0,0)
    for node_id, node_point in board_mapping['nodes'].items(): #draw node buttons
        button  = ButtonHex(node_point[0], node_point[1], button_radius[0], GRAY)
        button.draw(screen)
        node_buttons.append(button)
    
    for node_id, node_point in board_mapping['tiles'].items():
        button = ButtonHex(node_point[0], node_point[1], button_radius[1], WHITE, isFilled=False)
        tile_buttons.append(button)
        # invisible buttons at center of tiles

        
def draw_scoreboard(player_turn):
    """
    Draws the scoreboard as a seperate pygame surface
    """
    rect_width = DISPLAY_WIDTH-800
    rect_height = DISPLAY_HEIGHT

    rect_x = DISPLAY_WIDTH - rect_width
    rect_y = 0
    # create the rectangular surface
    rect_surf = pygame.Surface((rect_width, rect_height))
    rect_surf.fill((0, 120, 255))  # fill with blue color

    screen.blit(rect_surf, (rect_x, rect_y))

    rect_outline_width = 6
    scoreboard_width = rect_width-20
    scoreboard_outline = pygame.Rect(10, 10, scoreboard_width, 600)
    
    

    pygame.draw.rect(rect_surf, WHITE, scoreboard_outline, rect_outline_width)
    pygame.draw.line(rect_surf, WHITE, (10,80), (rect_width-10, 80), 6)
    pygame.draw.line(rect_surf, WHITE, (10, 160), (rect_width-10, 160), 6)
    pygame.draw.line(rect_surf, WHITE, (10, 430), (rect_width-10, 430), 6) # space for gamelog


        

    player_width = scoreboard_width//num_players
    font_size = 20 if len(players)==6 else 30 if len(players)==5 else 40
    player_font = pygame.font.SysFont('Palatino',font_size)

    for i in range(num_players): # draw player names at top of scoreboard
        x = 10 + i * player_width
        pygame.draw.line(rect_surf, WHITE, (x, 10), (x, 430), rect_outline_width)
        name =  player_font.render(players[i].name, True, WHITE)
        name_rect = name.get_rect(center=(x + player_width // 2, 40))
        rect_surf.blit(name, name_rect)
    
    for i in range(num_players): # draw victory points in each cell below player names
        x = 10 + i * player_width
        pygame.draw.line(rect_surf, WHITE, (10,510), (rect_width-10, 510), 6)
        name =  player_font.render(f'VP: {players[i].victory_points}', True, WHITE)
        name_rect = name.get_rect(center=(x + player_width // 2, 120))
        rect_surf.blit(name, name_rect)

    
    for i in range(len(game_log)): # draws game log text 
        game_log_text = game_log[-1] # most recent event
        game_log_text = GAME_LOG_FONT.render(game_log_text, True, WHITE)
        rect_surf.blit(game_log_text, (50, 460))
        screen.blit(rect_surf, (rect_x, rect_y))

    # player turn text being drawn
    player_turn_text = WORD_FONT.render(f'Current turn: {player_turn.name}', True, WHITE)
    rect_surf.blit(player_turn_text, (250, 540))
    screen.blit(rect_surf,(rect_x, rect_y))

def draw_dice(screen, roll_1, roll_2 ):
    # loading dice images
    DICE_SIZE = 80
    side_1 = pygame.image.load('src\\assets\dice\\1_sided.jpg')
    side_2 = pygame.image.load('src\\assets\dice\\2_sided.jpg')
    side_3 = pygame.image.load('src\\assets\dice\\3_sided.jpg')
    side_4 = pygame.image.load('src\\assets\dice\\4_sided.jpg')
    side_5 = pygame.image.load('src\\assets\dice\\5_sided.jpg')
    side_6 = pygame.image.load('src\\assets\dice\\6_sided.jpg')

    # scaling all to the same size

    side_1 = pygame.transform.scale(side_1, (DICE_SIZE, DICE_SIZE))
    side_2 = pygame.transform.scale(side_2, (DICE_SIZE, DICE_SIZE))
    side_3 = pygame.transform.scale(side_3, (DICE_SIZE, DICE_SIZE))
    side_4 = pygame.transform.scale(side_4, (DICE_SIZE, DICE_SIZE))
    side_5 = pygame.transform.scale(side_5, (DICE_SIZE, DICE_SIZE))
    side_6 = pygame.transform.scale(side_6, (DICE_SIZE, DICE_SIZE))



    if roll_1 ==1:
        screen.blit(side_1, (10, DISPLAY_HEIGHT-90))
        pygame.display.update()
    elif roll_1 == 2:
        screen.blit(side_2, (10, DISPLAY_HEIGHT-90))
        pygame.display.update()
    elif roll_1 == 3:
        screen.blit(side_3, (10, DISPLAY_HEIGHT-90))
        pygame.display.update()
    elif roll_1 == 4:
        screen.blit(side_4, (10, DISPLAY_HEIGHT-90))
        pygame.display.update()
    elif roll_1 == 5:
        screen.blit(side_5, (10, DISPLAY_HEIGHT-90))
        pygame.display.update()
    elif roll_1 == 6:
        screen.blit(side_6, (10, DISPLAY_HEIGHT-90))
        pygame.display.update()
    
    if roll_2 ==1:
        screen.blit(side_1, (130, DISPLAY_HEIGHT-90))
        pygame.display.update()
    elif roll_2 == 2:
        screen.blit(side_2, (130, DISPLAY_HEIGHT-90))
        pygame.display.update()
    elif roll_2 == 3:
        screen.blit(side_3, (130, DISPLAY_HEIGHT-90))
        pygame.display.update()
    elif roll_2 == 4:
        screen.blit(side_4, (130, DISPLAY_HEIGHT-90))
        pygame.display.update()
    elif roll_2 == 5:
        screen.blit(side_5, (130, DISPLAY_HEIGHT-90))
        pygame.display.update()
    elif roll_2 == 6:
        screen.blit(side_6, (130, DISPLAY_HEIGHT-90))
        pygame.display.update()

    pygame.display.update()




def popup():
    '''
    popup window that gives options for player when node is clicked
    '''
    
    popup_width = 630
    popup_height = 160

    popup_rect = pygame.Rect(810, 620, popup_width, popup_height)
    pygame.draw.rect(screen, (255, 255, 255), popup_rect)

    build_road_button = ButtonRect(830, 640, 190, 40,
                              'Build Road', WORD_FONT, WHITE, (17, 104, 245), WHITE)
    build_road_button.draw(screen)
    build_settlement_button = ButtonRect(830, 700, 190, 40,
                              'Build Settlement', WORD_FONT, WHITE,  (38, 140, 31), WHITE)
    build_settlement_button.draw(screen)
    build_city_button = ButtonRect(1030, 640, 190, 40,
                              'Build City', WORD_FONT, WHITE, (181, 186, 43) , WHITE)
    build_city_button.draw(screen)

    make_trade_button = ButtonRect(1030, 700, 190, 40,
                                   'Make Trade', WORD_FONT, WHITE, (255, 51, 153), WHITE)
    make_trade_button.draw(screen)
    
    other_button_1 = ButtonRect(1230, 640, 190, 40,
                                   'Other Button', WORD_FONT, WHITE, (51, 153, 255), WHITE)
    other_button_1.draw(screen)
    
    other_button_2 = ButtonRect(1230, 700, 190, 40,
                                   'Other Button', WORD_FONT, WHITE, (255, 153, 51), WHITE)
    other_button_2.draw(screen)
    make_trade_button.draw(screen)

    
    return build_road_button, build_settlement_button, build_city_button, make_trade_button, other_button_1, other_button_2

build_road_button, build_settlement_button, build_city_button, make_trade_button, other_button_1, other_button_2 = popup()

if __name__ == "__main__":
    tile_sprites, board, board_mapping, players = setup()
    main_game_loop(
        tile_sprites=tile_sprites,
        board=board,
        board_mapping=board_mapping,
        players=players
    )
