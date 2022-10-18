import pygame, random, time

pygame.init()

WIDTH, HEIGHT = 640, 480

win = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

run = True
start = True
WHITE = (255,255,255)
BLACK = (0,0,0)

n = 4
w = WIDTH//n
h_arr = []
states = []

for i in range(w):
	height = random.randint(10, 450)
	h_arr.append(height)
	states.append(1)

counter = 0



while run:
	if start:
		time.sleep(1)
		start = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	win.fill(BLACK)

	if counter < len(h_arr):
		for j in range(len(h_arr) - 1 - counter):
			if h_arr[j] > h_arr[j + 1]:
				states[j] = 0
				states[j + 1] = 0
				temp = h_arr[j]
				h_arr[j] = h_arr[j+1]
				h_arr[j+1] = temp
			else:
				states[j] = 1
				states[j + 1] = 1
	counter += 1

	if len(h_arr) - counter >= 0:
		states[len(h_arr) - counter] = 2

	for i in range(len(h_arr)):
		if states[i] == 0:
			color = (255, 0, 0)
		elif states[i] == 2:
			color = (0, 255, 0)
		else:
			color = WHITE

		pygame.draw.rect(win, color, pygame.Rect(int(i*n), HEIGHT - h_arr[i], n, h_arr[i]))
	
	pygame.display.flip()

	clock.tick(60)

pygame.quit()