import pygame
import time
import random
import sys 
from pygame.locals import *
from sys import exit

def collide(x1, x2, y1, y2, w1, w2, h1, h2):
	if x1+w1 > x2 and x1 < x2+w2 and y1+h1 > y2 and y1 < y2+h2:
		return True
	else:
		return False

def die(screen, score):
	f = pygame.font.SysFont('Chiller', 70)
	t = f.render('Game Over!!!', True, (255, 255, 255))
	t1 = f.render('Your score: '+str(score), True, (255, 255, 255))
	screen.blit(t, (150, 200))
	screen.blit(t1, (135, 270))

	f = pygame.font.SysFont('Chiller', 25)
	t = f.render('Press q to exit the game. Any Other Key to Play ', True, (255, 255, 255))
	screen.blit(t, (170, 350))


	fo = open("high_score.txt", "r")
	hs = fo.read(3)
	fo.close()
	if score > int(hs):
		fo = open("high_score.txt", "w")
		fo.write(str(score))
		fo.close()

		fo = open("high_score.txt", "r")
		hs = fo.read(4)
		fo.close()

		blackbox = pygame.Surface((40, 20))
		blackbox.fill((0, 0, 0))
		screen.blit(blackbox, (560, 10))

		f = pygame.font.SysFont('Chiller', 20)
		t = f.render('High score: '+str(hs), True, (255, 255, 255))
		screen.blit(t, (490, 10))

		f = pygame.font.SysFont('Chiller', 35)
		t = f.render('Congrats!!!', True, (255, 255, 255))
		screen.blit(t, (220, 70))

		f = pygame.font.SysFont('Chiller', 35)
		t = f.render('You have a new High score...', True, (255, 255, 255))
		screen.blit(t, (140, 100))

		pygame.mixer.music.load('applause.wav')
		pygame.mixer.music.play(1, 0.0)
	else:
		pygame.mixer.music.load('gameover.wav')
		pygame.mixer.music.play(0, 0.0)

	pygame.time.wait(2000)
	pygame.display.update()
	while True:
		for e in pygame.event.get():
			if e.type == pygame.quit:
				pygame.quit()
				sys.exit(0)
			elif e.key == K_q:
				pygame.quit()
				sys.exit(0)
			elif e.key == K_UP or K_DOWN or K_LEFT or K_RIGHT:
				play_again()
				

        

def levelComplete(screen, score):
	blackbox = pygame.Surface((40, 20))
	blackbox.fill((0, 0, 0))
	screen.blit(blackbox, (300, 10))

	f = pygame.font.SysFont('Chiller', 20)
	t = f.render('Level '+str(level)+'Score: '+str(score), True, (255, 255, 255))
	screen.blit(t, (10, 10))

	f = pygame.font.SysFont('Chiller', 70)
	t = f.render('Level '+str(level)+' Complete!!!', True, (255, 255, 255))
	screen.blit(t, (100, 130))
	t1 = f.render('Your score: '+str(score), True, (255, 255, 255))
	screen.blit(t1, (150, 270))
	pygame.mixer.music.load('applause.wav')
	pygame.mixer.music.play(0, 0.0)
	pygame.display.update()
	pygame.time.wait(3000)

def play_again():
	xs = [290, 290, 290, 290, 290]
	ys = [290, 270, 250, 230, 210]
	dirs = 0
	score = 0
	global level
	level = 1
	prevLevelScore = 0
	applepos = (random.randint(0, 590), random.randint(0, 590))
	pygame.init()
	s = pygame.display.set_mode((600, 600))
	pygame.display.set_caption('Snake')
	appleimage = pygame.image.load('apple.bmp')
	appleimage = pygame.transform.scale(appleimage, (20, 15))
	img = pygame.Surface((15, 15))
	img.fill((255, 0, 0))
	img1 = pygame.Surface((20, 20))
	img1.fill((0, 0, 200))
	f = pygame.font.SysFont('Chiller', 20)
	clock = pygame.time.Clock()
	
	while True:	
		clock.tick(9+level)
		for e in pygame.event.get():
			if e.type == QUIT:
				pygame.quit()
				sys.exit(0)
			elif e.type == KEYDOWN:
				if e.key == K_UP and dirs != 0:
					dirs = 2
				elif e.key == K_DOWN and dirs != 2:
					dirs = 0
				elif e.key == K_LEFT and dirs != 1:
					dirs = 3
				elif e.key == K_RIGHT and dirs != 3:
					dirs = 1
		i = len(xs)-1
		while i >= 2:
			if collide(xs[0], xs[i], ys[0], ys[i], 20, 20, 20, 20):
				die(s, score)
			i-= 1
			
		if collide(xs[0], applepos[0], ys[0], applepos[1], 20, 10, 20, 10):
			score += 10;
			pygame.mixer.music.load('eat.wav')
			pygame.mixer.music.play(0, 0.0)
			xs.append(700)
			ys.append(700)
			if score >= prevLevelScore+60:
				prevLevelScore = score
				levelComplete(s, score)
				level = level+1
			applepos = (random.randint(0,590),random.randint(0,590))
			
		if xs[0] < 0 or xs[0] > 580 or ys[0] < 0 or ys[0] > 580:
			die(s, score)
			
		i = len(xs)-1
		
		while i >= 1:
			xs[i] = xs[i-1];
			ys[i] = ys[i-1];
			i -= 1
			
		if dirs == 0:
			ys[0] += 20
		elif dirs == 1:
			xs[0] += 20
		elif dirs == 2:
			ys[0] -= 20
		elif dirs == 3:
			xs[0] -= 20
			
		s.fill((0, 0, 0))
		
		for i in range(0, len(xs)):
			s.blit(img, (xs[i], ys[i]))
			
		s.blit(appleimage, applepos)
		t=f.render('Level '+str(level)+'Score: '+str(score), True, (255, 255, 255))
		s.blit(t, (10, 10))

		fo = open("high_score.txt", "r")
		hs = fo.read(3)
		fo.close()

		f = pygame.font.SysFont('Chiller', 20)
		t = f.render('High score: '+str(hs), True, (255, 255, 255))
		s.blit(t, (490, 10))
		
		pygame.display.update()


play_again()




