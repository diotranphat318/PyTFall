label forest_dark:
    python:
        background_number = -1
        forest_bg_change = True
        # Build the actions
        if pytfall.world_actions.location("forest_entrance"):
            pytfall.world_actions.finish()
    
label forest_dark_continue:
    if forest_bg_change:
        $ background_number_list = list(i for i in range(1, 7) if i != background_number)
        $ background_number = choice(background_number_list)
        $ forest_location = "content/gfx/bg/locations/forest_" + str(background_number) + ".jpg"
    else:
        $ forest_bg_change = True
    scene expression forest_location
    with dissolve

    # Music related:
    if not "forest_entrance" in ilists.world_music:
        $ ilists.world_music["forest_entrance"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("forest_entrance")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["forest_entrance"])
    $ global_flags.del_flag("keep_playing_music")
    
    if not hero.flag('visited_deep_forest'):
        $ hero.set_flag('visited_deep_forest')
        $ block_say = True
        "You step away from the city walls and go deep into the forest. It's not safe here, better to be on guard."
        $ block_say = False
    
    show screen city_dark_forest
    
    while 1:
        $ result = ui.interact()
        if result in hero.team:
            $ came_to_equip_from = "forest_dark_continue"
            $ eqtarget = result
            $ global_flags.set_flag("keep_playing_music")
            $ equipment_safe_mode = True
            $ forest_bg_change = False
            hide screen city_dark_forest
            jump char_equip
            
screen city_dark_forest():
    use top_stripe(False, None, False, True)
    frame:
        xalign 0.95
        ypos 50
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            style_group "wood"
            align (0.5, 0.5)
            spacing 10
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("city_dark_forest"), Jump("city_dark_forest_explore"), With(dissolve)]
                text "Explore" size 15
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("city_dark_forest"), Jump("city_dark_forest_rest"), With(dissolve), SensitiveIf(hero.flag("dark_forest_rested_today") != day)]
                text "Rest" size 15
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("city_dark_forest"), Jump("forest_entrance"), With(dissolve)]
                text "Leave" size 15
                
label city_dark_forest_explore:
    if not(take_team_ap(1)):
        if len(hero.team) > 1:
            "Unfortunately your team is too tired at the moment. Maybe another time."
        else:
            "Unfortunately you are too tired at the moment. Maybe another time."
        $ global_flags.set_flag("keep_playing_music")
        jump forest_dark_continue
    else:
        if dice(25) and hero.flag("dark_forest_met_girl") != day:
            jump dark_forest_girl_meet
        elif dice(70) or hero.flag("dark_forest_met_bandits") == day:
            jump city_dark_forest_fight
        else:
            $ hero.set_flag("dark_forest_met_bandits", value=day)
            jump city_dark_forest_hideout
    
label city_dark_forest_rest:
    $ hero.set_flag("dark_forest_rested_today", value=day)
    $ forest_bg_change = False
    scene bg camp
    with dissolve
    "You take a short rest before moving on, restoring mp and vitality."
    $ forest_bg_change = False
    $ global_flags.set_flag("keep_playing_music")
    python:
        for i in hero.team:
            i.vitality += int(i.get_max("vitality")*0.25)
            i.health += int(i.get_max("health")*0.05)
            i.mp += int(i.get_max("mp")*0.2)
    jump forest_dark_continue
    
label city_dark_forest_hideout:
    hide screen city_dark_forest
    scene bg forest_hideout
    with dissolve
    $ forest_bg_change = False
    menu:
        "You found bandits hideout inside an old abandoned castle."
        
        "Attack them":
            "You carefully approach the hideout when a group of bandits attack you."
        "Leave them be":
            show screen city_dark_forest
            $ global_flags.set_flag("keep_playing_music")
            jump forest_dark_continue
    call city_dark_forest_hideout_fight
    $ N = randint(1, 3)
    $ j = 0
    while j < N:
        scene bg forest_hideout
        with dissolve
        "Another group is approaching you!"
        call city_dark_forest_hideout_fight
        $ j += 1
    show screen give_exp_after_battle(hero.team)
    pause 2.5
    hide screen give_exp_after_battle
    show screen city_dark_forest
    scene bg forest_hideout
    with dissolve
    "After killing all the bandits you found stash with loot."
    call give_to_mc_item_reward(type="loot", price=300)
    if locked_dice(50):
        call give_to_mc_item_reward(type="loot", price=300)
    call give_to_mc_item_reward(type="restore", price=100)
    if locked_dice(50):
        call give_to_mc_item_reward(type="restore", price=200)
    if locked_dice(50):
        call give_to_mc_item_reward(type="armor", price=300)
    if locked_dice(50):
        call give_to_mc_item_reward(type="weapon", price=300)
    jump forest_dark_continue

label city_dark_forest_hideout_fight:
    python:
        enemy_team = Team(name="Enemy Team", max_size=3)
        levels = 0
        for i in hero.team:
            levels += i.level
        levels = int(levels/len(hero.team))+randint(0, 5)
        levels = 1
        for i in range(3):
            mob_id = choice(["Samurai", "Warrior", "Archer", "Soldier", "Barbarian", "Orc", "Infantryman", "Thug", "Mercenary", "Dark Elf Archer"])
            mob = build_mob(id=mob_id, level=levels)
            mob.controller = BE_AI(mob)
            enemy_team.add(mob)
    $ place = interactions_pick_background_for_fight("forest")
    $ result = run_default_be(enemy_team, background=place, slaves=True, prebattle=False, death=True)
    if result is True:
        python:
            for member in hero.team:
                member.exp += adjust_exp(member, 250)
        scene expression forest_location
        return

label city_dark_forest_fight:
    $ forest_bg_change = False
    python:
        enemy_team = Team(name="Enemy Team", max_size=3)
        levels = 0
        for i in hero.team:
            levels += i.level
        levels = int(levels/len(hero.team))+randint(0, 5)
        mob = choice(["slime", "were", "harpy", "goblin", "wolf", "bear", "druid", "rat", "undead", "butterfly"])
    if mob == "slime":
        "You encountered a small group of predatory slimes."
        python:
            for i in range(randint(2, 3)):
                mob_id = choice(["Alkaline Slime", "Slime", "Acid Slime"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "were":
        "A hungry shapeshifters want a piece of you."
        python:
            for i in range(randint(2, 3)):
                mob_id = choice(["Werecat", "Werewolf", "Weregirl"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "harpy":
        "A flock of wild harpies attempts to protects their territory."
        python:
            for i in range(randint(2, 3)):
                mob_id = choice(["Harpy", "Vixen"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "goblin":
        "You find yourself surrounded by a group of goblins."
        python:
            for i in range(3):
                mob_id = choice(["Goblin", "Goblin Archer", "Goblin Warrior", "Goblin Shaman"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "wolf":
        "A pack of wolves picks you for dinner."
        python:
            for i in range(3):
                mob_id = choice(["Wolf", "Black Wolf"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "bear":
        "You disturbed an angry bear."
        python:
            mob_id = choice(["Bear", "Beargirl"])
            mob = build_mob(id=mob_id, level=levels)
            mob.controller = BE_AI(mob)
            enemy_team.add(mob)
    elif mob == "druid":
        "Forest fanatics attempt to sacrifice you in the name of «mother nature» or something like that."
        python:
            for i in range(randint(2, 3)):
                mob_id = choice(["Druid", "Wild Dryad"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "rat":
        "A pack of foul-smelling rats picks you for dinner."
        python:
            for i in range(randint(2, 3)):
                mob_id = "Undead Rat"
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    elif mob == "rat":
        "A pack of foul-smelling rats picks you for dinner."
        python:
            for i in range(3):
                mob_id = choice(["Skeleton", "Skeleton Warrior"])
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    else:
        "You encountered a small group of aggressive giant butterflies."
        python:
            for i in range(randint(2, 3)):
                mob_id = "Black Butterfly"
                mob = build_mob(id=mob_id, level=levels)
                mob.controller = BE_AI(mob)
                enemy_team.add(mob)
    $ place = interactions_pick_background_for_fight("forest")
    $ result = run_default_be(enemy_team, background=place, slaves=True, prebattle=False, death=True)
    if result is True:
        python:
            for member in hero.team:
                member.exp += adjust_exp(member, 150)
        scene expression forest_location
        show screen give_exp_after_battle(hero.team)
        pause 2.5
        hide screen give_exp_after_battle
        jump forest_dark_continue
    else:
        jump game_over
        
label dark_forest_girl_meet:
    $ hero.set_flag("dark_forest_met_girl", value=day)
    $ choices = list(i for i in chars.values() if i.location == "city" and i not in hero.chars and not i.arena_active and i not in gm.get_all_girls()) #TODO: will we even have arena_active eventually?
    $ badtraits = ["Homebody", "Indifferent", "Coward"]
    $ choices = list(i for i in choices if not any(trait in badtraits for trait in i.traits))
    if choices:
        $ character = random.choice(choices)
        $ spr = character.get_vnsprite()
        show expression spr at center with dissolve
        "You found a girl lost in the woods and escorted her to the city."
        $ character.override_portrait("portrait", "happy")
        $ character.show_portrait_overlay("love", "reset")
        $ character.say("She happily kisses you in the chick as a thanks. Maybe you should try to find her in the city later.")
        if character.disposition < 450:
            $ character.disposition += 100
        else:
            $ character.disposition += 50
        hide expression spr with dissolve
        $ character.restore_portrait()
        $ character.hide_portrait_overlay()
        $ global_flags.set_flag("keep_playing_music")
        jump forest_dark_continue