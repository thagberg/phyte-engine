import factory
import player
import json
import pygame


class CharacterNotFoundError(Exception):
    def __init__(self, value):
        self.value = value 

    def __str__(self):
        return 'No character found for %s' % self.value


def load_character(character_name):
    # start by opening the file found at character_name.char
    file_name = '../content/%s.char' % character_name
    try:
        char_file = open(file_name)
    except IOError as e:
        raise CharacterNotFoundError(character_name)
    # parse the JSON config and return it as the config
    char_config = json.loads(char_file.read())
    return char_config

def create_player(character_config, entity_id=None):
    # first verify that we have a valid entity and
    # entity_id for this player
    if not entity_id:
        entity = factory.create_entity()
        entity_id = entity.entity_id
    else:
        entity = factory.get_entity(entity_id)
    # start pulling values off of the config
    char = character_config['character']
