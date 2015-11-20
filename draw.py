import pygame
import operator

def main():
    pygame.init()
    screen = pygame.display.set_mode((320, 240))
    clock = pygame.time.Clock()
    
    radius = 5
    x = 0
    y = 0
    mode = 'blue'
    points = []
    
    while True:
        
        pressed = pygame.key.get_pressed()
        
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.MOUSEMOTION:
              if event.buttons[0]:
                # if mouse moved, add point to list 
                position = event.pos
                points = points + [position]
                points = points[-500:]

            if event.type == pygame.MOUSEBUTTONUP:
	        pygame.quit()
                return points
            
        screen.fill((0, 0, 0))
        
        # draw all points 
        i = 0
        while i < len(points) - 1:
            drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
            i += 1
        
        pygame.display.flip()
        
        clock.tick(24)
def drawLineBetween(screen, index, start, end, width, color_mode):
    color = (255, 255, 255)
    
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in xrange(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = aprogress * start[0] + progress * end[0]
        y = aprogress * start[1] + progress * end[1]
        pygame.draw.circle(screen, color, (int(x), int(y)), width)

points = main()

# screen size 320 x 240
# dividing by a factor of 16
Matrix = [0 for x in range(20*15)]

i = 0
while i < len(points) - 1:
  x = int(points[i][0]/16)
  y = int(points[i][1]/16)
#  print "x: " + str(x) + " y: " + str(y)
  i += 1
  Matrix [ x + 20*y ] = 1

# initialise KNN
Knn = [[300 for x in range(4)] for x in range(10)]


num = 0

# computing K nearest neighbor
while num < 10:

  # Reading data file
  f = open("data_{}.dat".format(num),"r")
  line = f.readline()
  
  while line:
  
    # code for converting string to list
    line = line.strip('[')
    line = line.strip(']\n')
    line = line.split(",")
    data = [int(e) for e in line ] 
  
    # Distance between test and training set
    dist =  sum(map(operator.xor, Matrix, data))
    
    index = 0
    for x in Knn[num]:
      if dist < x:
        Knn[num][index] = dist
	break
      index += 1

    line = f.readline()

  f.close()
  num += 1  

# Voting function
num = 0
predicted_num = 0
minimum       = 1200 

while num < 10:
  
  total = sum(Knn[num])
  print str(num) + " : " +str(total)
  if total < minimum:
    minimum       = total
    predicted_num = num
  num += 1

print "My Prediction: " + str(predicted_num)

a = True

while a:

  check = raw_input('Is my prediction correct? (y/n):')

  if (check == "y"):
    print "YES!"
    a = False

  elif (check == "n"):
    predicted_num = input('Please enter the number: ')
    a = False

  else:
    print "You entered wrong input, please try again..."

if Knn[predicted_num][0] != 0:
  with open("data_{}.dat".format(predicted_num), "a") as myfile:
    myfile.write(str(Matrix) + "\n")
