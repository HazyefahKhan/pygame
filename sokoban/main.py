import pygame

class Sokoban:
    
    # class constructor
    def __init__(self):
        # initialize pygame module
        pygame.init()

        # load images used in game into list called "images"
        self.load_images()
        # creates 2d list name containing the initial state of game
        self.new_game()


        # initialize height and width per dimensions of game grid
        self.height = len(self.map)
        self.width = len(self.map[0])
        # length of a square grid
        self.scale = self.images[0].get_width()

        window_height = self.scale * self.height
        window_width = self.scale * self.width
        self.window = pygame.display.set_mode((window_width,  window_height + self.scale))
        self.game_font = pygame.font.SysFont("Arial", 24)

        pygame.display.set_caption("Sokoban")

        self.main_loop()
    
    # load all images to be used in game
    def load_images(self):
        self.images = []
        # images used can be found in program file
        for name in ["floor", "wall", "target", "box", "robot", "done", "target_robot"]:
            self.images.append(pygame.image.load(name + ".png"))
    
    # create initial state of game grid
    def new_game(self):
        # initialize 2d list map]
        # numbered position of images list correspond to position in grid
        self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                    [1, 2, 3, 0, 0, 0, 1, 0, 0, 1, 2, 3, 0, 0, 0, 0, 1],
                    [1, 0, 0, 1, 2, 3, 0, 2, 3, 0, 0, 0, 1, 0, 0, 0, 1],
                    [1, 0, 4, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        # move count initialized to 0 at start of game
        self.moves = 0

    # through each iteration call check_events() and draw_window()
    def main_loop(self):
        while True:
            # go through any new event since last iteration
            self.check_events()
            # update windows content
            self.draw_window()
    
    def check_events(self):
        for event in pygame.event.get():
            # when player presses arrow key, move character in appropriate direction
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move(0, -1)
                if event.key == pygame.K_RIGHT:
                    self.move(0, 1)
                if event.key == pygame.K_UP:
                    self.move(-1, 0)
                if event.key == pygame.K_DOWN:
                    self.move(1, 0)
                    
                # F2 key starts new game
                if event.key == pygame.K_F2:
                    self.new_game()
                # ESC key exits game
                if event.key == pygame.K_ESCAPE:
                    exit()
                    
            # Close game window
            if event.type == pygame.QUIT:
                exit()
    
    
    def draw_window(self):
        self.window.fill((0, 0, 0))

        # traverse game grind and draw corresponding image to grid location
        for y in range(self.height):
            for x in range(self.width):
                square = self.map[y][x]
                self.window.blit(self.images[square], (x * self.scale, y *self.scale))

        # updates moves taken counter
        game_text = self.game_font.render("Moves: " + str(self.moves), True, (255, 0, 0))
        self.window.blit(game_text, (25, self.height * self.scale + 10))

        # information for functionality of keys
        game_text = self.game_font.render("F2 = new game", True, (255, 0, 0))
        self.window.blit(game_text, (200, self.height * self.scale + 10))

        game_text = self.game_font.render("Esc = exit game", True, (255, 0, 0))
        self.window.blit(game_text, (400, self.height * self.scale + 10))

        # Displays if player has won game
        if self.game_solved():
            game_text = self.game_font.render("Congratulations, you solved the game!", True, (255, 0, 0))
            game_text_x = self.scale * self.width / 2 - game_text.get_width() / 2
            game_text_y = self.scale * self.height / 2 - game_text.get_height() / 2
            pygame.draw.rect(self.window, (0, 0, 0), (game_text_x, game_text_y, game_text.get_width(), game_text.get_height()))
            self.window.blit(game_text, (game_text_x, game_text_y))

        pygame.display.flip()
    
    # find location of robit
    def find_robot(self):
        # go through game grid and return coordinates of square that contains robot
        # 4 represents robot on its own, 6 represents robot on a target square
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] in [4, 6]:
                    return (y, x)
    
    # take direction indicated by playyer and move to those coordinates
    # updates grid accordingly if move possible
    def move(self, move_y, move_x):

        # can no longer move if player has solved game
        if self.game_solved():
            return

        # call find_robot method to find current location of robot
        # store current location in robot_old_y, robot_old_x
        robot_old_y, robot_old_x = self.find_robot()
        # calculate new robot position by adding current location to to location passed by method
        robot_new_y = robot_old_y + move_y
        robot_new_x = robot_old_x + move_x

        # return w/o changes if robot hits a will (1 represents position of wall square)
        if self.map[robot_new_y][robot_new_x] == 1:
            return

        # if location of robot is a box (3) or target box(5), attempt to move box to next square
        if self.map[robot_new_y][robot_new_x] in [3,5]:
            # location of box after being moved
            box_new_y = robot_new_y + move_y
            box_new_x = robot_new_x + move_x

            # return w/o changes if box is moved into wall (1) or another box(3) or target box(5)
            if self.map[box_new_y][box_new_x] in [1, 3, 5]:
                return
            
            # box can be sucessfully moved
            self.map[robot_new_y][robot_new_x] -=3
            self.map[box_new_y][box_new_x] +=3

        # move robot correspondly
        self.map[robot_old_y][robot_old_x] -= 4
        self.map[robot_new_y][robot_new_x] += 4

        # increase move counter
        self.moves += 1

    # checks to see if game has been solved
    def game_solved(self):

        # go through game grid
        for y in range(self.height):
            for x in range(self.width):
                # if grid still contains empty target square (2) or robot in a target square (6), game is not solved
                if self.map[y][x] in [2, 6]:
                    return False
        # if all target squares are occupied return True
        return True

if __name__ == "__main__":
    Sokoban()           

            

    
    



