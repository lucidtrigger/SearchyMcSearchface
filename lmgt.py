import discord

if message.content.lower().startswith('!rip'):
    # store arguments in x, excluding the first element (!rip)
    x = message.content.split(" ",4)[1:]
    # pad x with empty strings in case there are less than 4 arguments, and store the result in riptext
    riptext = x[:4] + ['']*(4 - len(x))
    print(riptext)

    rip = discord.Embed(color=random.randint(0x000000, 0xFFFFFF))
    rip.set_image(
            url=f"http://www.tombstonebuilder.com/generate.php?top1={quote(riptext[0])}&top2={quote(riptext[1])}&top3={quote(riptext[2])}&top4={quote(riptext[3])}&sp=")
    await client.send_message(message.channel, embed=rip)
