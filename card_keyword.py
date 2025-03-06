class CardKeyword:
    name = "Generic Keyword"
    power_modifier = 0
    health_modifier = 0
    adjacent_effect = False
    stage = None
    keyword_description = ""

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
    stage = AttackStage.BEFORE_ATTACK

class Explosive(CardKeyword):
    name = "Explosive"
    power_modifier = -2
    keyword_description = "Deal 2 damage to all enemy cards on death"
    stage = AttackStage.AFTER_ATTACK

class Ranged(CardKeyword):
    name = "Ranged"
    health_modifier = -1
    keyword_description = "Deal 1 damage before attack"
    stage = AttackStage.BEFORE_ATTACK

class Prideful(CardKeyword):
    name = "Prideful"
    power_modifier = 1
    keyword_description = "Can only attack the highest health card"

class Myopic(CardKeyword):
    name = "Myopic"
    power_modifier = 1
    keyword_description = "Can only attack the leftmost card"

class Dervish(CardKeyword):
    name = "Dervish"
    keyword_description = "Can swap places with a friendly card after attack"
    stage = AttackStage.AFTER_ATTACK

class Ramping(CardKeyword):
    name = "Ramping"
    power_modifier = -1
    keyword_description = "Gains +1 power after attack"
    stage = AttackStage.AFTER_ATTACK

class Furious(CardKeyword):
    name = "Furious"
    health_modifier = -1
    keyword_description = "Any overkill damage is dealt to an adjacent card"
    stage = AttackStage.AFTER_ATTACK