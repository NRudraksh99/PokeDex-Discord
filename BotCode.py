from httpx import AsyncClient,HTTPError
from discord import Intents,File
from discord.ext import commands
from os.path import dirname

Intents = Intents.default()
Intents.message_content = True  # Enable message content intent if needed

p=dirname(__file__)
client = commands.Bot(command_prefix="!",intents=Intents)

async def get_info_move(move):
    async with AsyncClient() as ac:
        url=f"https://pokeapi.co/api/v2/move/{move.lower()}/"
        try:
            response=await ac.get(url)
            response.raise_for_status()
            return response.json()
        except HTTPError as exc:
            print(f"HTTP error while fetching {url}: {exc}")
        except Exception as exc:
            print(f"An error occurred while fetching {url}: {exc}")

async def get_info_ability(ability:str):
    async with AsyncClient() as ac:
        url=f"https://pokeapi.co/api/v2/ability/{ability.lower()}/"
        try:
            response=await ac.get(url)
            response.raise_for_status()
            return response.json()
        except HTTPError:
            print("HTTP Error occurred...")
        except Exception:
            print("Error while fetching details....")

async def get_info_item(item):
    async with AsyncClient() as ac:
        url = f"https://pokeapi.co/api/v2/item/{item.lower()}/"
        try:
            response = await ac.get(url)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            return response.json()
        except HTTPError as exc:
            print(f"HTTP error while fetching {url}: {exc}")
        except Exception as exc:
            print(f"An error occurred while fetching {url}: {exc}")

async def get_info(pokemon_name):
    async with AsyncClient() as ac:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/"
        try:
            response = await ac.get(url)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            return response.json()
        except HTTPError as exc:
            print(f"HTTP error while fetching {url}: {exc}")
        except Exception as exc:
            print(f"An error occurred while fetching {url}: {exc}")

@client.command()
async def commands(ctx):
    await ctx.send("""The commands supported by me are:
- !info <pokemon_name> to view details about a certain pokemon.
- !show <pokemon_name> to view the default front and rear sprites of a pokemon.
- !shiny <pokemon_name> to view the shiny sprites of a pokemon.
- !item <item_name> to view a description of a specified item.
- !cry <pokemon_name> to get an audio file of the cry of a pokemon.
- !move <attack_name> to get information regarding a move/attack.
- !ability <ability_name> to get information regarding any Pokemon ability.
""")

@client.command()
async def hello(ctx):
    await ctx.send("Hello! Nice to meet you!! How may I help you in your Pokemon research?")

@client.command()
async def thanks(ctx):
    await ctx.send("Glad to hear I managed to help you 😊")

@client.command()
async def ability(ctx,ability:str):
    try:
        print(f"Fetching details about {ability}.....")
        result=await get_info_ability(ability.lower())
        if result and isinstance(result,dict):
            english_flavor_texts = (([entry["flavor_text"] for entry in result.get('flavor_text_entries', []) if entry.get('language', {}).get('name', '') == 'en'])[0]).replace("\n"," ")
            await ctx.send(f'''Some information about the ability {ability.capitalize()}
{english_flavor_texts}
''')
        else:
            await ctx.send("No information found about this attack....")
    except Exception:
        await ctx.send("Unfortunately, an error occurred, please try again....")

def get_stats(x:dict) -> str:
    s=""
    for i in x.keys():
        s+=f"{i.capitalize()}:  {x[i]}\n"
    return s

async def download_image(image_url, name):
    async with AsyncClient() as ac:
        try:
            response = await ac.get(image_url)
            response.raise_for_status()
            with open(f"{p}\\{name}.png", 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded successfully!")
        except HTTPError as exc:
            print(f"HTTP error while fetching {image_url}: {exc}")
        except Exception as exc:
            print(f"An error occurred while fetching {image_url}: {exc}")

@client.command()
async def cry(ctx,pokemon):
    try:
        print("Fetching cry....")
        result=await get_info(pokemon.lower())
        if not result:
            raise TypeError
        else:
            c=result["cries"]["latest"]
            async with AsyncClient() as ac:
                result=await ac.get(c)
                with open(f"{p}\\temp.ogg","wb") as cry_file:
                    cry_file.write(result.content)
            print("Cry saved!")
            await ctx.send(f"Here is the cry of the pokemon {pokemon.capitalize()}.",file=File(f"{p}\\temp.ogg"))
    except:
        await ctx.send("No cry was found for this pokemon.... please try again....")

@client.command()
async def move(ctx,move_name:str):
    try:
        print(f"Fetching details about the move {move_name}.....")
        result=await get_info_move(move_name.lower())
        if result and isinstance(result,dict):
            english_flavor_texts = (([entry["flavor_text"] for entry in result.get('flavor_text_entries', []) if entry.get('language', {}).get('name', '') == 'en'])[0]).replace("\n"," ")
            await ctx.send(f'''Some information about the move/attack {move_name.capitalize()}
- Type: {result["type"]["name"].capitalize()}
- Accuracy: {result["accuracy"]}
- Base Power: {result["power"]}
- Base PP (Power Points): {result["pp"]}
- Description: {english_flavor_texts}
''')
        else:
            await ctx.send("No information found about this attack....")
    except Exception:
        await ctx.send("Unfortunately, an error occurred, please try again....")

@client.command()
async def show(ctx,pokemon):
    try:
        print(f"Creating sprites of {pokemon}.....")
        result=await get_info(pokemon.lower())
        result=result['id']
        await download_image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{result}.png","front")
        await ctx.send("Front",file=File(f"{p}\\front.png"))
        await download_image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{result}.png","rear")
        await ctx.send("Rear",file=File(f"{p}\\rear.png"))
    except Exception as e:
        print(f"Error {e} Occurred.....")
        await ctx.send("An error occurred.... please try again....")

@client.command()
async def shiny(ctx,pokemon):
    result=await get_info(pokemon.lower())
    result=result['id']
    await download_image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/shiny/{result}.png","front_shiny")
    await ctx.send(f"Sprite of a shiny {pokemon.capitalize()}",file=File(f"{p}\\front_shiny.png"))

@client.command()
async def info(ctx, pokemon):
    try:
        print(f"Fetching details of {pokemon}.....")
        result = await get_info(pokemon.lower())
        if result and isinstance(result, dict):
            types=[i["type"]["name"].capitalize() for i in result.get("types",[])]
            abilities = [ability["ability"]["name"] for ability in result.get("abilities", [])]
            stats={stat['stat']['name']: stat['base_stat'] for stat in result['stats']}
            await ctx.send(f'''Some details about the pokemon {pokemon.capitalize()} are shown below:
- Type(s): {', '.join(types)}\t
- Height = {result.get('height', 0) / 10} meters
- Weight = {result.get('weight', 0) / 10} kilograms
- Abilities = {', '.join(abilities)}\t
- Base Stats:
{get_stats(stats)}
''')
        else:
            await ctx.send(f"No information found for {pokemon.capitalize()}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        await ctx.send("An error occurred. Please try again.")

@client.command()
async def item(ctx,item_name:str):
    try:
        r=f"Here are some details about the item {item_name.capitalize()}:\n"
        print(f"Fetching some details about {item_name}....")
        result= await get_info_item(item_name.lower())
        if result['category']['name']:
            r+=f"- Category: {result['category']['name'].capitalize()}"
        if result and isinstance(result,dict):
            english_flavor_texts = (([entry['text'] for entry in result.get('flavor_text_entries', []) if entry.get('language', {}).get('name', '') == 'en'])[0]).replace("\n"," ")
            r+=f"\n{english_flavor_texts}. This is what it looks like:"
            await download_image(result["sprites"]["default"],f"item_temp")
            await ctx.send(r,file=File(f"{p}\\item_temp.png"))
        else:
            await ctx.send("Unfortunately, no information was found....")
    except TypeError:
        await ctx.send("Unfortunately, no information was found for this item....")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

client.run("<bot_token_goes_here>")
