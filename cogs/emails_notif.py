import asyncio
import json
import smtplib
import time
import imaplib
import email
import traceback
from discord.ext import commands
from discord.ext import tasks

from bot import client





class Emails_Notif(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()  # function decorator
    async def on_ready(self):
        print('Reading emails is online.')

    # Commands
    @commands.command(aliases=['set_gmail', 'my_email'])
    async def set_email(self, ctx, email, password):
        def check(react, user):
            return user == ctx.message.author and str(react.emoji) in emojis

        msg = await ctx.send(f'Your email will be saved as: {email} and your password as ||{password}|| Proceed?')
        emojis = ["✅", '❎']
        for emoji in (emojis):
            await msg.add_reaction(emoji)
        try:
            reaction = await client.wait_for("reaction_add", check=check, timeout=15)  # Wait for a reaction
        except asyncio.TimeoutError:
            await ctx.send("Time out")
        else:
            if reaction[0].emoji == '✅':
                with open('emails.json', 'r') as f:
                    file = open("emails.json", "w")  # these 2 lines will
                    file.close()                    # delete all the text in the file
                try:
                    a_dictionary = {"email": email, "password": password}
                    with open('emails.json', 'w') as f:
                        f.write(str(a_dictionary))
                    await ctx.send(f'Changes have been saved.')
                except Exception as e:
                    print(e)
            else:
                await ctx.send('Credentials wont be changed.')

    @tasks.loop(seconds=30)
    async def check_email(self, ctx):
        print('1')
        while not client.is_closed():
            try:
                with open('emails.json', 'r') as f:
                    variables = json.load(f)
                    f.close()
                    serverEmail = variables['email']
                    serverPassword = variables['password']
            except Exception as e:
                print(e)
        print('test')
        try:
            SMTP_SERVER = "imap.gmail.com"
            mail = imaplib.IMAP4_SSL(SMTP_SERVER)
            mail.login(serverEmail, serverPassword)

            mail.select('inbox')
            data = mail.search(None, 'ALL')
            mail_ids = data[1]
            id_list = mail_ids[0].split()
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])

            for i in range(latest_email_id, first_email_id, -1):
                data = mail.fetch(str(i), '(RFC822)')
                for response_part in data:
                    arr = response_part[0]
                    if isinstance(arr, tuple):
                        msg = email.message_from_string(str(arr[1], 'utf-8'))
                        email_subject = msg['subject']
                        email_from = msg['from']
                        print('From : ' + email_from + '\n')
                        print('Subject : ' + email_subject + '\n')
        except Exception as e:
            traceback.print_exc()
            print(str(e))




def setup(client):
    client.add_cog(Emails_Notif(client))
