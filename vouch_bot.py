# By CocaLite , discord.gg/brtnleak

import discord
from discord.ext import commands
from discord import app_commands
import datetime
import os
from typing import Optional

TOKEN = ""
VOUCH_CHANNEL_ID = None

def stars_to_emoji(n: int) -> str:
    return "⭐" * max(1, min(5, n))

def build_vouch_embed(
    author: discord.Member,
    message: str,
    stars: int,
    proof_url: Optional[str],
    target: Optional[discord.Member] = None,
) -> discord.Embed:
    embed = discord.Embed(
        title="New Vouch Created!",
        color=0xF5A623,
    )
    embed.add_field(name="Vouch:", value=f"{stars_to_emoji(stars)}\n{message}", inline=False)

    now_str = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
    embed.add_field(name="Vouched by", value=author.mention, inline=True)
    embed.add_field(name="Vouched at", value=now_str, inline=True)

    if target:
        embed.add_field(name="Vouched for", value=target.mention, inline=False)

    if proof_url:
        embed.set_image(url=proof_url)

    embed.set_thumbnail(url=author.display_avatar.url)
    embed.set_footer(text="Powered By CocaLite Vouches • Today")
    return embed

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Connected as {bot.user}  (ID: {bot.user.id})")

@tree.command(name="vouch", description="Create a vouch for a user or a service.")
@app_commands.describe(
    message="Vouch message (required)",
    stars="Number of stars from 1 to 5 (required)",
    proof="Proof image to upload directly (required)",
    target="Vouched user (optional)",
)
@app_commands.choices(stars=[
    app_commands.Choice(name="⭐⭐⭐⭐⭐ (5)", value=5),
    app_commands.Choice(name="⭐⭐⭐⭐  (4)", value=4),
    app_commands.Choice(name="⭐⭐⭐   (3)", value=3),
    app_commands.Choice(name="⭐⭐    (2)", value=2),
    app_commands.Choice(name="⭐     (1)", value=1),
])
async def vouch_cmd(
    interaction: discord.Interaction,
    message: str,
    stars: int,
    proof: discord.Attachment,
    target: Optional[discord.Member] = None,
):
    await interaction.response.defer(ephemeral=False)

    if not proof.content_type or not proof.content_type.startswith("image/"):
        await interaction.followup.send(
            "❌ The proof must be an **image** (PNG, JPG, GIF, WEBP…).", ephemeral=True
        )
        return

    embed = build_vouch_embed(
        author=interaction.user,
        message=message,
        stars=stars,
        proof_url=proof.url,
        target=target,
    )

    if VOUCH_CHANNEL_ID:
        channel = interaction.guild.get_channel(VOUCH_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed)
            await interaction.followup.send(
                f"✅ Vouch created and posted in {channel.mention}!", ephemeral=True
            )
            return

    await interaction.followup.send(embed=embed)

if __name__ == "__main__":
    bot.run(TOKEN)
