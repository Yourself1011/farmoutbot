import random


async def air(message, client):
    responses = [
        "here, have some air. :dash: :dash: :dash:\nresponse 1",
        "air? wait, what? that's a thing?\nresponse 2",
        "anyone found response 3 yet\nresponse 4",
    ]

    return (random.choice(responses), True)
