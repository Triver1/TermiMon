import os
from google import genai
from google.genai import types

prompts = {
    "breed": "You will now breed these two mons together to create a new one, base the stats on the parents also. Try to not include the parents in the description, just base it on the new pokemon concept. Base the new name and lore on real life or pop culture. For example Aquawormie and Firepookie would create Steambunny",
    "starter": "You will now create a startermon, this one should be pretty special but not legendary like. These should be common."
}


def generate(prompt, rarity="Common", extra=""):
    client = genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Generate a firetype starter mon.
The icon is one emoji representative, MAKE SURE THIS IS ONLY ONE EMOJI. 
The pokemon should have some lore in the description and accurate variables based on this. 
Be really original and creative. Base them on real life or pop culture. The rarity should be as logical as possible, try not to make pokemons to rare."""),
                types.Part.from_text(text=prompt + extra),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            required=["Moves", "Weight", "Dimensions", "Stats"],
            properties={
                "Name": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "Types": genai.types.Schema(
                    type=genai.types.Type.ARRAY,
                    items=genai.types.Schema(
                        type=genai.types.Type.STRING,
                        enum=["Fire", "Grass", "Steel", "Air", "Earth", "Water", "Electric",
                              "Technic", "Cosmic", "Dragon", "Mythic", "Ghost", "Sound"],
                    ),
                ),
                "Rarity": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    enum=["Common", "Uncommon", "Rare",
                          "Legendary", "Mythic"],
                ),
                "Moves": genai.types.Schema(
                    type=genai.types.Type.ARRAY,
                    items=genai.types.Schema(
                        type=genai.types.Type.OBJECT,
                        required=["Movename", "Description", "Damage",
                                  "Type", "Statuseffect", "Chance", "Cooldown"],
                        properties={
                            "Movename": genai.types.Schema(
                                type=genai.types.Type.STRING,
                            ),
                            "Description": genai.types.Schema(
                                type=genai.types.Type.STRING,
                            ),
                            "Damage": genai.types.Schema(
                                type=genai.types.Type.NUMBER,
                            ),
                            "Type": genai.types.Schema(
                                type=genai.types.Type.STRING,
                                enum=["Fire", "Grass", "Steel", "Air", "Earth", "Water", "Electric",
                                      "Technic", "Cosmic", "Dragon", "Mythic", "Ghost", "Sound"],
                            ),
                            "Statuseffect": genai.types.Schema(
                                type=genai.types.Type.STRING,
                                enum=["Burn", "Freeze", "Paralyze", "Poison",
                                      "Sleep", "Stun", "Confuse", "None"],
                            ),
                            "Chance": genai.types.Schema(
                                type=genai.types.Type.NUMBER,
                            ),
                            "Cooldown": genai.types.Schema(
                                type=genai.types.Type.NUMBER,
                            ),
                        },
                    ),
                ),
                "Icon": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "Weight": genai.types.Schema(
                    type=genai.types.Type.NUMBER,
                    description="Weight in kilograms",
                ),
                "Dimensions": genai.types.Schema(
                    type=genai.types.Type.OBJECT,
                    required=["Length", "Width", "Height"],
                    properties={
                        "Length": genai.types.Schema(
                            type=genai.types.Type.NUMBER,
                            description="Length in meters",
                        ),
                        "Width": genai.types.Schema(
                            type=genai.types.Type.NUMBER,
                            description="Width in meters",
                        ),
                        "Height": genai.types.Schema(
                            type=genai.types.Type.NUMBER,
                            description="Height in meters",
                        ),
                    },
                ),
                "Stats": genai.types.Schema(
                    type=genai.types.Type.OBJECT,
                    required=["damage", "magic", "health",
                              "defense", "magicdefense", "speed"],
                    properties={
                        "damage": genai.types.Schema(
                            type=genai.types.Type.NUMBER,
                        ),
                        "magic": genai.types.Schema(
                            type=genai.types.Type.NUMBER,
                        ),
                        "health": genai.types.Schema(
                            type=genai.types.Type.NUMBER,
                        ),
                        "defense": genai.types.Schema(
                            type=genai.types.Type.NUMBER,
                        ),
                        "magicdefense": genai.types.Schema(
                            type=genai.types.Type.NUMBER,
                        ),
                        "speed": genai.types.Schema(
                            type=genai.types.Type.NUMBER,
                        ),
                    },
                ),
                "description": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
            },
        ),
    )

    result = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text)
        result += chunk.text
    return result


def breed(termimon1, termimon2):
    prompt = prompts["breed"]
    extra = f"\nTermimon 1: {termimon1}\nTermimon 2: {termimon2}"
    return generate(prompt, extra)


def startermon(startertype):
    prompt = prompts["starter"]
    return generate(prompt, extra=f"\nStarter type: {startertype}")
