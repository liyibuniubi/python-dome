import turtle as t
t.hideturtle()
t.speed(10)
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'violet']
def wjx(x,y,r,p,c): ## x,y为坐标，r为外接圆半径，p为相对y的正轴的逆时针偏移角度，c为颜色
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

for i in range(6):
    wjx(0,0,100,(i)*60,colors[i])
t.done()