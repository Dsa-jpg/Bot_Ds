import discord
import os
from webserver import keep_alive
from discord.ext import commands

# Inicializace Discord bota
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


# Nastavení vlastní přítomnosti
@client.event
async def on_ready():
  """
    Metoda volaná při připojení bota k Discordu.
    Nastavuje vlastní přítomnost bota.
    """
  await client.change_presence(activity=discord.Game(
    name="Čekám na nové studenty"))
  print(f"Bot přihlášen jako {client.user}")


# Odeslání instrukcí novým členům přes soukromou zprávu
@client.event
async def on_member_join(member):
    try:
        welcome_message = f"Ahoj {member}, Vítej na serveru JČU PŘF! Pro přiřazení role přejdi na serveru do roomky role-selector."
        await member.send(welcome_message)
        print(f"Zpráva odeslána {member}")
    except discord.errors.HTTPException as e:
        if e.status == 50007:
            print(f"Cannot send welcome message to {member}: DMs disabled.")
        else:
            print(f"Error sending welcome message to {member}: {e}")



# Reakce na přidání reakce k zprávě
@client.event
async def on_raw_reaction_add(payload):
  """
    Metoda volaná při přidání reakce k zprávě.
    Přidá příslušnou roli uživateli podle provedené reakce.
    """
  message_id = payload.message_id
  if message_id == 1021025890949398590:
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

    role = discord.utils.get(guild.roles, name=payload.emoji.name)

    if role is not None:
      member = discord.utils.find(lambda m: m.id == payload.user_id,
                                  guild.members)
      if member is not None:
        await member.add_roles(role)
        print(f"Role {role} byla přídána uživatelem {member}.")
      else:
        print("Člen nenalezen.")

    else:
      print("Role nenalezena.")


# Reakce na odebrání reakce ze zprávy
@client.event
async def on_raw_reaction_remove(payload):
  """
    Metoda volaná při odebrání reakce ze zprávy.
    Odebere příslušnou roli uživateli podle odebrané reakce.
    """
  message_id = payload.message_id
  if message_id == 1021025890949398590:
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

    role = discord.utils.get(guild.roles, name=payload.emoji.name)

    if role is not None:
      member = discord.utils.find(lambda m: m.id == payload.user_id,
                                  guild.members)
      if member is not None:
        await member.remove_roles(role)
        print(f"Role {role} byla odebrána uživatelem {member}.")
      else:
        print("Člen nenalezen.")

    else:
      print("Role nenalezena.")


keep_alive()

TOKEN = os.environ.get("DISCORD_CODE")

try:
  client.run(TOKEN)
except:
  os.system("kill 1")
