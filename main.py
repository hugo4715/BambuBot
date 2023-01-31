import json
import os

import requests as requests
from discord import Intents
from discord.ext import commands, tasks
import asyncio

intents = Intents.default()
bot = commands.Bot(command_prefix='!', description='Filament checker', intents=intents)


def request_filaments():
    url = "https://eu.store.bambulab.com/collections/bambu-lab-3d-printer-filament/products.json"
    response = requests.get(url)
    return response.json()


def get_stock():
    data = request_filaments()
    stock = {}
    for product in data['products']:
        for variant in product['variants']:
            product_name = product['title'] + ' ' + variant['title']
            available = variant['available']
            stock[product_name] = available
    return stock


@tasks.loop(seconds = 60)
async def check_filaments():
    # check out of stock filaments
    old_stock = get_stock()

    while True:
        await asyncio.sleep(60)
        if not users_to_notify:
            print('No users to notify')
            continue

        print('Checking stock...')
        stock = get_stock()
        for product_name, available in stock.items():
            if available and not old_stock[product_name]:
                print(f'{product_name} is back in stock')
                await notify_users(product_name)
        old_stock = stock


async def notify_users(product):
    for user_id in users_to_notify:
        user = bot.get_user(user_id)
        product_name = product['title']
        print(f'Notifying {user.name} about {product_name}')
        await user.send(product_name + ' is back in stock')


@bot.command()
async def filaments(ctx):
    response = get_stock()
    msg = 'Filaments out of stock:\n'
    # first add the out of stock filaments
    out_of_stock = 0
    for product_name, available in response.items():
        if not available:
            msg += product_name + ' - out of stock\n'
            out_of_stock += 1

    # then add the available filaments
    msg += '\nFilaments available:\n'
    in_stock = 0
    for product_name, available in response.items():
        if available:
            msg += product_name + ' - available\n'
            in_stock += 1

    msg += f'\n{in_stock} filaments in stock, {out_of_stock} out of stock'

    # send at most 2000 characters and split the message at a line break if needed
    part = ''
    for line in msg.splitlines():
        if len(part) + len(line) > 2000:
            await ctx.send(part)
            part = ''
        part += line + '\n'
    await ctx.send(part)


@bot.command('notify')
async def filaments_in_stock_notification(ctx):
    # add user to list of users to notify or remove user from list of users to notify
    user_id = ctx.message.author.id
    if user_id in users_to_notify:
        users_to_notify.remove(user_id)
        await ctx.send('You will not be notified when filament is in stock')
    else:
        users_to_notify.append(user_id)
        await ctx.send('You will be notified when filament is in stock')
    # write json
    with open('/data/users.json', 'w') as f:
        json.dump(users_to_notify, f)


@bot.listen()
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    check_filaments.start()


if __name__ == '__main__':
    print('Starting bot...')

    # load user from json
    users_to_notify = []
    if os.path.isfile('/data/users.json'):
        with open('/data/users.json', 'r') as f:
            users_to_notify = json.load(f)

    print(f'Users to notify: {len(users_to_notify)}')

    if os.environ.get('TOKEN') is None:
        print('Missing TOKEN environment variable')
        exit(1)

    token = os.environ['TOKEN']
    bot.run(token)

