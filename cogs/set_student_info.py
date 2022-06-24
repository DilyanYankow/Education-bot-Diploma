import json
from discord.ext import commands

class Set_Student_Info(commands.Cog):
    def __init__(self, client):
        self.client=client

    def set_info(member, fac_num):
        try:
            file = open('stu_info.json')
            dict = {str(member): [member.guild.id, fac_num]}
            if str(member) in file.read():
                file = open("stu_info.json", "w")
            else:
                file = open("stu_info.json", "a")
            json.dump(dict, file)
            file.close()
        except Exception as e:
            print(e)

    #Events
    @commands.Cog.listener()        #function decorator
    async def on_ready(self):
        print('Set_student_info cog is open.')

    #Commands



def setup(client):
    client.add_cog(Set_Student_Info(client))