import asyncio, json, imaplib, email, traceback, discord
from discord.ext import commands, tasks
from bot import client, is_botchannel


class Emails_Notif(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()  # function decorator
    async def on_ready(self):
        print('Reading emails is online.')
        self.check_email.start()

    # Commands
    @commands.command(aliases=['set_gmail', 'my_email'])
    @commands.check(is_botchannel)
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
                    channel = discord.utils.get(ctx.guild.channels, name='server-email')
                    channel_id = channel.id
                    a_dictionary = {"email": [email, password, channel_id]}
                    file = open("emails.json", "w")
                    json.dump(a_dictionary, file)
                    await ctx.send(f'Changes have been saved.')
                except Exception as e:
                    print(e)
            else:
                await ctx.send('Credentials wont be changed.')

    @tasks.loop(minutes=10)
    async def check_email(self):
        print('1')
        try:
            print('2')
            with open('emails.json', 'r') as f:
                variables = json.load(f)
                f.close()
                credentials = variables[str("email")]
                serverEmail = str(credentials[0])
                serverPassword = str(credentials[1])
                server_channel_id=client.get_channel(int(credentials[2]))


        except Exception as e:
            print(e)
        print('test')
        try:
            print('3')

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
                        email_from = msg['from']
                       #  print('From : ' + email_from + '\n')
                        await server_channel_id.send(f'Email from: {email_from}')
                _, data = mail.fetch(str(i), '(RFC822)')
                _, bytes_data = data[0]
                email_message = email.message_from_bytes(bytes_data)

                for part in email_message.walk():
                    if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                        message = part.get_payload(decode=True)
                        await server_channel_id.send(f'Email message: {message.decode()}')
                        break
                await server_channel_id.send('-------------------------')

        except Exception as e:
            traceback.print_exc()
            print(str(e))




def setup(client):
    client.add_cog(Emails_Notif(client))
