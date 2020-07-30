import random
from typing import Callable, Any

from telebot import types, TeleBot

from .exceptions import TileNotInTilesetException, InvalidPositionFormat
from .models import Tile, Member


class World:
    def __init__(self):
        self.tile_set = {}
        self.walk_range = 1
        self.look_range = 2

        self.walk_attention = '<walk_attention>'
        self.members_list = list()
        self.map = dict()
        self.spawns = ['0_0']

    def __getitem__(self, item):
        return self.get_tile(item)

    def __setitem__(self, key, value):
        return self.insert_map({key: value})

    def insert_map(self, world_map: dict):
        if not isinstance(world_map, dict):
            return
        for pos in world_map:
            try:
                self.parse_pos(pos)
            except:
                raise InvalidPositionFormat
            if world_map[pos] not in self.tile_set:
                raise TileNotInTilesetException
            self.map.update({pos: world_map[pos]})

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
        return {member.pos: member.icon for member in self.members_list}

    @property
    def members(self):
        return {member.id: member for member in self.members_list}

    @property
    def members_positions(self):
        return {member.id: member.pos for member in self.members_list}

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
        members_icons = self.members_icons
        if pos in members_icons:
            return members_icons[pos]
        tile = self[pos]
        return tile.icon

    def create_member(self, user_id, pos: str = None, icon='🔵'):
        if not pos:
            pos = random.choice(self.spawns)
        member = Member(user_id, icon, list(), pos)
        self.members_list.append(member)
        return member

    @staticmethod
    def parse_pos(pos):
        x = int(pos.split('_')[0])
        y = int(pos.split('_')[1])
        return x, y

    def get_tile(self, pos) -> Tile:
        tile_name = self.map.get(pos)
        if not tile_name:
            tile_name = 'nothing'
        tile: Tile = self.tile_set[tile_name]
        if not tile:
            return self.tile_set['nothing']
        return tile

    def __map_elem(self, l: list, f: Callable[[Any], Any]):
        rows = []
        row = []
        for elem in l:
            row.append(f(elem))
            if len(row) == self.width:
                rows.append(row)
                row = []
        return rows

    def get_tg_map(self, pos):
        kb = types.InlineKeyboardMarkup(self.width)
        visible = self.get_visible_tiles(pos)
        for row in self.__map_elem(visible,
                                   lambda tile: types.InlineKeyboardButton(text=self.get_icon(tile),
                                                                           callback_data=tile)):
            kb.add(*row)
        return kb

    def create_tile(self, name='nothing', icon=' ', walkable=True, destructuble=False):
        def actual_decorator(func):
            def wrapper(member, pos):
                if walkable:
                    member.pos = pos
                if destructuble:
                    self[pos] = 'nothing'
                return func(member, pos)

            self.tile_set.update({name: Tile(name, icon, lambda m, p: wrapper(m, p))})
            return wrapper

        return actual_decorator

    def inject_callback_handler(self, bot: TeleBot, map_text='Map.'):
        @bot.callback_query_handler(func=lambda c: c.data.count('_') == 1)
        def callback_handler(c):
            pos = c.data
            tile = self[pos]
            member = self.members[c.from_user.id]

            if pos not in self.get_walkable_tiles(member.pos):
                bot.answer_callback_query(c.id, self.walk_attention)
                return
            bot.answer_callback_query(c.id, tile.func(member, pos))
            kb = self.get_tg_map(member.pos)
            bot.edit_message_text(map_text.format(member=member, pos=pos),
                                  c.from_user.id, c.message.message_id,
                                  reply_markup=kb)
