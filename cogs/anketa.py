import sqlite3
import disnake
from disnake import ButtonStyle
from disnake.ext import commands
from mcrcon import MCRcon

mcr = MCRcon("Ip_Rcon", "Password_Rcon", port=00000) #Сюда надо вставить данные от Rcon

class prinorkl(disnake.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @disnake.ui.button(label="Принять", style=ButtonStyle.green, custom_id="yes")
    async def prin(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        con = sqlite3.connect('LastEmpires.db')
        cur = con.cursor()
        a = cur.execute(f'''SELECT msg_id, member_id, member_nick FROM anketa WHERE msg_id = ({interaction.message.id})''').fetchone()
        yeees = disnake.Embed(title='Вы приняты!', colour=0x2F3136, description="– MineWeeks - приватный сервер для воплощения ваших идей и новых знакомств! У нас вы можете погрузиться в **улучшенный ванильный** игровой процесс, который не искажён различными, давно изжившими себя плагинами, а только дополнен новыми небольшими механиками.\n\n**Вход на сервер**\n– Ip сервера - play.mineweeks.ru или 5.9.143.176:25586\n– Версия - 1.19-1.19.2\n– Веб-карта - http://65.108.130.198:25789/\n\n**Моды (необязательно)**\n– Используемые моды: PlasmoVoice, EmoteCraft– Более подробная информация о модах и установке на сайте - https://www.mineweeks.ru/game/mods")
        error = disnake.Embed(title='Ошибка.', colour=0x2F3136, description='**Причина**: Проблемы с RCON')
        left = disnake.Embed(title='Ошибка.', colour=0x2F3136, description='**Причина**: Человек покинул дискорд сервер.')
        try:
            member = await interaction.guild.fetch_member(a[1])
            role = interaction.guild.get_role(123456789000000000) #Id роли игрока
            await member.edit(nick=a[2])
            await member.add_roles(role)
            try:
                mcr.connect()
                mcr.command("whitelist add " + a[2]) #Команда для добавления в вайтлист
                mcr.disconnect()
            except:
                await interaction.send(embed=error, ephemeral=True)
            else:
                await interaction.send("Принят", ephemeral=True)
                cur.execute(f'''DELETE FROM anketa WHERE msg_id = {interaction.message.id}''')
                await interaction.message.delete()
                await member.send(embed=yeees)
        except:
            await interaction.send(embed=left, ephemeral=True)
            cur.execute(f'''DELETE FROM anketa WHERE msg_id = {interaction.message.id}''')
            await interaction.message.delete()
        con.commit()
        con.close()

    @disnake.ui.button(label="Отклонить", style=ButtonStyle.danger, custom_id="noo")
    async def otkl(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        con = sqlite3.connect('LastEmpires.db')
        cur = con.cursor()
        a = cur.execute(f'''SELECT member_id FROM anketa WHERE msg_id = ({interaction.message.id})''').fetchone()
        left = disnake.Embed(title='Ошибка.', colour=0x2F3136, description='**Причина**: Человек покинул дискорд сервер.')
        send_embed_ank = disnake.Embed(
            title='К сожалению ваша заявка была отклонена',
            description='Причина: Отклонение беспричинное',
            colour=0x2F3136
        )
        ls = disnake.Embed(title='Ошибка.', description='**Причина**: У этого участника закрыт лс.', colour=0x2F3136)
        try:
            member = await interaction.guild.fetch_member(a[0])
            try:
                await member.send(embed=send_embed_ank)
                cur.execute(f'''DELETE FROM anketa WHERE msg_id = {interaction.message.id}''')
                await interaction.send("Отклоняю...", ephemeral=True)
                await interaction.message.delete()
            except:
                await interaction.send(embed=ls)
        except Exception as e:
            await interaction.send(embed=left)
        con.commit()
        con.close()

    @disnake.ui.button(label="Отклонить по причине", style=ButtonStyle.danger, custom_id="noreason")
    async def otkl2(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        left = disnake.Embed(title='Ошибка.', colour=0x2F3136, description='**Причина**: Человек покинул дискорд сервер.')
        ls = disnake.Embed(title='Ошибка.', description='**Причина**: У этого участника закрыт лс.', colour=0x2F3136)
        try:
            try:
                await interaction.response.send_modal(modal=lank2(bot=self.bot))
                await interaction.send("Отклоняю...", ephemeral=True)
            except:
                await interaction.send(embed=ls)
        except Exception as e:
            await interaction.send(embed=left)

class lank2(disnake.ui.Modal):
    def __init__(self, bot):
        self.bot = bot
        components = [
            disnake.ui.TextInput(
                label="Причина",
                placeholder="Укажите причину отказа",
                custom_id="reason",
                style=disnake.TextInputStyle.short,
                min_length=0,
                max_length=16,
            ),
        ]
        super().__init__(title="Причина", custom_id="create_reason", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        con = sqlite3.connect('LastEmpires.db')
        cur = con.cursor()
        a = cur.execute(f'''SELECT member_id FROM anketa WHERE msg_id = ({inter.message.id})''').fetchone()
        member = await inter.guild.fetch_member(a[0])
        success2 = disnake.Embed(title='Отклоняю...', colour=0x2F3136, description=f"Указанная причина: {inter.text_values['reason']}")
        send_embed_ank = disnake.Embed(
            title='К сожалению ваша заявка была отклонена',
            description=f"Причина: {inter.text_values['reason']}",
            colour=0x2F3136
        )
        await member.send(embed=send_embed_ank)
        await inter.send(embed=success2, ephemeral=True)

class modalank(disnake.ui.Modal):
    def __init__(self, bot):
        self.bot = bot
        components = [
            disnake.ui.TextInput(
                label="Какой ваш ник в minecraft?",
                placeholder="Например: Vupsenn_",
                custom_id="nick",
                style=disnake.TextInputStyle.short,
                min_length=0,
                max_length=16,
            ),
            disnake.ui.TextInput(
                label="Сколько вам лет",
                placeholder="Напишите сюда сколько вам реальных полных лет",
                custom_id="old",
                style=disnake.TextInputStyle.paragraph,
                min_length=0,
                max_length=3,
            ),
            disnake.ui.TextInput(
                label="Расскажите немного о себе",
                placeholder="Напишите немного о себе",
                custom_id="description",
                style=disnake.TextInputStyle.paragraph,
                min_length=100,
                max_length=400,
            ),
            disnake.ui.TextInput(
                label="Откуда узнали о нас (Если игрок то его ник)?",
                placeholder="Например: От Nykk3t",
                custom_id="what",
                style=disnake.TextInputStyle.paragraph,
                min_length=0,
                max_length=250,
            ),
        ]
        super().__init__(title="Заявка", custom_id="create_ank", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        cb_embed = disnake.Embed(title="Анкета", colour=0x2F3136, description=f"**Автор:** {inter.author.mention}\n"
                                                                              f"**Ник:** {inter.text_values['nick']}\n"
                                                                              f"**Возраст:** {inter.text_values['old']}\n"
                                                                              f"**О себе:** {inter.text_values['description']}\n\n"
                                                                              f"**Откуда узнал(-а):** {inter.text_values['what']}\n")
        channel = self.bot.get_channel(123456789000000000) #Тут должен быть id канала для рассмотрения заявок
        success = disnake.Embed(title='Заявка отправлена!', description='Ожидайте час или получаса, пока вам не ответит модерация', colour=0x2F3136)
        m = await channel.send(embed=cb_embed, view=prinorkl(bot=self.bot))
        con = sqlite3.connect('LastEmpires.db')
        cur = con.cursor()
        cur.execute(f'''INSERT INTO anketa VALUES ({m.id}, {inter.author.id}, '{inter.text_values['nick']}')''')
        con.commit()
        con.close()
        await inter.send(embed=success, ephemeral=True)

    async def on_error(self, error: Exception, inter: disnake.ModalInteraction):
        print(error)
        await inter.response.send_message("Произошла какая-то ошибка, она уже передана администратору.", ephemeral=True)


class anketab(disnake.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @disnake.ui.button(label="Написать заявку", style=ButtonStyle.primary, custom_id="ank")
    async def ank(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.send_modal(modal=modalank(bot=self.bot))



class anketa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_views_added = False

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.persistent_views_added:
            self.bot.add_view(anketab(bot=self.bot))
            self.bot.add_view(prinorkl(bot=self.bot))
            self.persistent_views_added = True

    @commands.command() #Создание бд в которой будет вся информацию о заявках
    async def bdas(self, ctx):
        con = sqlite3.connect('LastEmpires.db')
        cur = con.cursor()
        cur.execute('''CREATE TABLE anketa (msg_id INT, member_id INT, member_nick TEXT)''')
        con.commit()
        con.close()

    @commands.command() #Команда для отправки embed'a с кнопкой подачи заявки
    async def start(self, ctx):
        start_embed = disnake.Embed(title="Добро пожаловать!", colour=0x2F3136, description="– MineWeeks - приватный сервер для воплощения ваших идей и новых знакомств! У нас вы можете погрузиться в **улучшенный ванильный** игровой процесс, который не искажён различными, давно изжившими себя плагинами, а только дополнен новыми небольшими механиками.\n\n**Вход на сервер**\n– Ip сервера - play.mineweeks.ru или 5.9.143.176:25586\n– Версия - 1.19-1.19.2\n– Веб-карта - http://65.108.130.198:25789/\n\n**Моды (необязательно)**\n– Используемые моды: PlasmoVoice, EmoteCraft– Более подробная информация о модах и установке на сайте - https://www.mineweeks.ru/game/mods")
        start_embed.set_image(url="https://cdn.discordapp.com/attachments/982262896887218227/994597896706072719/2022-01-02_18.00.49.png")
        await ctx.send(embed=start_embed, view=anketab(bot=self.bot))


def setup(bot):
    bot.add_cog(anketa(bot))