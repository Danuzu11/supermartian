from typing import Any
from src.GameItem import GameItem
from src.Player import Player
import settings
from src.RotatingKey import RotatingKey
import pygame


class SpecialBox(GameItem):
    def __init__(self, x: int, y: int, game_level) -> None:
        super().__init__(
            collidable=True,
            consumable=False,
            x=x,
            y=y,
            width=settings.SPECIAL_BOX_WIDTH,
            height=settings.SPECIAL_BOX_HEIGHT,
            texture_id="boxLevel",
            frame_index=0,
            solidness=dict(top=True, right=False, bottom=False, left=False),
        )
        self.texture = settings.TEXTURES["boxLevel"]
        self.texture_grey = settings.TEXTURES["boxLevelGrey"]
        self.game_level = game_level
        self.original_y = y
        self.jump_velocity = -settings.GRAVITY / 5 # asignamos velocidad negativa para controlar los saltos y su velocidad
        self.vy = 0
        self.state = "Idle" # los estados son idle, jumping y falling igual que el player para controlar su salto

    def update(self, dt: float) -> None:
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

    def on_collide(self, player: Player) -> Any:

        player_rect = player.get_collision_rect()
        box_rect = self.get_collision_rect()

        # Si el jugador golpea la caja y esta esta activa y se encuentra quieta se generara una animacion de salto
        # y ademas de esto se creara una llave que sera la que nos lleve al nuevo nivel
        if self.state == "Idle" and player_rect.top <= self.y and self.texture != self.texture_grey:
            self.state = "Jumping"
            self.vy = self.jump_velocity
            self.texture = self.texture_grey

            key_x_position = self.x + self.width // 2 - 18
            key_y_position = self.y - self.height // 2 - 16
            
            # Creamos la llave para que se cree en el nivel y se pueda recoger
            new_key = RotatingKey(
                x=key_x_position,
                y=key_y_position,
                width=16,
                height=16,
                game_level=self.game_level,
            )
            new_key.state = "Jumping"
            # Luego de definir todos sus parametros la agregamos a la lista de items del mundo
            self.game_level.add_item(new_key)

        # Verificamos que si el jugador esta encima de especialbox este se mantenga arriba y no caiga
        if player.vy > 0 and player_rect.bottom >= box_rect.top and player_rect.top < box_rect.top:
            player.y = box_rect.top - player.height
            player.vy = 0

            # Correcion de bug de animacion del player cuando salta encima de mi especialbox
            direction = "left" 
            if player.vx > 0: 
                direction = "right"
                
            # Solo detecta la direccion a la cual va si el jugador se mueve su animacion sera walk en la direccion correcta 
            if player.vx != 0:
                player.change_state("walk", direction)  
            # Sino el sprite sera el de estar parado   
            else:
                player.change_state("idle")

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, (self.x, self.y))



