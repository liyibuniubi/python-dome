import turtle as t
t.hideturtle()
t.speed(10)

t.penup()
t.goto(-150,-100)
t.pendown()

t.pencolor('red')
t.fillcolor('red')
t.begin_fill()
for i in range(2):
    t.fd(300)
    t.lt(90)
    t.fd(200)
    t.lt(90)
t.end_fill()

def wjx(x,y,r,p,c):
    p=(p+360)%360
    t.penup()
    t.pencolor(c)
    b=0.8507*r
    t.goto(x, y)
    t.pendown()
    t.setheading(90+p)
    t.fd(r)
    t.lt(180)
    t.lt(18.5)
    t.fd(b)
    t.fillcolor(c)
    t.begin_fill()
    for i in range(5):
        t.lt(72)
        t.fd(b)
        t.rt(144)
        t.fd(b)
    t.end_fill()

wjx(-100, 50, 30, 0, 'yellow')
wjx(-50, 80, 10, 108.44, 'yellow')
wjx(-30, 60, 10, 123.69, 'yellow')
wjx(-30, 30, 10, 146.31, 'yellow')
wjx(-50, 10, 10, 161.57, 'yellow')

t.done()