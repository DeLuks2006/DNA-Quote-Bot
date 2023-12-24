from discord import Interaction


def is_admin(interaction: Interaction) -> bool:
    return interaction.permissions.administrator


def is_moderator(interaction: Interaction) -> bool:
    return interaction.permissions.manage_messages
