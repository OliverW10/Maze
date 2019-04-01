import pygame
import math
import random
import time
import numpy
i = input("Line of sight stuff(y or n): ")
if i == "y":
	showMaze = False
else:
	showMaze = True
displayWidth, displayHeight = 800, 600
pygame.init()
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("maze game")
clock = pygame.time.Clock()

def line_intersection(line1, line2): # copied from stack overflow
	xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
	ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

	def det(a, b):
		return a[0] * b[1] - a[1] * b[0]

	div = det(xdiff, ydiff)
	if div == 0:
	   return False

	d = (det(*line1), det(*line2))
	x = det(d, xdiff) / div
	y = det(d, ydiff) / div
	return x, y

def generateMaze(width, height):
	lastPrint = 0.0
	mazeArray = numpy.ones((width*2, height*2))
	pathTaken = [(0, 0)]
	allVisited = [(0, 0)]
	mazeArea = width*height
	while len(allVisited) < mazeArea:
		allNeighbours = [(pathTaken[-1][0], pathTaken[-1][1]+1),
		(pathTaken[-1][0]+1, pathTaken[-1][1]),
		(pathTaken[-1][0]-1, pathTaken[-1][1]),
		(pathTaken[-1][0], pathTaken[-1][1]-1)]

		validNeighbours = []
		for i in range(len(allNeighbours)):
			if allNeighbours[i][0] >= 0 and allNeighbours[i][0] < width and allNeighbours[i][1] >= 0 and allNeighbours[i][1] < height and allNeighbours[i] not in allVisited:
				validNeighbours.append(allNeighbours[i])

		if len(validNeighbours) > 0:
			nextStep = random.choice(validNeighbours)
			pathTaken.append(nextStep)
			allVisited.append(nextStep)
			mazeArray[nextStep[0]*2][nextStep[1]*2] = 0
			mid = ((pathTaken[-1][0]+pathTaken[-2][0]), (pathTaken[-1][1]+pathTaken[-2][1]))
			mid = (round(mid[0]), round(mid[1]))
			mazeArray[mid[0]][mid[1]] = 0
		else:
			del pathTaken[-1]
		donePer = len(allVisited)/mazeArea
		if donePer > lastPrint:
			print(round(donePer, 2))
			lastPrint = donePer + 0.001
	return mazeArray

def generateLines(mazeBlockMap):
	rectList = []
	vertexList = []
	for x in range(len(mazeBlockMap)):
		for y in range(len(mazeBlockMap[x])):
			if maze[x][y] == 1:
				if len(mazeBlockMap[x]) > y-1:
					N = mazeBlockMap[x][y-1]
				else:
					N = 1
				if len(mazeBlockMap[x]) > y+1:
					S = mazeBlockMap[x][y+1]
				else:
					S = 1
				if len(mazeBlockMap) > x+1:
					E = mazeBlockMap[x+1][y]
				else:
					E = 1
				if len(mazeBlockMap) > x-1:
					W = mazeBlockMap[x-1][y]
				else:
					W = 1

				rectList.append(pygame.Rect(x*50, y*50, 50, 50))

				if N == 0 and E == 0:
					vertexList.append(((x+1)*50, y*50))
				if E == 0 and S == 0:
					vertexList.append(((x+1)*50, (y+1)*50))
				if S == 0 and W == 0:
					vertexList.append((x*50, (y+1)*50))
				if W == 0 and N == 0:
					vertexList.append((x*50, y*50))
				
				if N == 1 and E == 1:
					vertexList.append(((x+1)*50, y*50))
				if E == 1 and S == 1:
					vertexList.append(((x+1)*50, (y+1)*50))
				if S == 1 and W == 1:
					vertexList.append((x*50, (y+1)*50))
				if W == 1 and N == 1:
					vertexList.append((x*50, y*50))

	return rectList, vertexList

def onScreen(X, Y):
	if X > -100 and X < displayWidth+100 and Y > -100 and Y < displayHeight+100:
		return True
	else:
		return False

def dist(x1, y1, x2, y2):
	xdif = x1-x2
	ydif = y1-y2
	return math.hypot(xdif, ydif)
mazeSize = (80, 60) #160, 120 is the normal
maze = generateMaze(mazeSize[0], mazeSize[1])
shadowRects, shadowPoints = generateLines(maze)

mazeSurf = pygame.Surface(((mazeSize[0]*2+1)*50, (mazeSize[1]*2+1)*50))
mazeSurf.fill((255, 255, 255))
for x in range(len(maze)):
	#pygame.draw.rect(mazeSurf, (0,0,0), (x*50, 0, 50 ,50))
	#pygame.draw.rect(mazeSurf, (0,0,0), (x*50, len(maze[x])*50, 50 ,50))
	for y in range(len(maze[x])):
		if maze[x][y] == 1:
			pygame.draw.rect(mazeSurf, (0,0,0), (x*50, y*50, 50, 50))

for i in range(len(shadowPoints)):
	pygame.draw.circle(mazeSurf, (0, 0, 255), (shadowPoints[i][0], shadowPoints[i][1]), 10)

playerPos = [0, 0] #goes from 0 - 50
playerSquare = [0,0] #the square the player is in
Keys = {"W": False, "A": False, "S": False, "D": False, "E": False, "Esc" : False, "Space" : False}

while True:
	startFrame = time.time()
	gameDisplay.fill((0, 0, 0))
	mousePos = pygame.mouse.get_pos()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				Keys["W"] = True
			if event.key == pygame.K_a:
				Keys["A"] = True
			if event.key == pygame.K_s:
				Keys["S"] = True
			if event.key == pygame.K_d:
				Keys["D"] = True
			if event.key == pygame.K_f:
				print(clock.get_fps())
			if event.key == pygame.K_ESCAPE:
				Keys["Esc"] = True
			if event.key == pygame.K_SPACE:
				Keys["Space"] = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				Keys["W"] = False
			if event.key == pygame.K_a:
				Keys["A"] = False
			if event.key == pygame.K_s:
				Keys["S"] = False
			if event.key == pygame.K_d:
				Keys["D"] = False
			if event.key == pygame.K_ESCAPE:
				Keys["Esc"] = False
			if event.key == pygame.K_SPACE:
				Keys["Space"] = False

	if Keys["D"] == True:
		playerPos[0] -= frameTime * 100

	if Keys["A"] == True:
		playerPos[0] += frameTime * 100

	if Keys["W"] == True:
		playerPos[1] += frameTime * 100

	if Keys["S"] == True:
		playerPos[1] -= frameTime * 100

	if showMaze == True:
		gameDisplay.blit(mazeSurf, (playerPos[0], playerPos[1]))

	shadowDrawPoints = []

	for i in range(len(shadowPoints)):
		pointX = shadowPoints[i][0]+playerPos[0]
		pointY = shadowPoints[i][1]+playerPos[1]
		if onScreen(pointX, pointY):
			xDif = pointX - displayWidth/2
			yDif = pointY - displayHeight/2


			angle = math.atan2(yDif, xDif) + math.pi/2
			angle -= 0.02
			xVel = math.sin(angle) *2
			yVel = -math.cos(angle) *2
			x = -playerPos[0] + displayWidth/2
			y = -playerPos[1] + displayHeight/2
			while maze[math.floor(x/50)][math.floor(y/50)] == 0:
				x+=xVel
				y+=yVel
			shadowDrawPoints.append((x, y, angle))

			angle = math.atan2(yDif, xDif) + math.pi/2
			angle += 0.02
			xVel = math.sin(angle) *2
			yVel = -math.cos(angle) *2
			x = -playerPos[0] + displayWidth/2
			y = -playerPos[1] + displayHeight/2
			while maze[math.floor(x/50)][math.floor(y/50)] == 0:
				x+=xVel
				y+=yVel
			shadowDrawPoints.append((x, y, angle))

	'''
	for i in range(360):
		angle = (i/360)*math.pi*2
		xVel = math.sin(angle) * 2 
		yVel = -math.cos(angle) * 2
		x = -playerPos[0] + displayWidth/2
		y = -playerPos[1] + displayHeight/2
		while maze[math.floor(x/50)][math.floor(y/50)] == 0:
			x+=xVel
			y+=yVel
		shadowDrawPoints.append((x, y, angle))
	'''

	shadowDrawPoints.sort(key = lambda x : x[2])
	for i in range(len(shadowDrawPoints)-1, -1, -1):
		#pygame.draw.circle(gameDisplay, (0, 255, 255), (round(shadowDrawPoints[i][0]), round(shadowDrawPoints[i][1])), 3)
		pygame.draw.polygon(gameDisplay, (255, 255, 100), [(shadowDrawPoints[i][0]+playerPos[0], shadowDrawPoints[i][1]+playerPos[1]),(shadowDrawPoints[i-1][0]+playerPos[0], shadowDrawPoints[i-1][1]+playerPos[1]),(displayWidth/2, displayHeight/2)])

	pygame.draw.circle(gameDisplay, (255, 0, 0), (round(displayWidth/2), round(displayHeight/2)), 10)
	pygame.display.update()
	clock.tick()
	frameTime = time.time() - startFrame
