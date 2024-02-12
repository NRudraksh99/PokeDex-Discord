import requests
import validators
from discord import Intents,File
from discord.ext import commands
from os.path import dirname


Intents = Intents.default()
Intents.message_content = True  # Enable message content intent if needed

p=dirname(__file__)
# Could add command prefix !!
client = commands.Bot(command_prefix=None ,intents = Intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(".hello"):
        user_name = message.author
        await message.channel.send(f"Hello {user_name}!")

    if message.content.startswith(".info"):
        try:
            pokemon = message.content.split()[1].lower()
            if not validators.url(f"https://pokeapi.co/api/v2/pokemon/{pokemon}/"):
                raise ValueError("Invalid Pokémon name. Please try again.")
        except (IndexError, ValueError):
            await message.channel.send(
                "Please provide a valid Pokémon name after the .info command."
            )
            return
        
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}/")

        if response.status_code == 200:
            data = response.json()
            height_in_meters = data['height'] / 10
            weight_in_kilograms = data['weight'] / 10

            info_message = f"""
            Some information regarding the Pokémon {pokemon.capitalize()}:
            => Height = {height_in_meters} meters
            => Weight = {weight_in_kilograms} kilograms
            """
            await message.channel.send(info_message)
        else:
            await message.channel.send(f"Error fetching data (status code: {response.status_code})")

    if message.content.startswith(".desc"):
        try:
            pokemon = message.content.split()[1].lower()
            if not validators.url(f"https://pokeapi.co/api/v2/pokemon/{pokemon}/"):
                raise ValueError("Invalid Pokemon name. Please try again.")
        except(IndexError,ValueError):
            await message.channel.send("Please provide a valid Pokemon name after the .desc command.")
            return    

        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}/")   

        if response.status_code == 200:
            data = response.json()

            # Extracting species URL from the response
            species_url = data["species"]["url"]
        
            # Making a request to the species endpoint
            species_response = requests.get(species_url)
        
            if species_response.status_code == 200:
                species_data = species_response.json()
            
                # Extracting the flavor text (description) from the species data
                flavor_text_entries = species_data["flavor_text_entries"]

                # Assuming English language, you can filter for entries with language "en"
                english_entries = [entry for entry in flavor_text_entries if entry["language"]["name"] == "en"]
            
                if english_entries:
                    description = english_entries[0]["flavor_text"]
                    desc_message = f"""
                    Description regarding the Pokémon {pokemon.capitalize()}:
                    => Description = {description}
                    """
                    await message.channel.send(desc_message)
                else:
                    await message.channel.send("No English flavor text entry found.")
            else:
                await message.channel.send(f"Error fetching species data (status code: {species_response.status_code})")
        else:
            await message.channel.send(f"Error fetching Pokemon data (status code: {species_response.status_code})")

    if message.content.startswith(".getcry"):
        try:
            pokemon = message.content.split()[1].lower()
            if not validators.url(f"https://pokeapi.co/api/v2/pokemon/{pokemon}/"):
                raise ValueError("Invalid Pokemon name. Please try again.")
        except(IndexError,ValueError):
            await message.channel.send("Please provide a valid Pokemon name after the .getcry command.")
            return
        
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}/")

        if response.status_code == 200:
            data = (response.json().get("cries")).get("legacy")
            download_path = dirname(__file__)
            with open(f"{download_path}\\temp.mp3","wb") as file:
                file.write(data)
                print("Succes")
            await message.channel.send(file = File(f"{download_path}\\temp.mp3"))
        else:
            print("Operation failed")        
    else:
        await message.channel.send(f"Error fetching Pokemon data (status code: {species_response.status_code})")

client.run("{secret token goes here!")
