from typing import Any
from src.GameItem import GameItem
from src.Player import Player
import settings
import pygame
import math

class RotatingKey(GameItem):

    def __init__(self, x: int, y: int, width: int, height: int, game_level) -> None:
        super().__init__(
            collidable=True,
            consumable=True,
            x=x,
            y=y,
            width=settings.KEY_WIDTH,
            height=settings.KEY_HEIGHT,
            texture_id="key",
            frame_index=0,
            solidness=False
        )

        self.texture = settings.TEXTURES["key"]
        self.is_active = True
        self.game_level = game_level
        self.original_y = y  
        self.jump_velocity = -settings.GRAVITY / 5

        self.state = "Jumping" # los estados son idle, jumping y falling igual que el player para controlar su salto
        self.vy = self.jump_velocity
        self.angle = 0 

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

    def on_consume(self, player: Player) -> Any:
        print("Key consumed")
        self.active = False 
    
    def render(self, surface: pygame.Surface) -> None:
        if self.is_active:
            if self.state == "Idle":
                # aplica rotacion en el eje x
                scale_factor = abs(math.sin(pygame.time.get_ticks() * 0.005))
                scaled_width = max(1, int(self.width * scale_factor))
                scaled_texture = pygame.transform.scale(self.texture, (scaled_width, self.height))
                x_offset = (self.width - scaled_width) // 2
                surface.blit(scaled_texture, (self.x + x_offset, self.y))
            else:
                # Render the key normally during jumping or falling
                surface.blit(self.texture, (self.x, self.y))


