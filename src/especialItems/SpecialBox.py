from typing import Any
from src.GameItem import GameItem
from src.Player import Player
import settings
from src.especialItems.RotatingKey import RotatingKey
import pygame


class SpecialBox(GameItem):
    def __init__(self, x: int, y: int, game_level) -> None:
        super().__init__(
            collidable=True,
            consumable=False,
            x= x,
            y= y,
            width=settings.SPECIAL_BOX_WIDTH ,
            height=settings.SPECIAL_BOX_HEIGHT,
            texture_id="boxLevel",
            frame_index=0,
            solidness=dict(top=True, right=True, bottom=True, left=True),
        )
        # Guardamos la textura de la caja especial original
        self.texture = settings.TEXTURES["boxLevel"]
        # Guardamos tambien la textura de la caja especial en gris para que no se pueda golpear mas
        self.texture_grey = settings.TEXTURES["boxLevelGrey"]
        self.game_level = game_level
        # Guardamos la posicion original donde estara la caja para que vuelva a su posicion original despues de saltar
        self.original_y = y
        # asignamos velocidad negativa para controlar los saltos y su velocidad
        self.jump_velocity = -settings.GRAVITY / 5 
        self.vy = 0
        self.state = "Idle" # los estados son idle, jumping y falling igual que el player para controlar su salto

    def update(self, dt: float) -> None:
   
        # Si la caja esta en estado saltando se le aplica gravedad a su velocidad en y para que caiga
        if self.state == "Jumping":
            # Aplciamos gravedad para que caiga la caja
            self.vy += settings.GRAVITY * dt
            # Y aqui aplicamos el dt a la velocidad para que el desplazamiento sea proporcional al tiempo tambien
            self.y += self.vy * dt
            # Si la velocidad es mayor a cero signica que la caja alcanzo su maximo y debe empezar a caer de lo contrario sigue subiendo
            if self.vy > 0:
                self.state = "Falling"

        # Mismo funcionamiento de lo anterior pero configuramos su estado de caida
        elif self.state == "Falling":
            self.vy += settings.GRAVITY * dt
            self.y += self.vy * dt
            # Aqui en ves de comparar su velocidad en y comparamos su posicion para que vaya bajando hasta su posicion original
            if self.y >= self.original_y:
                # Si la posicion en y sobrepasa la original la ajustamos a su posicion original y la detenemos para colocarla en estado estatico
                self.y = self.original_y
                self.vy = 0
                self.state = "Idle"

    def get_collision_rect(self) -> pygame.Rect:
        colliision_width = self.width * 0.40
        colliision_height = self.height * 0.83
        x_offset = (self.width - colliision_width) / 2
        y_offset = (self.height - colliision_height) / 2

        return pygame.Rect(self.x + x_offset + 1 , self.y + y_offset + 3 , colliision_width , colliision_height )
    
    def __verify_collision(self, player: Player , typeCollision: str) -> Any:
        # Obtenemos los rectaguloos de colision del jugador y la caja especial para hacer nuestro collide personal
        player_rect = player.get_collision_rect()
        box_rect = self.get_collision_rect()

        if typeCollision == "top":
            return (player_rect.bottom >= box_rect.top and player_rect.top < box_rect.top)
        elif typeCollision == "bottom":
            return (player_rect.top <= box_rect.bottom and player_rect.bottom > box_rect.bottom)
        
    def on_collide(self, player: Player) -> Any:


        # Verificamos que si el jugador esta encima de especialbox este se mantenga arriba y no caiga
        if player.vy > 0 and self.__verify_collision(player, "top") :
            
            # Restamos la altura del jugador para que este se quede encima de la caja
            player.y = self.get_collision_rect().top - player.height
            #Ajustamos la velocidad verticual para que el player no caiga ni atraviese la caja
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
                
        # Verificamos si el jugador golpea la parte inferior de la caja
        if player.vy < 0 and self.__verify_collision(player, "bottom") :

            # Si la caja esta quieta y su textura no es la gris (que esta desactivada) se generara salto y creacion de llave
            if self.state == "Idle" and self.texture != self.texture_grey:
                settings.SOUNDS["hitEspecialBox"].play()
                self.state = "Jumping"
                self.vy = self.jump_velocity
                self.texture = self.texture_grey

                # Calculamos la posicion de la llave en relacion a la caja especial
                key_x_position = self.x - 3
                key_y_position = self.y - self.height - 4

                # key_x_position = self.x - 2.5
                # key_y_position = self.y  - 5

                # Creamos la llave para que se cree en el nivel y se pueda recoger
                new_key = RotatingKey(
                    x=key_x_position,
                    y=key_y_position,
                    game_level=self.game_level,
                )
                
                # Luego de definir todos sus parametros la agregamos a la lista de items del mundo
                self.game_level.add_item(new_key)

            # Ajustamos la posicion del jugador para que no atraviese la caja ningun pixel
            # Quedando completamentepor debajo de la caja
            player.y = self.get_collision_rect().bottom
            # Y aplicamos gravedad para que caiga apenas toque la caja
            player.vy = settings.GRAVITY / 5

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, (self.x, self.y))
        
       




