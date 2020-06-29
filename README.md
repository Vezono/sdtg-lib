# sdtg-lib
Second-dimensional Telegram Games library.
## Requires:
`pyTelegramBotApi`
## Installing by requirements.txt:
`git+git://github.com/Vezono/sdtg-lib.git#egg=sdtg`

## Usage:

Creating a world:
```python
world = World()
```
Uploading icons:
```python
world.insert_icons({
  '<tile_name>': '<icon (symbol or emoji)>'
})
```
Uploading custom map:
```python
world.insert_map({
  '<x>_<y>': '<tile_name (must be in icons)>'
})
```
Setting custom keyboard and movable size:
```python
world.look_range = 2 # keyboard size will be 5 (walk_range*2 + 1)
world.walk_range = 1 # player would be able to move only 1 tile ahead
```
Getting tile on certain pos:
```python
world.world.get_tile('<x>_<y>') # returns tile_name
```
Getting walkable tiles for certain position (depends on walk_range):
```python
world.get_walkable_tiles('<x>_<y>') # returns list of walkable positions
```
Getting tg keyboard for certain position:
```python
world.get_tg_map('<x>_<y>') # returns InlineKeyboardMarkup object
```
Moving example:
```python
@bot.callback_query_handler(func=lambda c: '_' in c.data)
def call(c: types.CallbackQuery):
    player = c.from_user.id
    pos = world.members[player]['pos']
    walkable = world.get_walkable_tiles(pos)
    if c.data not in walkable or world.get_tile(c.data) == 'wall':
        bot.answer_callback_query(c.id, 'Yuo cant move there!')
        return
    world.members[player]['pos'] = c.data
    kb = world.get_tg_map(c.data)
    bot.edit_message_text(f'Map', c.message.chat.id, c.message.message_id, reply_markup=kb)
```

