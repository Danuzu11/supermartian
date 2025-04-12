"""
ISPPJ1 2024
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.Camera import Camera
from src.Clock import Clock
from src.GameLevel import GameLevel
from src.Player import Player

from src.especialItems.SpecialBox import SpecialBox

class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params.get("level", 1)
        self.game_level = enter_params.get("game_level")
        self.special_box = False

        if self.game_level is None:
            self.game_level = GameLevel(self.level)
            pygame.mixer.music.load(
                settings.BASE_DIR / "assets" / "sounds" / "music_grassland.ogg"
            )
            pygame.mixer.music.play(loops=-1)

        self.tilemap = self.game_level.tilemap
        self.player = enter_params.get("player")
        
        if self.player is None:
            self.player = Player(0, settings.VIRTUAL_HEIGHT - 66, self.game_level)
            self.player.change_state("idle")

        self.camera = enter_params.get("camera")

        if self.camera is None:
            self.camera = Camera(0, 0, settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
            self.camera.set_collision_boundaries(self.game_level.get_rect())
            self.camera.attach_to(self.player)

        self.clock = enter_params.get("clock")
       
        if self.clock is None:
            self.clock = Clock(30)
        Timer.clear()
        def countdown_timer():
            self.clock.count_down()

            if 0 < self.clock.time <= 5:
                settings.SOUNDS["timer"].play()

            if self.clock.time == 0:
                self.player.change_state("dead")

        Timer.every(1, countdown_timer)

        # Variables de transicion de nivel
        self.transitionating = False
        # 1 para fade in y -1 para fade out
        self.transition_direction = 1
        # transition_alpha basicamente sera la sombra que tenga la pantalla 255 completamente oscura y 0 para transparente
        self.transition_alpha = 0
        # La velocidad a la que se hace cada transicion
        self.transition_duration = 1.5

    def __start_transition(self):
        self.transitionating = True
        self.game_level.transitionin = False
        self.transition_direction = 1
        self.transition_alpha = 0
        print("comienza transicion")
             
    def __switch_transition(self):
        if self.transition_direction == 1:
            self.next_level()  

        self.transition_direction = -1
        print("cambia transicion")

    def __end_transition(self):
        self.transitionating = False
        self.game_level.transitionin = False
        self.transition_alpha = 0
        print("FIN transicion")
        
        
    def __verify_transition(self,dt:float):
        # Variable para controlar el inicio de transicion del nivel
        if self.game_level.transitionin:
            self.__start_transition()
            
        if self.transitionating:
            
            # Vamos calculando el alpha de la transicion, si es fade in a 255 y si es fade out a 0
            # Dependiendo de la direccion de la transicion sumara si es fade in y restara si es fade out
            self.transition_alpha += self.transition_direction * 255 * dt / self.transition_duration
            self.transition_alpha = max(0, self.transition_alpha)

            # Si el valor de alpha supera los 255 quiere decir que termino su fade in , entonces cambiamos la direccion
            if self.transition_alpha >= 255:
                self.__switch_transition()
            # Si el valor de alpha es 0 quiere decir que su fade out ya termino y termina transicion
            if self.transition_alpha == 0:
                self.__end_transition()
                
    def update(self, dt: float) -> None:

        # actualizamos y llamados a la funcion para verificar si debemos hacer la transicion de nivel
        self.__verify_transition(dt)
        
        # Si el nivel fue ganado detiene el tiempo
        if self.game_level.winner_level:
            Timer.pause()

        if self.player.is_dead:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            Timer.clear()
            self.state_machine.change("game_over", self.player)

        self.player.update(dt)

        if self.player.y >= self.player.tilemap.height:
            self.player.change_state("dead")

        self.camera.update()
        self.game_level.set_render_boundaries(self.camera.get_rect())
        self.game_level.update(dt)

        for creature in self.game_level.creatures:
            if self.player.collides(creature):
                self.player.change_state("dead")

        for item in self.game_level.items:
            if not item.active or not item.collidable:
                continue

            if self.player.collides(item):
                item.on_collide(self.player)
                item.on_consume(self.player)
        
        # Si el jugador obtiene cierta cantidad de puntos genera caja especial
        # Siempre y cuando no haya ya una caja activa
        if not self.special_box and self.player.score >= 1 and self.level != 2:
            self.special_box = True
            box_x = settings.VIRTUAL_WIDTH // 2 - 30 * 2 
            box_y = settings.VIRTUAL_HEIGHT // 2 - 30 * 2 - 5   
            # Crea el objeto Caja y lo agrega a la lista de items del nivel  
            box = SpecialBox(box_x, box_y,self.game_level)
            self.game_level.add_item(box)
            
        Timer.update(dt)
        
    def render(self, surface: pygame.Surface) -> None:
        world_surface = pygame.Surface((self.tilemap.width, self.tilemap.height))
        self.game_level.render(world_surface)
        self.player.render(world_surface)
        surface.blit(world_surface, (-self.camera.x, -self.camera.y))

        render_text(
            surface,
            f"Score: {self.player.score}",
            settings.FONTS["small"],
            5,
            5,
            (255, 255, 255),
            shadowed=True,
        )

        render_text(
            surface,
            f"Time: {self.clock.time}",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH - 60,
            5,
            (255, 255, 255),
            shadowed=True,
        )

        if self.transitionating:
            faded_surface = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
            faded_surface.fill((0, 0, 0))
            # Ponemos una capa de color self.transition_alpha
            # siendo self.transition_alpha = 0 transparente y 255 totalmente negro
            faded_surface.set_alpha(self.transition_alpha)
            surface.blit(faded_surface, (0, 0))
            

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause" and input_data.pressed:
            Timer.pause()
            self.state_machine.change(
                "pause",
                level=self.level,
                camera=self.camera,
                game_level=self.game_level,
                player=self.player,
                clock=self.clock,
            )
        else:
            self.player.on_input(input_id, input_data)
    
    
    def next_level(self):
        self.winner = False
        self.game_level.winner_level = False
        self.state_machine.change("play", level=2)
        print("CREANDO SIGUIENTE NIVEL....")
