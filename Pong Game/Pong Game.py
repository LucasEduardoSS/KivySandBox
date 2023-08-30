from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):

    # Velocidade da bola nos eixos x e y
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # Propriedade ReferenceListProperty para usar as velocity
    # como uma shorthand
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # Função "move" irá mover a bola um passo. Será chamada
    # em intervalos iguais para animar a bola
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        # Define a posição da bola no centro da tela
        self.ball.center = self.center
        # Defina a velocidade da bola
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # Raquetes
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # Faz a bola quicar de cima para baixo
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # Verifica se a bola encostou em um canto para pontuar
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))

        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):

        # Verifica qual raquete mover
        if touch.x < self.width / 3:  # Move a raquete da esquerda
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:  # Move a raquete da direita
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
