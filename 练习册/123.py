import turtle as t
t.speed(10)
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
def fun(t):
    for _ in range(12):
        t.fillcolor(colors[_%6])
        t.pencolor(colors[_ % 6])
        t.begin_fill()
        for i in range(4):
            t.fd(50)
            if i%2 == 0:
                t.lt(60)
            else :
                t.lt(120)
        t.rt(30)
        t.end_fill()
fun(t)
t.done()