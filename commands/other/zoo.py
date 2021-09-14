from zstats import pages, choosecolour
import discord

zoos = {
    "one": {
        "name": "One",
        "text": {
            'Picture this.\nYou\'re a lion at a zoo. You spend your days in boredom, while people stare at you and take pictures of you on their flashy cell phones. \nAnd one day, a really stupid dumb fat nerd thin stupid dumb comes up to you, comes right up to your face so that your noses are almost touching, and says as loud as water: \n"IS THIS A LION????????"\n"I THINK IT MIGHT BE A LION???????""LETS CHECK"\nThen, he gets out his phone, searches up a lion on safari, and compares you to the pictures."YUP"\n"DEF LION"\nYou stared after him in disgust as he waggled over to disturb the babbons.'
        },
    },
    "two": {
        "name": "Two",
        "text": {
            'Picture this.\nYou\'re a monkey at a zoo. You pass your time by juggling rocks, entertaining tourists, and playing cards with your chimpanzee and babbon friends.\nOne sunny day, when you were just about to start up the 8th game of president, you see a really weird-lookin\' dude strut up right to the glass. You don\'t think much of it at first, concentrating on not losing your spot at president, but then he starts making some really weird soundin\' noises from his weird lookin\' mouth.\n"HELLO, MONKEYS!!!!!", he says after reading from the info sign.\n"OMGGG!!! HELLO, HELLO, CHIMPSSSSSSS!!!!!!" You look up from your cards in disgust. The chimpanzees snort, and the babbons gag.\nHe walks over to the next sign, about babbons. He bends down to a perfect right angle, squints his eyes, and says: "B...B...BA...BABOON??"\nInstantly, the babbon family springs up from their cards and rush to the window, pressing their faces against it and banging. The guy jumps back, looking weirder than ever before.\nThen, in perfect english, the babbons roar: "NEVER CALL A BABBON A BABOON."\nThe weird lookin\' dude runs away as fast as he can, jumping into his weird lookin\' car and looking weirder than ever.'
        },
    },
}


async def zoo(message, client):
    await message.reply(
        'Picture this.\nYou\'re a lion at a zoo. You spend your days in boredom, while people stare at you and take pictures of you on their flashy cell phones. \nAnd one day, a really stupid dumb fat nerd thin stupid dumb comes up to you, comes right up to your face so that your noses are almost touching, and says as loud as water: \n"IS THIS A LION????????"\n"I THINK IT MIGHT BE A LION???????""LETS CHECK"\nThen, he gets out his phone, searches up a lion on safari, and compares you to the pictures."YUP"\n"DEF LION"\nYou stared after him in disgust as he waggled over to disturb the babbons.'
    )
