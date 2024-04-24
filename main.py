import discord
import os
from discord.ext import commands
import time
import random

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='e ', intents=intents)

schools = [
    'ASRJC', 'ASR', 'ACJC', 'ACSI', 'CJC', 'CJ', 'DHS', 'dunman', 'EJC', 'EJ',
    'HCI', 'HCJC', 'JPJC', 'MI', 'NYJC', 'NY', 'NJC', 'NJ', 'NUSH', 'RI',
    'RJC', 'RVHS', 'RVJC', 'SAJC', 'SJI', 'TMJC', 'TJC', 'TJ', 'VJC', 'VJ',
    'YIJC'
]
ongoing = []
game = {}


def createembed(name, avatar, type):
    if type == "bj":
        title = "{}'s blackjack game".format(name)
        description = "Type 'h' to hit (take another card) or type 's' to stand"
        color = 0x7851a9
        footer = "nice gambling addiction"

    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_author(name=name, icon_url=avatar)
    embed.set_footer(text=footer)
    return embed


def calctotal(cards):
    total = 0
    one = 0
    for card in cards:
        if card.isdigit():
            total += int(card)
        elif card != 'A':
            total += 10
        else:
            one += 1

    for i in range(one):
        if (total + 11) <= 21:
            total += 11
        else:
            total += 1

    return total


def checkwin(dcards, pcards):
    dtotal = calctotal(dcards)
    ptotal = calctotal(pcards)

    if dtotal == ptotal:
        return "Draw"
    elif dtotal == 21:
        return "Bot Wins"
    elif ptotal == 21:
        return "You Win"
    elif dtotal > ptotal and dtotal < 21:
        return "Bot Wins"
    elif ptotal > dtotal and ptotal < 21:
        return "You Win"
    elif dtotal > 21:
        return "You Win"
    elif ptotal > 21:
        return "Bot Wins"


def cardstr(cards):
    result = ''
    for card in cards:
        result += card + ' '
    return result


def pickcard(cards=[]):
    card = random.randint(1, 13)
    if card == 1:
        card = 'A'
    elif card == 11:
        card = 'J'
    elif card == 12:
        card = 'Q'
    elif card == 13:
        card = 'K'

    return str(card)


@bot.command(name="website", help='Gives you the link to the website')
async def website(ctx):
    await ctx.message.channel.send(
        "Check out the ETPS website: https://sites.google.com/moe.edu.sg/etps/home"
    )


@bot.command(name="rp", help='Determines your fate')
async def rp(ctx):
    userrp = random.randint(0, 90)
    if ctx.author.id == 350820475183824896 or ctx.author.id == 521306888097366028:
        await ctx.message.channel.send("{}, your RP is -{}".format(
            ctx.author.mention, userrp))

    else:  #? AHAHAHAHA brpther there is no loop
        await ctx.message.channel.send("{}, your RP is {}".format(
            ctx.author.mention, userrp))


@bot.command(name='check', help='admin command dont touch')
async def check(ctx):
    if ctx.author.id == 356004075793547264 or ctx.author.id == 502362064883417098 or ctx.author.id == 521306888097366028:
        etps = bot.get_guild(int(os.environ['GUILD']))
        mems = etps.members
        for m in mems:
            if etps.get_role(
                    1162418401071865968) not in m.roles and etps.get_role(
                        1162418372890345513) not in m.roles:
                name = m.display_name
                spl = ''

                for letter in name:
                    if not (letter.isalpha()):
                        spl = letter
                        break

                i = 1
                if spl != '':
                    lst = name.split(spl)
                    sch = ''
                    while sch.upper() not in schools and i <= len(lst):
                        sch = ''
                        hold = None
                        while (hold is None or hold == '') and i <= len(lst):
                            hold = lst[-1 * i]
                            i += 1

                        for l in hold:
                            if l.isalpha():
                                sch += l

                        if sch.upper() in schools:

                            print("{} from {} joined".format(m.name, sch))
                            mem = etps.get_member(m.id)
                            await mem.add_roles(
                                discord.utils.get(mem.guild.roles,
                                                  name="ETPS 2023-2024"))
                            break

                    #elif sch.upper() == "MOE":
                    #    print("{} from {} joined".format(after.name, sch))
                    #   await after.add_roles(discord.utils.get(after.guild.roles, name="MOE"))

                    if i > len(lst):

                        print("error! {}, {}".format(m.display_name, sch))

        await ctx.message.channel.send("successfully updated (i hope)")


@bot.command(name='bj', help='huat ah')
async def bj(ctx):
    author = int(ctx.message.author.id)

    name = ctx.message.author.name
    avatar = ctx.message.author.avatar

    embed = createembed(name, avatar, 'bj')

    dealercards = [pickcard(), pickcard()]
    dtotal = calctotal(dealercards)
    playercards = [pickcard(), pickcard()]
    total = calctotal(playercards)
    end = False

    if dtotal == 21:
        if total != 21:
            end = True
            #money = -1 * money
            result = "Bot Wins"
        else:
            end = True
            result = "Draw"
            #money = 0
    if total == 21:
        end = True
        result = "You Win"

    if end:
        dcardstr = cardstr(dealercards)
        embed.add_field(name="Bot's cards", value=dcardstr, inline=False)
        embed.add_field(name="Total", value=dtotal, inline=False)

        pcardstr = cardstr(playercards)
        embed.add_field(name="{}'s cards".format(name),
                        value=pcardstr,
                        inline=False)
        embed.add_field(name="Total", value=total, inline=False)

        embed.add_field(name=result, value='', inline=False)

    else:
        embed.add_field(name="Bot's cards", value="? ?", inline=False)
        embed.add_field(name="Total", value="?", inline=False)

        pcardstr = cardstr(playercards)
        embed.add_field(name="{}'s cards".format(name),
                        value=pcardstr,
                        inline=False)
        embed.add_field(name="Total", value=total, inline=False)

        game[author] = [avatar, dealercards, playercards]
        ongoing.append(author)
    await ctx.message.channel.send(embed=embed)


@bot.event
async def on_message(message):
    if int(message.author.id) in ongoing:
        if message.content.lower() == "h":

            set = game[int(message.author.id)]
            name = message.author.name

            embed = createembed(name, set[0], 'bj')
            dealercards = set[1]
            playercards = set[2]
            #money = set[3]
            card = pickcard(playercards)
            result = ''

            playercards.append(card)
            total = calctotal(playercards)

            if total >= 21:
                result = checkwin(dealercards, playercards)

                dtotal = calctotal(dealercards)
                dcardstr = cardstr(dealercards)
                embed.add_field(name="Bot's cards",
                                value=dcardstr,
                                inline=False)
                embed.add_field(name="Total", value=dtotal, inline=False)

                ongoing.remove(int(message.author.id))
                game.pop(int(message.author.id))
            elif len(playercards) == 5:
                result = "You Win"
                dtotal = calctotal(dealercards)
                dcardstr = cardstr(dealercards)
                embed.add_field(name="Bot's cards",
                                value=dcardstr,
                                inline=False)
                embed.add_field(name="Total", value=dtotal, inline=False)

                ongoing.remove(int(message.author.id))
                game.pop(int(message.author.id))
            else:
                embed.add_field(name="Bot's cards", value="? ?", inline=False)
                embed.add_field(name="Total", value="?", inline=False)

            pcardstr = cardstr(playercards)
            embed.add_field(name="{}'s cards".format(name),
                            value=pcardstr,
                            inline=False)
            embed.add_field(name="Total", value=total, inline=False)
            embed.add_field(name=result, value='', inline=False)

            await message.channel.send(embed=embed)

        if message.content.lower() == "s":

            set = game[int(message.author.id)]
            name = message.author.name
            embed = createembed(name, set[0], 'bj')
            dealercards = set[1]
            playercards = set[2]

            dtotal = calctotal(dealercards)

            while dtotal < 18:
                card = pickcard(dealercards)
                dealercards.append(card)
                dtotal = calctotal(dealercards)

            result = checkwin(dealercards, playercards)

            dcardstr = cardstr(dealercards)
            embed.add_field(name="Bot's cards", value=dcardstr, inline=False)
            embed.add_field(name="Total", value=dtotal, inline=False)

            total = calctotal(playercards)
            pcardstr = cardstr(playercards)
            embed.add_field(name="{}'s cards".format(name),
                            value=pcardstr,
                            inline=False)
            embed.add_field(name="Total", value=total, inline=False)

            embed.add_field(name=result, value='', inline=False)

            ongoing.remove(int(message.author.id))
            game.pop(int(message.author.id))
            await message.channel.send(embed=embed)

    await bot.process_commands(message)


@bot.event
async def on_member_update(before, after):
    if before.nick != after.nick:
        name = after.nick
        spl = ''
        try:
            for letter in name:
                if not (letter.isalpha()):
                    spl = letter
                    break
        except:
            print(name)
            print(before.nick)

        sch = ''
        i = 1

        while sch.upper() not in schools and i <= len(name.split(spl)):
            hold = None
            while hold is None or hold == '':
                hold = name.split(spl)[-1 * i]
                i += 1

            for l in hold:
                if l.isalpha():
                    sch += l

            if sch.upper() in schools:
                print("{} from {} joined".format(after.name, sch))
                await after.add_roles(
                    discord.utils.get(after.guild.roles,
                                      name="ETPS 2023-2024"))

        #elif sch.upper() == "MOE":
        #    print("{} from {} joined".format(after.name, sch))
        #   await after.add_roles(discord.utils.get(after.guild.roles, name="MOE"))

        if i > len(name.split(spl)):
            print("error! {}".format(after.nick))


@bot.event
async def on_user_update(before, after):
    if before.display_name != after.display_name:
        etps = bot.get_guild(int(os.environ['GUILD']))
        name = after.display_name
        spl = ''

        for letter in name:
            if not (letter.isalpha()):
                spl = letter
                break

        i = 1
        if spl != '':
            lst = name.split(spl)
            sch = ''
            while sch.upper() not in schools and i <= len(lst):
                sch = ''
                hold = None
                while (hold is None or hold == '') and i <= len(lst):
                    hold = lst[-1 * i]
                    i += 1

                for l in hold:
                    if l.isalpha():
                        sch += l

                if sch.upper() in schools:

                    print("{} from {} joined".format(after.name, sch))
                    mem = etps.get_member(after.id)
                    await mem.add_roles(
                        discord.utils.get(mem.guild.roles,
                                          name="ETPS 2023-2024"))
                    break

            #elif sch.upper() == "MOE":
            #    print("{} from {} joined".format(after.name, sch))
            #   await after.add_roles(discord.utils.get(after.guild.roles, name="MOE"))

            if i > len(lst):

                print("error! {}, {}".format(after.display_name, sch))


@bot.event
async def on_ready():
    print('We have logged in as {}'.format(bot.user))


#keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))
