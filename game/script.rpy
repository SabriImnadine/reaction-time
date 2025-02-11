define p = Character('Professor')

image character_normal = "images/character_normal.png"
image character_happy = "images/character_happy.png" 
image character_confidence = "images/character_confidence.png"

label start:
    scene school with dissolve
    show character_normal at left
    p "Welcome, test subject. You have been chosen to take part in a special challenge."
    
    show character_happy at left
    p "This is not just any test .."
    
    show character_confidence at left
    p "It's one of precision, speed, and reflexes."
    
    show character_normal at left
    p "In this game, your ability to react quickly will determine your success."
    p "The goal is simple: a button will light up randomly. Your task is to press the corresponding button before the light fades."
    
    show character_happy at left
    p "The faster you react, the higher your score will be. But beware – each missed button will cost you precious time."
    
    show character_confidence at left
    p "Your reflexes will be put to the test, and only the quickest will succeed."
    
    p "Are you ready to begin? Prove your skills and see if you have what it takes!"
    
    menu:
        "Yes, let's go!":
            play music "song.mp3" loop
            $ setup_reflex_game()
            scene black with fade
            call screen reflex_minigame
        "No, not right now":
            "Maybe another time. Come back when you're ready."
            return

init python:
    import random

    def activate_button():
        global random_button_indexes
        global current_button_index
        if current_button_index < buttons - 1:
            current_button_index += 1
        else:
            current_button_index = 0
            random_button_indexes = random.sample(range(6), k = 6)
        random_button_index = random_button_indexes[current_button_index]
        button_states[random_button_index] = "lit"

    def reaction_bpress(btn):
        global score

        if button_states[btn] == "lit":
            score += 1
            button_states[btn] = "idle"

    def setup_reflex_game():
        global random_button_indexes

        for i in range(buttons):
            button_states.append("idle")
        random_button_indexes = random.sample(range(buttons), k = buttons)

    def reset_reflex_game():
        global play_time
        global score
        global initial_countdown

        initial_countdown = 3
        play_time = 15
        score = 0
        for i in range(buttons):
            button_states[i] = "idle"

        renpy.show_screen("countdown_timer")


screen countdown_timer:
    frame:
        background "#00000080"
        xfill True
        yfill True
        text "[initial_countdown]" size 120 text_align 0.5 align(0.5, 0.5)
    timer 1.0 action If(initial_countdown > 1, SetVariable("initial_countdown", initial_countdown - 1), Hide("countdown_timer")) repeat If(initial_countdown > 1, True, False)

screen reflex_minigame:
    on "show" action Show("countdown_timer")
    add "background.png"

    grid int(buttons/2) 2:
        xspacing 100
        yspacing 20
        anchor(0.5, 0.5)
        align(0.5, 0.85)
        for i in range(buttons):
            imagebutton idle "button-%s.png" % button_states[i] focus_mask True action Function(reaction_bpress, btn = i)

    text "[score]" size 78 align(0.79, 0.145) text_align 0.5 anchor(0.5, 0.5)
    text "[play_time]" size 78 color "#FFFFFF" align(0.79, 0.355) text_align 0.5 anchor(0.5, 0.5)

    if renpy.get_screen("countdown_timer") == None:
        if "lit" not in button_states:
            timer 0.1 action Function(activate_button) repeat False
        timer 1.0 action If(play_time > 1, SetVariable("play_time", play_time - 1), Show("reflex_minigame_over")) repeat If(play_time > 1, True, False)

screen reflex_minigame_over:
    modal True
    frame:
        background "#00000080"
        xfill True
        yfill True
        frame:
            background "game-over-bg.png"
            xysize(1072, 698)
            align(0.5, 0.5)
            text "Your score: [score]" size 50 text_align 0.5 align(0.5, 0.4)
            imagebutton idle "play-again-button.png" align(0.2, 0.8) action [Hide("reflex_minigame_over"), Function(reset_reflex_game)]
            imagebutton idle "quit-button.png" align(0.85, 0.8) action Quit()  

default button_states = []
default buttons = 6
default random_button_indexes = []
default current_button_index = 0
default score = 0
default play_time = 20
default initial_countdown = 5

