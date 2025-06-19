# food_pref/models.py

from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'food_pref'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 5
    PAIRS = [
        ('soba', 'udon'),
        ('tsubuan', 'koshian'),
        ('sushi', 'yakiniku'),
        ('tea', 'coffee'),
        ('rice', 'bread')
    ]


class Subsession(BaseSubsession):
    def creating_session(subsession: 'Subsession'):
        import random
        pair_list = C.PAIRS.copy()
        if subsession.round_number == 1:
            for group in subsession.get_groups():
                random.shuffle(pair_list)
                group.session.vars[f'order_{group.id_in_subsession}'] = pair_list.copy()


class Group(BaseGroup):
    def current_pair(self):
        return self.session.vars[f'order_{self.id_in_subsession}'][self.subsession.round_number - 1]


class Player(BasePlayer):
    preference = models.StringField()
    first_guess = models.IntegerField(min=0, max=100)
    second_guess = models.IntegerField(min=0, max=100)
