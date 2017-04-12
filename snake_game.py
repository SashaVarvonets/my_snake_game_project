# Snake Game!

# Imports for game
import pygame, sys, random, time

# Pygame initializing
check_errors = pygame.init()

# Game over function
def game_over():
	my_font = pygame.font.SysFont('monaco', 48)
	game_over_surf = my_font.render('Game over!',True, red)
	game_over_rect = game_over_surf.get_rect()
	game_over_rect.midtop = (window_height/2,window_width/10)
	play_surface.blit(game_over_surf,game_over_rect)
	show_score(0)
	show_level(0)
	pygame.display.flip()
	time.sleep(4)
	pygame.quit()
	sys.exit()

# Score function
def show_score(choice=1):
	score_font = pygame.font.SysFont('monaco', 20)
	score_surf = score_font.render('Score: {0}'.format(score),True, black)
	score_rect = score_surf.get_rect()
	if choice == 1:
		score_rect.midtop = (30,10)
	else:
		score_rect.midtop = (window_height/2,window_width/4)
	play_surface.blit(score_surf,score_rect)


def show_level(choice=1):
	score_font = pygame.font.SysFont('monaco', int(window_height/10))
	score_surf = score_font.render('Level: {0}'.format(level),True, black)
	score_rect = score_surf.get_rect()
	if choice == 1:
		score_rect.midtop = (30,30)
	else:
		score_rect.midtop = (window_height/2,window_width/3)
	play_surface.blit(score_surf,score_rect)

# Getting food function
def get_food():
	get_pos = [random.randrange(1,window_height/10)*10,\
			  random.randrange(1,window_width/10)*10]
	if get_pos in list(snake_body):
		return get_food()
	else:
		return get_pos

# Important variables
window_height = 150
window_width =100

snake_pos = [100,50]
snake_body = [[100,50],[90,50],[80,50]]

food_spawn = False

direction = 'RIGHT'
changeto = direction

speed = 5
rate = 5
score = 0
level = 1

# Play surface
play_surface = pygame.display.set_mode((window_height,window_width))
pygame.display.set_caption('Snake Game')

# Colors
red = pygame.Color(255,0,0) # Gameover
green = pygame.Color(0,255,0) #Snake body
dark_green = pygame.Color(0,150,0) #Snake head
black = pygame.Color(0,0,0) #Score and level
white = pygame.Color(255,255,255) #Background
brown = pygame.Color(165,42,42) #Food

# FPS controller
fps_controller = pygame.time.Clock()

# Main Logic of the game
while True:
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT or event.key == ord('d'):
				changeto = 'RIGHT'
			if event.key == pygame.K_LEFT or event.key == ord('a'):
				changeto = 'LEFT'
			if event.key == pygame.K_UP or event.key == ord('w'):
				changeto = 'UP'
			if event.key == pygame.K_DOWN or event.key == ord('s'):
				changeto = 'DOWN'
			if event.key == pygame.K_ESCAPE:
				pygame.event.post(pygame.event.Event(pygame.QUIT))



	# Validation of direction
	if changeto == 'RIGHT' and not direction == 'LEFT':
		direction = 'RIGHT'
	if changeto == 'LEFT' and not direction == 'RIGHT':
		direction = 'LEFT'
	if changeto == 'UP' and not direction == 'DOWN':
		direction = 'UP'
	if changeto == 'DOWN' and not direction == 'UP':
		direction = 'DOWN'

	# Update snake position[x,y]
	if direction == 'RIGHT':
		snake_pos[0] +=10
	if direction == 'LEFT':
		snake_pos[0] -= 10
	if direction == 'UP':
		snake_pos[1] -= 10
	if direction == 'DOWN':
		snake_pos[1] += 10

	# Food spawn
	if food_spawn == False:
		food_pos = get_food()
	food_spawn = True

	# Snake body mechanism
	snake_body.insert(0,list(snake_pos))
	if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
		score += 1
		food_spawn = False
	else:
		snake_body.pop()

	# Background
	play_surface.fill(white)



	# Draw Snake
	for pos in snake_body:
		pygame.draw.rect(play_surface, green,
		pygame.Rect(pos[0],pos[1],10,10))

	# Draw head
	pygame.draw.rect(play_surface, dark_green,
	pygame.Rect(snake_pos[0],snake_pos[1],10,10))

	# Draw Food
	pygame.draw.rect(play_surface, brown,
	pygame.Rect(food_pos[0],food_pos[1],10,10))

	# Bound
	if snake_pos[0] > window_height-10 or snake_pos[0] < 0:
		game_over()
	if snake_pos[1] > window_width-10 or snake_pos[1] < 0:
		game_over()

	for block in snake_body[1:]:
		if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
			game_over()

	# Increase speed
	if score  == speed*level:
		speed += 1
		level += 1
		

	show_score()
	show_level()
	pygame.display.flip()
	fps_controller.tick(speed)