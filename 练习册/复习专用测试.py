import turtle as t
t.hideturtle()
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


t.done()