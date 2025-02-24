from django import template

register = template.Library()

@register.filter
def findcard(player_cards, card_name):
    for player_card in player_cards:
        if player_card.card.name == card_name:
            return player_card
    return None

@register.filter
def replace_space(value):
    """Replaces spaces with underscores in a string."""
    return value.replace(" ", "_")
