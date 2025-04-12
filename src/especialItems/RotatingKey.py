from typing import Any
from src.GameItem import GameItem
from src.Player import Player
import settings
import pygame
import math

class RotatingKey(GameItem):

    def __init__(self, x: int, y: int, game_level) -> None:
        super().__init__(
            collidable=True,
            consumable=True,
            x=x,
            y=y + 10,
            width=settings.KEY_WIDTH,
            height=settings.KEY_HEIGHT,
            texture_id="key",
            frame_index=0,
            solidness=False
        )

        # Guardamos la textura de la llave
        self.texture = settings.TEXTURES["key"]
        # Especificamos si esta acitva o no (para verificar si se puede recoger o ya se consumio)
        self.is_active = True
        self.game_level = game_level
        # Posicion original de la llave porque le agregaremos un salto
        self.original_y = y
        # Asignamos velocidad negativa para controlar velocidad de caida
        self.jump_velocity = -settings.GRAVITY / 5

        # Por defecto tendra estado saltando porque al crearse se creara saltando
        # los estados son idle, jumping y falling igual que el player para controlar su salto
        self.state = "Jumping" 
        self.vy = self.jump_velocity


        # timer_rotation controlara que tan rapido hara la rotacion para el giro de la imagen
        self.timer_rotation = 0.005
        # determinara el factor de giro para la imagen
        self.rotation_factor = 0
        # aqui calculamos la escala que tendra el acho durante la rotacion dependendiendo del factor de rotacion (como se vera la imagen reescalada)
        self.scale_rotation = 0

    def get_collision_rect(self) -> pygame.Rect:
        # recalculamos el rectangulo de colision para que sea mas peque;o
        colliision_width = self.width * 0.3
        colliision_height = self.height 
        # calculamos el offset de la posicion inicial del rectangulo de colision de la llave
        x_offset = (self.width - colliision_width) / 2
        y_offset = (self.height - colliision_height) / 2

        return pygame.Rect(self.x + x_offset , self.y + y_offset , colliision_width , colliision_height )
    
    def update(self, dt: float) -> None:
       
        # posee el mismo funcionamiento de salto que el player y el especialBox aplicando gravedad y cambio de posicion y estado
        if self.state == "Idle" :
            pass
        if self.state == "Jumping":
            self.vy += settings.GRAVITY * dt
            self.y += self.vy * dt
            if self.vy > 0: 
                self.state = "Falling"

        elif self.state == "Falling":
            self.vy += settings.GRAVITY * dt
            self.y += self.vy * dt
            if self.y >= self.original_y: 
                self.y = self.original_y
                self.vy = 0
                self.state = "Idle"

    def on_consume(self, player: Player) -> Any:
        # cuando el jugador consume la llave esta desaparecera y se pondra como inactiva
        print("Key consumed")
        settings.SOUNDS["win"].play()
        
        self.game_level.winner_level = True
        player.winner = True
        self.game_level.transitionin = True
    
        # Despues de que el jugador gana el nivel se desactivara la llave
        self.active = False 
    
    def render(self, surface: pygame.Surface) -> None:
        if self.is_active:
            # Si la llave se encuentra en el estado "quieto/inactiva" se le aplicara rotacion en el eje x
            if self.state == "Idle":
                # Calculamos un factor de rotacion
                # El sin lo que hace es que el angulo de rotacion sea el seno de el tiempo actual , esto para que la rotacion sea suave
                # math.sin lo que hace es devolver el seno de un angulo en radianaes, por lo que devolvera un valor entre -1 y 1
                self.rotation_factor = abs(math.sin(pygame.time.get_ticks() * self.timer_rotation))
                # aqui calculamos la escala que tendra la rotacion dependendiendo del factor de rotacion
                self.scale_rotation = max(1, int(self.width * self.rotation_factor ))  

                # aplicamos rotacion en el eje x con pygame.transform.scale para reescalar la imagen
                scaled_texture = pygame.transform.scale(self.texture, (self.scale_rotation, self.height))

                # el offset es el espacio de movimiento que tendra la imagen para que se pueda mover en el eje x centrada
                x_offset = (self.width - self.scale_rotation) // 2
                surface.blit(scaled_texture, (self.x + x_offset, self.y))
            else:
                # Renderizamos normal , para ver el movimiento en y de la llave (el salto)
                surface.blit(self.texture, (self.x, self.y))

