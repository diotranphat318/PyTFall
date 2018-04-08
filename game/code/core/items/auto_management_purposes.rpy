init python:
    FIGHTING_AEQ_PURPOSES = [
    "Combat",
    "Barbarian",
    "Shooter",
    "Battle Mage",
    "Mage"
    ]

    AEQ_PURPOSES = {
    "Combat":
        {"target_stats": ['health', 'mp', 'attack', 'magic', 'defence', 'agility', "luck"],
         "exclude_on_stats": ["luck", 'attack', "defence"],
         "target_skills": [],
         "exclude_on_skills": [],
         "base_purpose": ["Warrior"],
         "sub_purpose": [],
         "real_weapons": True},
    "Manager":
        {"target_stats": ["charisma", 'constitution', 'agility', "luck"],
         "exclude_on_stats": ["charisma", "luck"],
         "target_skills": ["management"],
         "exclude_on_skills": ["management"],
         "base_purpose": ["Manager"],
         "sub_purpose": ["Casual"],
         "real_weapons": False},
    "Casual":
        {"target_stats": ["charisma", 'constitution', 'agility', "luck"],
         "exclude_on_stats": ["charisma", "luck"],
         "target_skills": [],
         "exclude_on_skills": [],
         "base_purpose": ["Casual"],
         "sub_purpose": [],
         "real_weapons": False},
    "Slave":
        {"target_stats": ["charisma", 'constitution', 'agility', "luck"],
         "exclude_on_stats": [],
         "target_skills": [],
         "exclude_on_skills": [],
         "base_purpose": ["Slave"],
         "sub_purpose": ["Casual"],
         "real_weapons": False},
    "Barbarian":
        {"target_stats": ['health', 'attack', 'defence', 'constitution', 'agility'],
         "exclude_on_stats": ['health', 'attack'],
         "target_skills": [],
         "exclude_on_skills": [],
         "base_purpose": ["Warrior"],
         "sub_purpose": [],
         "real_weapons": True},
    "Shooter":
        {"target_stats": ["agility", 'attack', 'defence', "luck"],
         "exclude_on_stats": ["agility", "luck"],
         "target_skills": [],
         "exclude_on_skills": [],
         "base_purpose": ["Shooter"],
         "sub_purpose": ["Warrior"],
         "real_weapons": True},
    "Battle Mage":
        {"target_stats": ['health', 'mp', 'attack', 'magic'],
         "exclude_on_stats": ['magic', 'attack'],
         "target_skills": [],
         "exclude_on_skills": [],
         "base_purpose": ["Warrior", "Mage"],
         "sub_purpose": [],
         "real_weapons": True},
    "Mage":
        {"target_stats": ['mp', 'magic', "luck", 'intelligence'],
         "exclude_on_stats": ['magic', 'mp'],
         "target_skills": [],
         "exclude_on_skills": [],
         "base_purpose": ["Mage"],
         "sub_purpose": ["Warrior"],
         "real_weapons": True},
    "Striptease":
        {"target_stats": ["charisma"],
         "exclude_on_stats": ["charisma", "vitality"],
         "target_skills": ["strip", "dancing"],
         "exclude_on_skills": ["strip"],
         "base_purpose": ["Stripper"],
         "sub_purpose": ["SIW"],
         "real_weapons": False},
    "Sex":
        {"target_stats": ["charisma"],
         "exclude_on_stats": ["charisma"],
         "target_skills": ["sex", "vaginal", "anal", "oral"],
         "exclude_on_skills": ["sex", "vaginal", "anal", "oral"],
         "base_purpose": ["Whore"],
         "sub_purpose": ["SIW"],
         "real_weapons": False},
    "Service":
        {"target_stats": ["charisma"],
         "exclude_on_stats": [],
         "target_skills": ["service", "cleaning"],
         "exclude_on_skills": ["service", "cleaning"],
         "base_purpose": ["Service"],
         "sub_purpose": [],
         "real_weapons": False}
    }
