from card_keyword import AttackStage

class Status:
    name = "Generic Status"
    keyword_description = ""
    stage = None

class Poisoned(Status):
    name = "Poisoned"
    keyword_description = "This card has been poisoned"
    stage = AttackStage.AFTER_ATTACK