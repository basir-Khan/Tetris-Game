import pygame,sys
from game import Game
from colors import Colors
import mysql.connector


pygame.init()
game = Game()

mydb=mysql.connector.connect(
	                         host='localhost',
	                         user = 'root',
	                        passwd='1234',
	                        database ='scores',
							 )
mycursor=mydb.cursor() #initialize cursor
sqlFormla='INSERT INTO tetris_score (tgscore) VALUES (%s)'
mycursor.execute("SELECT MAX(tgscore) FROM tetris_score")
a=mycursor.fetchone() #get the max value
max_score=int(a[0])

title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)
highest_score_surface = title_font.render("higest score", True, Colors.white)
highest_score_value_surface = title_font.render(str(max_score), True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 210, 170, 160)
highest_score_rect=pygame.Rect(320,450,170,150)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")
clock = pygame.time.Clock()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 300)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if game.game_over == True:
				print(game.score)
				scr=(game.score,) #get the final score
				mycursor.execute(sqlFormla,scr)
				mydb.commit()
				game.game_over = False
				game.reset()
			if event.key == pygame.K_LEFT and game.game_over == False:
				game.move_left()
			if event.key == pygame.K_RIGHT and game.game_over == False:
				game.move_right()
			if event.key == pygame.K_DOWN and game.game_over == False:
				game.move_down()
				game.update_score(0, 1)
			if event.key == pygame.K_UP and game.game_over == False:
				game.rotate()
		if event.type == GAME_UPDATE and game.game_over == False:
			game.move_down()

	#Drawing
	score_value_surface = title_font.render(str(game.score), True, Colors.white)

	screen.fill(Colors.dark_blue)
	screen.blit(score_surface, (365, 20, 50, 50))
	screen.blit(next_surface, (375, 180, 50, 50))

	if game.game_over == True:
		screen.blit(game_over_surface, (320, 395, 50, 50))

	pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
	pygame.draw.rect(screen, Colors.light_blue,highest_score_rect,0,10 )
	screen.blit(highest_score_surface, (324, 460, 50, 50))

	screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx,
		centery = score_rect.centery))
	screen.blit(highest_score_value_surface, highest_score_value_surface.get_rect(centerx=highest_score_rect.centerx,
		 centery=highest_score_rect.centery))

	pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
	game.draw(screen)

	pygame.display.update()
	clock.tick(60)
