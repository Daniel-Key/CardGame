class CardKeyword:
    name = "Generic Keyword"
    power_modifier = 0
    health_modifier = 0
    adjacent_effect = False
    stage = None

class AttackStage:
    BEFORE_ATTACK = "Before attack"
    DURING_ATTACK = "During attack"
    AFTER_ATTACK = "After attack"

class Chonky(CardKeyword):
    name = "Chonky"
    power_modifier = -1
    health_modifier = 2

class Angy(CardKeyword):
    name = "Angy"
    power_modifier = 2
    health_modifier = -1

class Shielded(CardKeyword):
    name = "Shielded"
    health_modifier = -2
    keyword_description = "Reduce first instance of damage to 0"
    triggered = False
    stage = AttackStage.BEFORE_ATTACK