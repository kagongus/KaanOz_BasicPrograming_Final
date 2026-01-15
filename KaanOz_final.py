import random
import time


inventory = {
    "potion": 3,
    "items": []
}
dangeon_clear =False

gardain_note = "739"

lever_sira = ["middle", "left", "right"]
nlever_imput = []

old_man_talk = False
old_man =False

boss =  False
visit_check = set()

def roll_dice(): 

    return random.randint(1, 20)

class Hero:
    def __init__(self, name = "knight", hp = 130 , attack_power = 12, weapon=None, shield=None):
        self.name = name

        self.max_hp = hp

        self.hp =  hp

        self.attack_power =attack_power

        self.weapon =weapon

        self.shield = shield

        self.level = 1

        self.stun_cooldown = 0

        self.fireball_cooldown = 0

        self.exp = 0

        self.magicbonus = 0


    def attack(self, target):
        weapondamage = self.weapon.damage 

        damage = self.attack_power + weapondamage
        target.take_damage(damage)

    
        print(f"{self.name} attacked for \033[31m{damage}\033[0m damage.")
        print(f"{target.name} HP is \033[32m{target.hp}\033[0m")

    def critattack(self, target):
        weapondamage = self.weapon.damage

        damage = (self.attack_power + weapondamage) * 2
        target.take_damage(damage)

        print(f"{self.name} CRIT \033[33m{damage}\033[0m damage!")
        print(f"{target.name} HP is  \033[32m{target.hp}\033[0m")


    def potion(self, inventory): #heal system
        if inventory["potion"] <= 0:
            print("No potions left!")
            return
        
        if self.hp == self.max_hp:
            print("HP already full.")
            return
        
        healamount = roll_dice() + self.level 
        self.hp += healamount

        inventory["potion"] -= 1

       

        if self.hp > self.max_hp:
            self.hp = self.max_hp

        print(f"{self.name} used a potion and healed {healamount} HP.")
        print(f"{self.name} HP is  {self.hp}")


    def take_damage(self, damage):
        shielddefense = self.shield.defense 
        damage -= shielddefense
        self.hp -= damage
        if damage < 0:
            damage = 0
        
        if self.hp < 0:
            self.hp = 0

        if shielddefense > 0:
            print(f"shield blocked \033[32m{shielddefense}\033[0m damage.")

        print(f"{self.name} take \033[31m{damage}\033[0m damage.")

    def stun_spell(self, target): #lightning spell

        if self.stun_cooldown > 0:

            print(f"Magic is on cooldown! {self.stun_cooldown} turn left.")
            return False
        
        damage = self.magicbonus
        target.hp -= damage

        if target.hp < 0:
            target.hp = 0

        target.stunned = 3

        print(f"{target.name} is \033[36mSTUNNED\033[0m!")

        self.stun_cooldown = 6

        print(f"{self.name} casts Lightning! \033[33m{damage}\033[0m damage!")
        print(f"{target.name} HP is  \033[32m{target.hp}\033[0m")
        return True
    

    
    def magic(self, target):
        if self.fireball_cooldown > 0:
            print(f"Magic is on cooldown! {self.fireball_cooldown} turn left.")
            return False

        magicdamage = roll_dice() + 5 + self.magicbonus
        
        target.hp -= magicdamage
        if target.hp < 0:
            target.hp = 0

        self.fireball_cooldown = 4
        print(f"{self.name} cast a spell \033[35m{magicdamage}\033[0m magic damage")
        print(f"{target.name} HP is \033[32m{target.hp}\033[0m")
        return True


    def gain_exp(self, amount):  #level system
        self.exp += amount
        print(f"You gained {amount} EXP.")
        if self.exp >= 120:

            self.exp -= 120

            self.level += 1

            self.max_hp += 5

            self.attack_power += 2

            self.magicbonus += 1

            self.hp = self.max_hp

            print("\n LEVEL UP!")
            print(f"Level: {self.level}")
            print("Max HP +5")
            print("Attack +2")
            print("Magic Power +1")


class Monster:
    def __init__(self, name="goblin", hp=50, attack_power=5):

        self.name = name

        self.hp = hp

        self.attack_power = attack_power

        self.stunned = 0

    def attack(self, hero):

        if self.stunned > 0:

            print(f"{self.name} is stunned cannot attack")

            self.stunned -= 1
            return
        damage = self.attack_power

        print(f"{self.name} attack for \033[31m{damage}\033[0m damage.")


        hero.take_damage(damage)

        print(f"{hero.name} HP is  \033[32m{hero.hp}\033[0m")



    def critattack(self, hero):

        damage = self.attack_power * 2
        print(f"{self.name} CRIT \033[33m{damage}\033[0m damage")

        hero.take_damage(damage)
        print(f"{hero.name} HP is  \033[32m{hero.hp}\033[0m")

    def take_damage(self, damage):
        self.hp -= damage

        if self.hp < 0:
            self.hp = 0

class weapon:
    def __init__(self, name, damage):

        self.name = name
        self.damage = damage

    


class shield:
    def __init__(self, name, defense,):
        self.name = name

        self.defense = defense


ironsword = weapon("Iron Sword", 5, )
ironshield = shield("Iron Shield", 3, )
fist = weapon("fist",1)


currentlocation = "prison"
def slow_print(*message, delay):
    for word in message:
        for char in word:
            print(char, end="")
            time.sleep(delay)
        print(" ", end="")
    print("")

rooms = {
    "prison": {
        "east": "corridor",
        "item": []
    },
    "corridor": {
        "east": "workshop",
        "west": "prison",
        "item": ["gardian"]
    },
    "garden": {
        "north": "workshop",
        "locked": True,
    },
    "workshop": {
        "west": "corridor",
        "east": "dungeon",
        "south": "garden",
        "item": ["gardian"],
        "npc": "old_man"
    },
    "dungeon": {
        "west": "workshop",
        "npc": "necromancer"
    }
}

name = input("Enter hero name: ")
hero = Hero(name=name, hp=100, attack_power=10, weapon=ironsword, shield=ironshield)

slow_print("""[NARRATOR]
When you open your eyes, you find yourself awakened on a cold stone floor.
The walls are damp, the air heavy and dark.

As your vision clears, something glistens in the corner of the cell.
A rusty sword lies next to a worn-out shield.

You crawl towards them and grasp the sword's hilt.
You strap the shield to your arm.

You are no longer defenseless.
""", delay=0.0) 

valid_commands = ["look", "go", "inventory", "talk", "pull","stats","help"]



while True:
    slow_print("You are in the", currentlocation, "what do you do?", delay=0.02)

    action = input("> ")

    actionList = action.split(" ", 1) #start


    if actionList[0] not in valid_commands:

        slow_print("i don't understand", delay=0.02)

    elif actionList[0] == "look":

        npc = rooms[currentlocation].get("npc",)

        if npc:
            slow_print("You see:",npc, delay=0.02)

        else:

            slow_print("You see nothing", delay=0.02)

    elif actionList[0] == "stats":

        slow_print(f"HP: {hero.hp}/{hero.max_hp}",delay=0.02)
        slow_print(f"Level: {hero.level} (EXP {hero.exp}/120)",   delay=0.02)
        slow_print(f"AP: {hero.attack_power}", delay=0.02)
        slow_print(f"MAGIC BONUS: {hero.magicbonus}",  delay=0.02)
    elif actionList[0] == "help":
        slow_print("Available commands:", delay=0.02)
        slow_print("look  ", delay=0.02)
        slow_print("go + direction", delay=0.02)
        slow_print("talk       ", delay=0.02)
        slow_print("inventory ", delay=0.02)
        slow_print("stats   ", delay=0.02)
        slow_print("pull", delay=0.02)
        slow_print("help", delay=0.02)



    elif actionList[0] == "inventory":
    
        if inventory["items"]:

            slow_print("Items:", ", ".join(inventory["items"]), delay=0.001)
            slow_print(f"Potions: {inventory['potion']}", delay=0.001)
        else:

            slow_print("Items: none", delay=0.001)
            slow_print(f"Potions: {inventory['potion']}",delay=0.001)

    elif actionList[0] == "go":
        if len(actionList) >1:

            direction = actionList[1]

            if direction in rooms[currentlocation]:
                target = rooms[currentlocation][direction]

                if "locked" in rooms[target] and rooms[target]["locked"]:
                    slow_print("The door is locked.", delay=0.02)

                    if f"note = {gardain_note}" in inventory["items"]:
                        slow_print("There is a keypad on the door.",delay=0.02)
                    kod = input("Enter the code: ")

                    if kod == gardain_note:
                        slow_print("The door unlocks.", delay=0.02)
                        rooms[target]["locked"] = False
                        currentlocation = target
                        slow_print("You moved to", currentlocation, delay=0.02)

                else:
                    currentlocation = rooms[currentlocation][direction]
                    slow_print("You moved to", currentlocation, delay=0.02)

            else:
                slow_print("There are no doors in that direction.",delay=0.02)

        else:
            slow_print("Go where?", delay=0.02)

    elif actionList[0] == "talk":
        npc = rooms[currentlocation].get("npc")

        if not npc:
            slow_print("There is no one to talk to.", delay=0.02)
            continue

        if npc == "necromancer":
            if "note = 739" in inventory["items"]:
                slow_print("Necromancer: i gave you what you need.",delay=0.02)
                continue
            slow_print("He whispers: 739", delay=0.02)

            inventory["items"].append(f"note = {gardain_note}")
            slow_print("You get a note", delay=0.02)
            continue
    

        if old_man:
            slow_print("Old Man: I have nothing ", delay=0.02)
            continue

        elif old_man_talk:
            slow_print("Old Man: I have already taught you all I can. ", delay=0.02)

        else:
            slow_print("Old Man: Thank you for saving.", delay=0.02)
            slow_print("Old Man: Let me share my knowledge. ",delay=0.02)
            slow_print("Old man: Will you fight me? (yes/no)", delay=0.02)
            choice = input("> ")
            if choice != "yes":
                slow_print("Old Man: Then leave.", delay=0.02)
                continue
            slow_print("The duel begins.",delay=0.02)
        monster = Monster("Old Man",120,120)
        turn = 1
        



        while hero.hp > 0: # free xp farm :D
            print("\n--- OLD MAN FIGHT ---")
            print(f" {hero.name} HP: {hero.hp} {monster.name} HP: {monster.hp} ")
            print("1 - Attack")
            input("> ")
            slow_print("Old man dodged your attack",delay=0.02) 
            monster.attack(hero)
            if hero.hp <= 0:
                break
        hero.gain_exp(120)
        hero.gain_exp(120)
        hero.gain_exp(120)
        slow_print("Old Man: Wants to train you for a boss fight.", delay=0.02)
        slow_print("Old Man: Now you understand real combat.", delay=0.02)
        slow_print("You feel stronger than before.", delay=0.02)  
        slow_print("You can check your stats.", delay=0.02)
        old_man =True
                
            
    elif actionList[0] == "pull": # lever code
        if currentlocation != "garden":
            slow_print("There is nothing to pull here.", delay=0.02)

        else:
            nlever_imput.clear()
            slow_print("You see three levers", delay=0.02)

            for a in range(3):
                direction = input(f"Which lever {a+1}? (left / middle / right): ")

                while direction not in ["left", "middle", "right"]:
                    slow_print("That lever does not exist.", delay=0.02)
                    direction = input(f"Which lever {a+1}? (left / middle / right): ")
                nlever_imput.append(direction)
                slow_print("You pull the", direction, "lever.", delay=0.02)

            if len(nlever_imput) <  3:
                slow_print(f"gears moving ({len(nlever_imput)}/3)", delay=0.02)

            elif len(nlever_imput) ==3:

                if nlever_imput == lever_sira:
                    slow_print("gears turning behind the walls.", delay=0.02)
                    slow_print("A distant door unlocks...", delay=0.02)
                    rooms["garden"]["locked"] = False
                    slow_print("You can escape.", delay=0.02)
                    boss =True

                else:
                    slow_print("Wrong combination", delay=0.02)
                nlever_imput.clear()
     
    if currentlocation == "corridor" and currentlocation not in visit_check:  #description
        slow_print("you enter a narrow corridor.", delay=0.02)
        slow_print("Torches flicker on the walls, making strange shadows.", delay=0.02)
        slow_print("The place smells odd, like metal or rust.", delay=0.02)
        slow_print("You hear noises, but cannot tell where they come from.", delay=0.02)
        visit_check.add(currentlocation)

    if currentlocation == "workshop" and currentlocation not in visit_check:
        slow_print("You step into a ruined workshop.", delay=0.02)
        slow_print("Broken tools lie scattered across the floor.", delay=0.02)
        slow_print("A campfire flickers weakly in the corner.", delay=0.02)
        visit_check.add(currentlocation)



    if currentlocation == "garden" and not boss and currentlocation not in visit_check:
        slow_print("You step into the garden.", delay=0.02)
        slow_print("Moonlight reveals a massive iron gate at the far end.", delay=0.02)
        slow_print("It feels like this is not the end yet...", delay=0.02)
        slow_print("You see 3 lever you could try to pull", delay=0.02)
        visit_check.add(currentlocation)

    if currentlocation == "dungeon" and dangeon_clear and currentlocation not in visit_check:
        slow_print("The dungeon is silent.", delay=0.02)
        slow_print("You see a necromancer you could try to talk.", delay=0.02)

    if currentlocation == "dungeon" and not dangeon_clear:    #dungeon chek
        dangeon_clear = True
        slow_print("You step into the dungeon.", delay=0.02)
        slow_print("You feel bad things.", delay=0.02)
        slow_print("You hear fighting sounds", delay=0.02)
        slow_print("Enemies watching you from the deep", delay=0.02)



        dangeon_enemy = [
            Monster("dark goblin", 80, 10),
            Monster("skeleton", 50, 12),
            Monster("zombie", 70, 8),
            Monster("orc", 100, 15),
            Monster("Mini Boss:DARK KNIGHT", 200, 30)
            ]
        for monster in dangeon_enemy:  #dangeon fight
            turn = 1
            slow_print(f"A {monster.name} attak", delay=0.0)

            while hero.hp > 0 and monster.hp > 0:
                print(f"\n--- TURN {turn} ---")
                print(f"{hero.name} HP: \033[32m{hero.hp}\033[0m {monster.name} HP: \033[32m{monster.hp}\033[0m")
                print("1 - Attack")
                print(f"2 - Heal (Potions: {inventory['potion']})")
                
                if hero.level >= 4:
                    if hero.fireball_cooldown > 0:
                        print(f"3 - Fire Ball (Cooldown: {hero.fireball_cooldown})")
                    else:
                        print("3 - Fire Ball (Ready)")
                if hero.level >= 7:
                    if hero.stun_cooldown > 0:
                        print(f"4 - Lightning (Cooldown: {hero.stun_cooldown})")
                    else:
                        print("4 - Lightning (Ready)")

                choice = input("> ")
                roll = roll_dice()

                if choice == "1":

                    if roll == 20:
                        hero.critattack(monster)

                    elif roll >= 5:
                        hero.attack(monster)

                    else:
                        print("Hero missed")

                elif choice == "2":
                    hero.potion(inventory)
                    continue

                elif choice == "3" and hero.level >= 4:
                    if not hero.magic(monster):
                        continue
                elif choice == "4" and hero.level >= 7:
                    if not hero.stun_spell(monster):
                        continue
                else:
                    slow_print("Invalid action", delay=0.02)
                    continue

                if monster.hp <= 0:
                    slow_print(f"The {monster.name} is defeated", delay=0.001)

                    hero.gain_exp(120)
                    break

                monster_roll = roll_dice()

                if monster_roll == 20:
                    monster.critattack(hero)

                elif monster_roll >= 1:
                    monster.attack(hero)

                else:
                    print(f"{monster.name} missed")

                if hero.hp <= 0:
                    slow_print("You have been slain in dungeon", delay=0.02)
                    slow_print("GAME OVER!", delay=0.2)
                    exit()

                if hero.fireball_cooldown > 0:
                    hero.fireball_cooldown-= 1

                if hero.stun_cooldown > 0:
                    hero.stun_cooldown -= 1

                turn += 1
        slow_print("The dungeon is silent.", delay=0.02)
        slow_print("You see a necromancer you could try to talk.", delay=0.02)

            
     # final boss     
    if boss:  

        turn = 1
        time.sleep(1)

        slow_print("As you move away, the ground shakes", delay=0.02)
        slow_print("shadow drops in front of you", delay=0.02)
        slow_print("..........................", delay=0.02)
        slow_print("BOSS: you can't pass here.", delay=0.02)


        monster = Monster("Shadow Knight", 300, 18)
        boss = False

        while hero.hp > 0 and monster.hp > 0:
            print(f"\n--- TURN {turn} ---")

            print(f"{hero.name} HP: \033[32m{hero.hp}\033[32m {monster.name} HP: \033[32m{monster.hp}\033[0m")
            print("1 - Attack")
            print(f"2 - Heal (Potions: {inventory['potion']})")

            if hero.level >= 2:

                if hero.fireball_cooldown > 0:
                    print(f"3 - Fire Ball (Cooldown: {hero.fireball_cooldown})")

                else:
                    print("3 - Fire Ball (Ready)")
            if hero.level >= 4:

                if hero.stun_cooldown > 0:
                    print(f"4 - Lightning (Cooldown: {hero.stun_cooldown})")

                else:
                    print("4 - Lightning (Ready)")
            print("5 - Run")

            choice = input("> ")
            roll = roll_dice()

            if choice == "1":

                if roll == 20:
                    hero.critattack(monster)

                elif roll >= 5:
                    hero.attack(monster)

                else:
                    print("Hero missed")

            elif choice == "2":

                hero.potion(inventory)
                continue

            elif choice == "3" and hero.level >= 4:

                if not hero.magic(monster):
                    continue

            elif choice == "4" and hero.level >= 7:
                if not hero.stun_spell(monster):
                    continue

            elif choice == "5":
                slow_print("You try to run...", delay=0.01)


                if roll_dice() >= 11:
                    slow_print("You break free and sprint into the darkness.", delay=0.01)
                    slow_print("The Shadow Knight roar fades behind you.", delay=0.01)
                    time.sleep(1)
                    slow_print("........................", delay=0.2)
                    slow_print("You survive...", delay=0.01)
                    slow_print("\nENDING 1 ESCAPE", delay=0.2)  # 1 ending 
                    exit()

                else:
                    slow_print("You stumble", delay=0.02)
                    slow_print(f"The {monster.name} blocks your path", delay=0.02)
                    slow_print("You failed to escape", delay=0.02)
                    monster.attack(hero)

                    if hero.hp <= 0:
                        slow_print("You fall as you try to flee", delay=0.02)
                        slow_print("GAME OVER!", delay=0.2)
                        exit()

            else:
                slow_print("Invalid action", delay=0.02)
                continue

            if monster.hp <= 0:
                slow_print(f"The {monster.name} is defeated", delay=0.02)
                slow_print(f"The {monster.name} falls to one knee...", delay=0.02)
                slow_print("Cracks of light burst from its armor.", delay=0.02)
                slow_print("\nENDING 2 WIN", delay=0.2)   # 2 endin
                slow_print("\033[32mYOU WIN!\033[32m", delay=0.2)
                exit()
                break

            monster_roll = roll_dice()
            if monster_roll == 20:
                monster.critattack(hero)

            elif monster_roll >= 1:
                monster.attack(hero)

            else:
                print(f"{monster.name} missed!")


            if hero.hp <= 0:
                slow_print(f"{monster.name}: PUHAHHAHAHAHHAHH", delay=0.02)
                slow_print("GAME OVER!", delay=0.2)  # dead ending
                exit()

            if hero.fireball_cooldown > 0:
                hero.fireball_cooldown-= 1




            if hero.stun_cooldown > 0:
                hero.stun_cooldown -= 1


            turn += 1

     # goblin fights
    if "gardian" in rooms[currentlocation].get("item", []  ):
        slow_print("Goblin attacks you!", delay=0.0)


        monster = Monster("guardian goblin", 30, 8)
        turn = 1

        while hero.hp > 0 and monster.hp > 0:
            print(f"\n--- TURN {turn} ---  ")
            print(f"{hero.name} HP: \033[32m{hero.hp}\033[0m {monster.name} HP: \033[32m{monster.hp}\033[0m " )
            print("1 - Attack")
            print(f"2 - Heal (Potions: {inventory['potion']} ) ")


            if hero.level >= 4:
                if hero.fireball_cooldown > 0:
                    print(f"3 - Fire Ball (Cooldown: {hero.fireball_cooldown}  ")

                else:
                    print("3 - Fire Ball (Ready)")

            if hero.level >= 7:
                if hero.stun_cooldown > 0: 
                    print(f"4 - Lightning (Cooldown: {hero.stun_cooldown} ) ")

                else:
                    print("4 - Lightning (Ready) ")

            choice = input("> ")
            roll = roll_dice()

            if choice == "1":
                if roll == 20:
                    hero.critattack(monster)

                elif roll >= 5:
                    hero.attack(monster)

                else:
                    print("Hero missed! ")

            elif choice == "2":
                hero.potion(inventory)
                continue

            elif choice == "3" and hero.level >= 4:
                if not hero.magic(monster):
                    continue
                
            elif choice == "4" and hero.level >= 7:
                if not hero.stun_spell(monster):
                    continue

            else:
                slow_print("Invalid action!", delay=0.02)
                continue

            if monster.hp <= 0:
                slow_print("The guardian is defeated!", delay=0.0)
                rooms[currentlocation]["item"].remove("gardian")
                hero.gain_exp(80)

                if currentlocation == "workshop":
                    slow_print("You notice an old man sitting in the shadows.", delay=0.02) # old man dialog
                    slow_print("Perhaps you could try talking to him.", delay=0.02)
                break
                    



            monster_roll = roll_dice()
            if monster_roll == 20:

                monster.critattack(hero)
            elif monster_roll >= 1:
                monster.attack(hero)

            else:
                print(f"{monster.name} missed!")


            if hero.hp <= 0:
                slow_print("You have been slain...", delay=0.2)
                slow_print("GAME OVER!", delay=0.2)
                exit()

            if hero.fireball_cooldown > 0:
                hero.fireball_cooldown-= 1

            if hero.stun_cooldown > 0:
                hero.stun_cooldown -= 1


            turn += 1
