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

class Eager(CardKeyword):
    name = "Eager"
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

class Whirling(CardKeyword):
    name = "Whirling"
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
    keyword_description = "Any overkill damage after an attack is dealt to an adjacent card"
    stage = AttackStage.AFTER_ATTACK

class Cheerleading(CardKeyword):
    name = "Cheerleading"
    power_modifier = -1
    keyword_description = "When an adjacent card attacks, give it +1 health"
    stage = AttackStage.AFTER_ATTACK

class Avenging(CardKeyword):
    name = "Avenging"
    power_modifier = -1
    keyword_description = "Gains +1 power after friendly card is destroyed"
    stage = AttackStage.AFTER_ATTACK

class Vicious(CardKeyword):
    name = "Vicious"
    keyword_description = "Deals +1 damage to cards with less health than this"

class Spiky(CardKeyword):
    name = "Spiky"
    power_modifier = -1
    keyword_description = "Before being attacked, deal 1 damage back"
    stage = AttackStage.BEFORE_ATTACK

class Toxic(CardKeyword):
    name = "Toxic"
    power_modifier = -1
    keyword_description = "On dealing damage, applies a poison which deals 1 damage at the end of the enemy's turn"

class Skulking(CardKeyword):
    name = "Skulking"
    power_modifier = -3
    keyword_description = "On death, steals a random enemy card"
    stage = AttackStage.AFTER_ATTACK

class Distractible(CardKeyword):
    name = "Distractible"
    power_modifier = 1
    keyword_description = "Deals damage randomly split between all enemy cards"

class Rooted(CardKeyword):
    name = "Rooted"
    health_modifier = 2
    keyword_description = "+2 health while this remains in its initial position"
    stage = AttackStage.AFTER_ATTACK

class Disruptive(CardKeyword):
    name = "Disruptive"
    keyword_description = "Swaps position of attacked card with an adjacent one"
    stage = AttackStage.AFTER_ATTACK

class Generous(CardKeyword):
    name = "Generous"
    power_modifier = -1
    health_modifier = -1
    keyword_description = "At start of game distributes its stats randomly to friendly cards before being removed"

class Charmed(CardKeyword):
    name = "Charmed"
    power_modifier = 1
    keyword_description = "Deal no damage to the rightmost card"