import random
from typing import Callable, Any

from telebot import types


class World:
    def __init__(self):
        self.icons = {'nothing': 'ᅠ'}
        self.size = 11
        self.walk_range = 1
        self.look_range = 2

        self.members_list = list()
        self.map = dict()
        self.spawns = ['5_5']

    def insert_map(self, world_map: dict):
        if not isinstance(world_map, dict):
            return
        for pos in world_map:
            if pos.count('_') != 1:
                continue
            try:
                self.parse_pos(pos)
            except:
                continue
            self.map.update({pos: world_map[pos]})

    def insert_icons(self, icons: dict):
        if not isinstance(icons, dict):
            return
        for icon_name in icons:
            if not isinstance(icon_name, str) or not isinstance(icons[icon_name], str):
                continue
            self.icons.update({icon_name: icons[icon_name]})

    @property
    def walk_range_list(self):
        walk_range_list = [0]
        for i in range(self.walk_range):
            i += 1
            walk_range_list.insert(0, -i)
            walk_range_list.append(i)
        return walk_range_list

    @property
    def look_range_list(self):
        look_range_list = [0]
        for i in range(self.look_range):
            i += 1
            look_range_list.insert(0, -i)
            look_range_list.append(i)
        return look_range_list

    def get_walkable_tiles(self, pos):
        x, y = self.parse_pos(pos)
        walkable_tiles = []
        for i in self.walk_range_list:
            for j in self.walk_range_list:
                tile = f'{x + j}_{y + i}'
                walkable_tiles.append(tile)
        return walkable_tiles

    @property
    def members_icons(self):
        return {member['pos']: member['icon'] for member in self.members_list}

    @property
    def members(self):
        return {member['id']: member for member in self.members_list}

    @property
    def width(self):
        return len(self.look_range_list)

    def get_visible_tiles(self, pos):
        x, y = self.parse_pos(pos)
        visible_tiles = []
        for i in self.look_range_list:
            for j in self.look_range_list:
                tile = f'{x + j}_{y + i}'
                visible_tiles.append(tile)
        return visible_tiles

    def get_icon(self, pos) -> str:
        players_icons = self.members_icons
        if pos in players_icons:
            return players_icons[pos]
        icon_name = self.get_tile(pos)
        if icon_name not in self.icons:
            return self.icons['nothing']
        return self.icons[icon_name]

    def create_member(self, user_id):
        pos = random.choice(self.spawns)
        commit = {
            'id': user_id,
            'pos': pos,
            'icon': '🔵',
            'inventory': dict()
        }
        self.members_list.append(commit)
        return commit

    @staticmethod
    def parse_pos(pos):
        x = int(pos.split('_')[0])
        y = int(pos.split('_')[0])
        return x, y

    def get_tile(self, pos):
        tile = self.map.get(pos)
        if not tile:
            return 'nothing'
        return tile

    @staticmethod
    def __map5elem(l: list, f: Callable[[Any], Any]):
        row = []
        for elem in l:
            row.append(f(elem))
            if len(row) == 5:
                yield row
                row = []

    def get_tg_map(self, pos):
        kb = types.InlineKeyboardMarkup(self.width)
        visible = self.get_visible_tiles(pos)
        for row in self.__map5elem(visible,
                            lambda tile: types.InlineKeyboardButton(text=self.get_icon(tile), callback_data=tile)):
            kb.add(*row)
        return kb
