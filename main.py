#Space Invaders - Part 1
#from turtle import Turtle, Screen, listen, onkey, register_shape
import  turtle
import  math
import  random
import  winsound

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space invaders")
wn.bgpic("Immagini/space_invaders_background.gif")
canvas = wn.getcanvas()
root = canvas.winfo_toplevel()


def on_close():
    global running
    running = False

root.protocol("WM_DELETE_WINDOW", on_close())
running = True

#register shape
turtle.register_shape("Immagini/invader.gif")
turtle.register_shape("Immagini/player.gif")

border_pen = turtle.Turtle()
border_pen.speed("fastest")
border_pen.color("white")
border_pen.pensize(3)

border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()

for side in range(4):
    border_pen.forward(600)
    border_pen.left(90)

border_pen.hideturtle()

#score
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: %s" %score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()
fine = False
#Player turtle
player= turtle.Turtle()
player.color("blue")
player.shape("Immagini/player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)
#MOVING
playerspeed = 15



#number of enemy
number_of_enemies = 5
#empty list of enemy
enemies = []

#Add enemies to the list
for i in range(number_of_enemies):
    # Create enemy
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.color("red")
    enemy.shape("Immagini/invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)

enemyspeed = 2

#Create weapon bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle()

bulletspeed = 20

#define bullet state
bulletstate = "ready"



def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = -280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    #declare bulletstate as global if need changes
    global bulletstate
    if bulletstate == "ready":
        winsound.PlaySound("Suoni/laser",winsound.SND_ASYNC)
        bulletstate = "fire"
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x,y)
        bullet.showturtle()

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2) + math.pow(t1.ycor()- t2.ycor(),2))
    if distance < 15:
        winsound.PlaySound("Suoni/explosion", winsound.SND_ASYNC)
        return True
    else:
        return False

#key board binding
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")
turtle.onkey(on_close, "x" )

#Main game loop

while running:
    for enemy in enemies:
        #move enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        #move enemy back down
        if enemy.xcor()>280 :
            for e in enemies:
                #drop down all enemies
                y = enemy.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *= -1

        if enemy.xcor()< -280:
            for e in enemies:
                #drowp down all enemies
                y = enemy.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *= -1

            # check for collision
        if isCollision(bullet, enemy):
            # reset bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            # reset enemy
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)
            #update score
            score += 10
            scorestring = "Score: %s" %score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))


        if isCollision(player, enemy):
            player.hideturtle()
            enemy.hideturtle()
            fine = True
            break
    if fine:
        print("Game Over")
        break

    #move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    #check bullet
    if bullet.ycor()>275:
        bullet.hideturtle()
        bulletstate = "ready"

