from replit import db
from random import randint, choices
import discord
from asyncio import TimeoutError, wait, FIRST_COMPLETED
from time import time
from math import floor
from zstats import convertInt
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
amounts = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
suits = ["♠️", "♥️", "♣️", "️♦️"]


class Game:
    def __init__(self, message, client):
        self.message = message
        self.client = client
        self.cardCount = {
            "A": 24,
            "2": 24,
            "3": 24,
            "4": 24,
            "5": 24,
            "6": 24,
            "7": 24,
            "8": 24,
            "9": 24,
            "10": 24,
            "J": 24,
            "Q": 24,
            "K": 24,
        }
        self.bet = None

    def cardFormat(self, x):
        return f"`{x[0]} {x[1]}`"

    def getCard(self):
        out = [
            choices(population=cards, weights=[i for i in self.cardCount.values()])[0],
            suits[randint(0, 3)],
            False,
        ]
        self.cardCount[out[0]] -= 1
        total = 0

        for i in self.cardCount.values():
            total += i

        if total <= 187:
            out[2] = True
            self.cardCount = {
                "A": 24,
                "2": 24,
                "3": 24,
                "4": 24,
                "5": 24,
                "6": 24,
                "7": 24,
                "8": 24,
                "9": 24,
                "10": 24,
                "J": 24,
                "Q": 24,
                "K": 24,
            }

        return out

    def getTotal(self, cardes):
        numbers = [i[0] for i in cardes]
        total = 0
        aUsed = 0
        for i in numbers:
            total += amounts[cards.index(i)]
        while total > 21 and len([i for i in numbers if i == "A"]) > aUsed:
            total -= 10
            aUsed += 1
        return total

    async def ask(self):
        buttons = [Button(style = ButtonStyle.blue, label = self.bet)] if bool(self.bet) else []
        buttons.extend([
            Button(style = ButtonStyle.green, label = "All"),
            Button(style = ButtonStyle.grey, label = "Half"),
            Button(style = ButtonStyle.red, label = "Leave")
        ])
        buttonMsg = await self.message.channel.send(
            "How much do you bet? Type leave to, well, leave",
            components = [buttons]
        )
        done, pending = await wait([
            self.client.wait_for(
                "message",
                check=lambda x: (
                    bool(convertInt(x.content))
                )
                and x.author.id == self.message.author.id
                and x.channel.id == self.message.channel.id,
                timeout=60.0,
            ),
            self.client.wait_for(
                "button_click",
                check = lambda x:
                x.author.id == self.message.author.id
                and x.channel.id == self.message.channel.id,
                timeout = 60.0
            ),
        ], return_when = FIRST_COMPLETED
        )
        try:
            msg = done.pop().result()

        except TimeoutError:
            await self.message.channel.send("bruh respond with a valid bet")
            return

        for future in done:
            future.exception()

        for future in pending:
            future.cancel()

        await buttonMsg.edit(components = [])

        if hasattr(msg, "component"):
            await msg.respond(type = 6)

        msg = msg.content.lower() if hasattr(msg, "content") else msg.component.label.lower()

        if msg == "leave":
            return await self.message.channel.send("aight looks like no more bj")

        dbuser = db["members"][str(self.message.author.id)]
        if "bjcd" in dbuser:
            if dbuser["bjcd"] < time():

                cdFormatted = floor(time() - dbuser["bjcd"]) + "s"

                await self.message.channel.send(
                    f"Woah there, chill. Wait {cdFormatted} before gambling again"
                )
                return

        amt = msg
        if amt.lower() in ["a", "all", "max"]:
            amt = dbuser["money"]
        elif amt.lower() in ["h", "half"]:
            amt = round(dbuser["money"] / 2)
        else:
            self.bet = amt
            amt = convertInt(amt)

            if not bool(amt):
                await self.message.channel.send("bet a number")
                return

        if dbuser["money"] < amt:
            await self.message.channel.send(
                "Sorry, you can't go into debt here at farmout"
            )
            return
        elif amt < 50:
            await self.message.channel.send("Bet an amount over 50.")
            return

        await self.play(int(amt))

    async def play(self, amt):

        dbuser = db["members"][str(self.message.author.id)]

        m = db["members"]
        db["members"][str(self.message.author.id)]["bjcd"] = time() + 10
        db["members"] = m

        cardsDrawn = [self.getCard(), self.getCard(), self.getCard()]

        bot = [cardsDrawn[0]]
        user = [[cardsDrawn[1], cardsDrawn[2]]]

        botTotal = self.getTotal(bot)
        userTotal = [self.getTotal(user[0])]

        userSplit = 0

        insurance = 0

        surrender = False

        if bool([i for i in cardsDrawn if i[2]]):
            await self.message.channel.send("Shuffled :game_die:")

        end = True
        while end:
            if userSplit > len(user) - 1:
                end = False
                userSplit -= 1
                break
            if userTotal[userSplit] >= 21:
                if userSplit < len(user) - 1:
                    userSplit += 1
                else:
                    break
            options = ["Hit", "Stand"]

            if (
                user[userSplit][0][0] == user[userSplit][1][0]
                and len(user[userSplit]) == 2
            ):
                options.append("Split")
            if (
                botTotal == 11
                and amt * 1.5 <= dbuser["money"]
                and insurance == 0
                and len(user[0]) == 2
            ):
                options.append("Insurance")
            if amt * 2 <= dbuser["money"]:
                options.append("Double down")
            if len(user) == 1 and len(user[0]) == 2:
                options.append("Surrender")

            e = discord.Embed(
                title=f"{self.message.author.name}'s blackjack game",
                description=f"**Bot, total: {botTotal}**\n{', '.join(list(map(self.cardFormat, bot)))}, `?`",
                colour=15721648,
            )

            for i in range(len(user)):
                e.add_field(
                    name=f"{'» ' if i == userSplit else ''}Hand {i + 1}, total: {userTotal[i]}",
                    value=", ".join(list(map(self.cardFormat, user[i]))),
                    inline=False,
                )

            buttonMsg = await self.message.channel.send(
                embed=e,
                components=[
                    [Button(style=ButtonStyle.green, label=i) for i in options]
                ],
            )

            try:
                msg = await self.client.wait_for(
                    "button_click",
                    check=lambda x: x.author.id == self.message.author.id
                    and x.channel.id == self.message.channel.id
                    and x.component.label.lower() in [i.lower() for i in options]
                    and x.message.id == buttonMsg.id,
                    timeout=60.0,
                )

            except TimeoutError:
                await self.message.channel.send(
                    "SMH my head 60 seconds is more than enough time to make up your mind"
                )
                return
            else:
                await buttonMsg.edit(components=[])
                await msg.respond(type=6)

                buttonMsg.components = []

                card = [
                    "I'm spending too long trying to think of something funny to say here",
                    69,
                    False,
                ]
                if msg.component.label == "Hit":
                    card = self.getCard()
                    user[userSplit].append(card)

                    userTotal[userSplit] = self.getTotal(user[userSplit])

                elif msg.component.label == "Stand":
                    userSplit += 1

                elif msg.component.label == "Double down":
                    card = self.getCard()
                    user[userSplit].append(card)

                    userTotal[userSplit] = self.getTotal(user[userSplit])

                    amt *= 2

                    userSplit += 1

                elif msg.component.label == "Insurance":
                    insurance = amt * 0.5

                elif msg.component.label == "Split":
                    userCopy = user[userSplit]
                    card = self.getCard()
                    user[userSplit] = [userCopy[0], card]
                    shuffle = card[2]

                    card = self.getCard()
                    user.append([userCopy[1], card])

                    card[2] = shuffle if shuffle else card[2]

                    userTotal[userSplit] = self.getTotal(user[userSplit])
                    userTotal.append(self.getTotal(user[userSplit + 1]))

                elif msg.component.label == "Surrender":
                    end = False
                    surrender = True
                    amt = round(amt / 2)

                if card[2]:
                    await self.message.channel.send("Shuffled :game_die:")

        while botTotal < 17 and not surrender:
            card = self.getCard()
            bot.append(card)
            botTotal = self.getTotal(bot)
            if card[2]:
                await self.message.channel.send("Shuffled :game_die:")

        insuranced = False
        if bot[0][0] == "A" and amounts[cards.index(bot[1][0])] == 10:
            insuranced = True

        largestSplit = (
            max([i for i in userTotal if i <= 21])
            if bool([i for i in userTotal if i <= 21])
            else 0
        )

        if (
            largestSplit > botTotal
            or (botTotal > 21 and bool(largestSplit))
            or (bool([a for a, b in zip(userTotal, user) if len(b) == 2 and a == 21]))
        ) and not surrender:
            reason = "Nice you found a bug\n"
            if largestSplit > botTotal:
                reason = "You went higher than the bot!\n"
            elif botTotal > 21:
                reason = "The bot busted!\n"
            elif bool([a for a, b in zip(userTotal, user) if len(b) == 2 and a == 21]):
                reason = "You got blackjack\n"

            if bool(insurance):
                amt -= insurance
            e = discord.Embed(
                title=f"{self.message.author.name}'s blackjack game. You win!",
                description=f"{reason}{'Also your insurance did not work' if bool(insurance) else ''}\nYou won {amt}\n**Bot, total: {botTotal}**\n{', '.join(list(map(self.cardFormat, bot)))}",
                colour=1950746,
            )

            e.set_footer(text="winner winner chicken dinner")

            for i in range(len(user)):
                e.add_field(
                    name=f"Hand {i + 1}, total {userTotal[i]}",
                    value=", ".join(list(map(self.cardFormat, user[i]))),
                    inline=False,
                )

            await self.message.channel.send(embed=e)
            m = db["members"]
            m[str(self.message.author.id)]["money"] += amt
            m[str(self.message.author.id)]["amounts"]["gambled"] += amt
            db["members"] = m

        elif (
            largestSplit == botTotal
            and bool(largestSplit)
            and not (len(bot) == 2 and botTotal == 21)
        ) and not surrender:
            reason = "You and the bot tied\n"

            if bool(insurance):
                amt -= insurance
            e = discord.Embed(
                title=f"{self.message.author.name}'s blackjack game. You tied!",
                description=f"{reason}{'Also your insurance did not work' if bool(insurance) else ''}\nYour balance did not change\n**Bot, total: {botTotal}**\n{', '.join(list(map(self.cardFormat, bot)))}",
                colour=16442624,
            )

            e.set_footer(text="👔")

            for i in range(len(user)):
                e.add_field(
                    name=f"Hand {i + 1}, total {userTotal[i]}",
                    value=", ".join(list(map(self.cardFormat, user[i]))),
                    inline=False,
                )

            await self.message.channel.send(embed=e)

        else:
            insuranceMsg = ""
            if bool(insurance) and insuranced:
                insuranceMsg = " But hey, at least you bought insurance and it worked\n"
                amt -= insurance
            elif bool(insurance) and not insuranced:
                insuranceMsg = " oh also your insurance didn't work\n"
                amt += insurance

            reason = "Nice you found a bug\n"

            if botTotal > largestSplit:
                reason = "The bot got higher than you.\n"
            elif not bool(largestSplit) and botTotal > 21:
                reason = "You and the bot busted! House wins.\n"
            elif not bool(largestSplit):
                reason = "You busted!\n"
            elif botTotal == 21:
                reason = "The bot got blackjack\n"
            if surrender:
                reason = "You surrendered\n"

            e = discord.Embed(
                title=f"{self.message.author.name}'s blackjack game. You lose!",
                description=f"{reason}{insuranceMsg}You lost {amt}\n**Bot, total: {botTotal}**\n{', '.join(list(map(self.cardFormat, bot)))}",
                colour=12851738,
            )

            e.set_footer(text="too bad so sad")

            for i in range(len(user)):
                e.add_field(
                    name=f"Hand {i + 1}, total {userTotal[i]}",
                    value=", ".join(list(map(self.cardFormat, user[i]))),
                    inline=False,
                )

            await self.message.channel.send(embed=e)  # is it working now no
            m = db["members"]
            m[str(self.message.author.id)]["money"] -= amt
            m[str(self.message.author.id)]["amounts"]["gambled"] -= amt
            db["members"] = m

        await self.ask()


async def blackjack(message, client):
    if str(message.author.id) not in db["members"]:
        await message.channel.send("make an account to blackjack")
        return

    game = Game(message, client)
    await game.ask()
