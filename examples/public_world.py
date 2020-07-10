from telebot import TeleBot

from sdtg import World

bot = TeleBot('TOKEN')
world = World()  # initializing world
world.walk_range = 1  # user can move only one tile ahead now
world.walk_attention = 'You can go so far!'  # user will see this text when he will try to walk further then walk_range
world.look_range = 3  # user now see for 2 tiles around now (width of telegram keyboard would be 5)

world.spawns = ['0_0', '5_5']  # new users will spawn on some of this positions


# now we going to create tiles and their actions


@world.create_tile()  # there is tile of nothing by default
def nothing_handler(member, pos):  # creating action function
    pass  # and do nothing cause of nothing)


@world.create_tile(name='wall', icon='<wall_emoji>', walkable=False)  # creating wall tile with wall emoji.
def wall_handler(member, pos):
    return 'You cant walk through the wall!'


@world.create_tile(name='coin', icon='<coin_icon>', destructuble=True)  # it will disapear from the map
def coin_handler(member, pos):
    member.inventory.append('coin')  # giving him a coin
    return 'You recieved a coin!'


world.insert_map({'1_1': 'wall', '2_2': 'coin'})  # just for test


@bot.message_handler(commands=['game'])
def game_handler(m):  # this function will send user keyboard
    if m.from_user.id not in world.members:
        member = world.create_member(m.from_user.id)
    else:
        member = world.members[m.from_user.id]
    kb = world.get_tg_map(member.pos)
    bot.send_message(m.from_user.id, 'Here your map!', reply_markup=kb)


world.inject_callback_handler(bot, 'Map. Your pos: {pos}. Member pos: {member.pos}')  # injecting callback handler.

bot.polling(none_stop=True)
