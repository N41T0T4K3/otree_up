# food_pref/pages.py

from otree.api import *
from .models import C, Subsession, Group, Player

def food_label(code):
    labels = {
        'soba': 'そば',
        'udon': 'うどん',
        'tsubuan': 'つぶあん',
        'koshian': 'こしあん',
        'sushi': 'すし',
        'yakiniku': '焼肉',
        'tea': '紅茶',
        'coffee': 'コーヒー',
        'rice': 'ごはん',
        'bread': 'パン',
    }
    return labels.get(code, code)


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class WaitOthers0(WaitPage):
    pass

class Round1(Page):
    form_model = 'player'
    form_fields = ['preference', 'first_guess']

    def vars_for_template(self):
        food1, food2 = self.group.current_pair()
        return dict(
            food1=food1,
            food2=food2,
            food1_img = f'food_pref/{food1}.jpg',
            food2_img = f'food_pref/{food2}.jpg',
            food1_label = food_label(food1),
            food2_label = food_label(food2),
            initial_guess = self.player.field_maybe_none('first_guess') or 50,
        )

class WaitOthers(WaitPage):
    pass

class ShowOthers(Page):
    def vars_for_template(self):
        food1, food2 = self.group.current_pair()

        others = self.player.get_others_in_group()
        others_with_complements = []
        for p in others:
            others_with_complements.append({
                'id_in_group': p.id_in_group,
                'first_guess': p.first_guess,
                'complement': 100 - p.first_guess if p.first_guess is not None else None
            })

        return dict(
            food1_label=food_label(food1),
            food2_label=food_label(food2),
            others=others_with_complements
        )

class Round2(Page):
    form_model = 'player'
    form_fields = ['second_guess']

    def vars_for_template(self):
        food1, food2 = self.group.current_pair()
        return dict(
            food1_img = f'food_pref/{food1}.jpg',
            food2_img = f'food_pref/{food2}.jpg',
            food1_label = food_label(food1),
            food2_label = food_label(food2),
            initial_guess = self.player.field_maybe_none('second_guess') or 50,
        )

class WaitOthers2(WaitPage):
    pass

class Final(Page):
    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS

    def vars_for_template(self):
        return dict()


page_sequence = [Introduction, WaitOthers0, Round1, WaitOthers, ShowOthers, Round2, WaitOthers2, Final]
