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
Getting tg keyboard for certain position:
```python
world.get_tg_map('<x>_<y>') # returns InlineKeyboardMarkup object
```

