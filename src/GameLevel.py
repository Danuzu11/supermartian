"""
ISPPJ1 2024
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class GameLevel.
"""

from typing import Any, Dict

import pygame

import settings
from src.Creature import Creature
from src.GameItem import GameItem
from src.definitions import creatures, items
from src import SpecialBox, RotatingKey

class GameLevel:
    def __init__(self, num_level: int) -> None:
        self.tilemap = None
        self.creatures = []
        self.items = []
        settings.LevelLoader().load(self, settings.TILEMAPS[num_level])

    def add_item(self, item_data: Any) -> None:
        """
        Add an item to the game level. The item can be either a GameItem instance
        or a dictionary with item data.
        """
        if isinstance(item_data, GameItem):
            # If it's already a GameItem instance, add it directly
            self.items.append(item_data)
        else:
            # Otherwise, assume it's a dictionary and process it as before
            item_name = item_data.pop("item_name")
            if item_name == "special_box":
                self.items.append(
                    SpecialBox(
                        x=item_data["x"],
                        y=item_data["y"],
                        game_level=self,
                    )
                )
            elif item_name == "rotating_key":
                self.items.append(
                    RotatingKey(
                        x=item_data["x"],
                        y=item_data["y"],
                        width=item_data["width"],
                        height=item_data["height"],
                        game_level=self,
                    )
                )
            else:
                definition = items.ITEMS[item_name][item_data["frame_index"]]
                definition.update(item_data)
                self.items.append(GameItem(**definition))

    def add_creature(self, creature_data: Dict[str, Any]) -> None:
        definition = creatures.CREATURES[creature_data["tile_index"]]
        self.creatures.append(
            Creature(
                creature_data["x"],
                creature_data["y"],
                creature_data["width"],
                creature_data["height"],
                self,
                **definition,
            )
        )

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(0, 0, self.tilemap.width, self.tilemap.height)

    def set_render_boundaries(self, rect: pygame.Rect) -> None:
        self.tilemap.set_render_boundaries(rect)

    def update(self, dt: float) -> None:
        for creature in self.creatures:
            creature.update(dt)

        for item in self.items:
            item.update(dt)  


        # Remove dead creatures
        self.creatures = [
            creature for creature in self.creatures if not creature.is_dead
        ]

    def render(self, surface: pygame.Surface) -> None:
        self.tilemap.render(surface)
        for creature in self.creatures:
            creature.render(surface)
        for item in self.items:
            if item.active:
                item.render(surface)
