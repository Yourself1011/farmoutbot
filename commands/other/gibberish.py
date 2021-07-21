from random import shuffle
import discord


async def gibberish(message, client):
    wordList = message.content.replace("\n", "\n ").split(" ")
    wordList.pop(0)
    wordList.pop(0)
    if wordList == []:
        await message.channel.send("mar mar marnio papido appeal")
        return
    out = []
    puncList = [".", ",", "!", "?", ":", "\n", '"', "'", ";"]
    for i in wordList:
        if len(i) > 3:
            iList = list(i)
            start = 1

            for j in iList:
                if j not in puncList:
                    break
                else:
                    start += 1

            iRev = iList.copy()
            iRev.reverse()

            end = -1

            for j in iRev:
                if j not in puncList:
                    break
                else:
                    end -= 1

            shuffled = list(i[start:end])
            shuffle(shuffled)
            out.append(i[0:start] + "".join(shuffled) + i[end:])
        else:
            out.append(i)

    await message.channel.send(
        " ".join(out).replace(r"\n", '+ "\n" +'),
        allowed_mentions=discord.AllowedMentions().none(),
    )
    # whatcha doin yes
