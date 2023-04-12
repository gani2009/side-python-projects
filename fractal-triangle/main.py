import turtle

# define recursive function to draw Sierpiński triangle
def draw_triangle(length, depth):
    if depth == 0:
        for i in range(3):
            turtle.forward(length)
            turtle.left(120)
    else:
        draw_triangle(length/2, depth-1)
        turtle.forward(length/2)
        draw_triangle(length/2, depth-1)
        turtle.backward(length/2)
        turtle.left(60)
        turtle.forward(length/2)
        turtle.right(60)
        draw_triangle(length/2, depth-1)
        turtle.left(60)
        turtle.backward(length/2)
        turtle.right(60)

# set up Turtle graphics window
turtle.speed(0)
turtle.penup()
turtle.goto(-200, -200)
turtle.pendown()

# call recursive function to draw Sierpiński triangle
draw_triangle(400, 5)

# hide Turtle graphics cursor when finished
turtle.hideturtle()

# keep window open until closed by user
turtle.mainloop()