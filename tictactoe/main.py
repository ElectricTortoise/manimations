from manim import *
import random as Rand
import game


class Play(Scene):
    def construct(self):
        intro = Tex(r"My first manimation")
        self.play(Write(intro))
        self.play(Unwrite(intro))

        circle = Circle(radius=0.9, color=BLUE)
        cross = Cross(stroke_width=2, scale_factor=0.9)

        animatedBoard = VGroup(
            [Square(side_length=2) for _ in range(9)]
        ).arrange_in_grid(rows=3,cols=3,buff=0)

        self.play(Create(animatedBoard))
        self.wait(2)

        internalBoard = game.Board()
        counter = 0
        while (not internalBoard.gameOver and counter < 9):
            square = Rand.randint(0,8)
            if internalBoard.board[square] != 0:
                continue
            internalBoard.MakeMove(square)
            counter += 1

            row = square // 3
            col = square % 3

            if internalBoard.player == 1:
                self.play(Create(circle.copy().shift((row-1)*2*UP + (col-1)*2*RIGHT)))
            elif internalBoard.player == -1:
                self.play(Create(cross.copy().shift((row-1)*2*UP + (col-1)*2*RIGHT)))
            else:
                pass
        
        self.next_section()
        self.wait()
        gameOverText = Tex(r"Game Over!").shift(UP*3.6)

        self.play(Write(gameOverText))
                
        winnerText = Tex(r"wins!")
        if internalBoard.player == 1:
            winner = circle.copy().scale(0.25)
        elif internalBoard.player == -1:
            winner = cross.copy().scale(0.25)
        else:
            winnerText = Tex(r"Draw!")
        winner.next_to(winnerText, LEFT, buff=0.25)
        winnerGroup = VGroup(winner, winnerText).center().to_edge(DOWN, buff=0.25)
        self.play(Create(winnerGroup))