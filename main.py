import random
class Player:
    def __init__(self):
        self.hp = 100
        self.max_hp = 100
        self.stm = 50
        self.max_stm = 50
        self.lvl = 1
        self.xp = 0
        self.xp_to_lvl = 20*self.lvl
        self.base_dmg = 40
        self.equipped_weapon = None
        self.equipped_armor = None
        self.inventory = []

    def add_item(self,item_id):
        new_item = self.item_release(item_id)
        if new_item not in self.inventory :
            self.inventory.append(new_item)
            print(new_item)
        else:
            pass
        

    def item_release(self,item_id):
            item_data = ITEM_DB[item_id]
            new_item = Item(name=item_data["name"],item_type=item_data["item_type"],value=item_data["value"])
            return new_item
    
    def show_inventory(self):
        if self.inventory :
            for index, item in enumerate(self.inventory,1):
                print(f"{index}. {item.name} (+{item.value} {item.item_type})")

    def equip_item(self,item):
        if item.item_type =="damage":
            if self.equipped_weapon :
                self.unequip_item("weapon")
                print(f"Giyilen eşya çıkarıldı.")
            self.equipped_weapon = item
            self.base_dmg += item.value
            self.inventory.remove(item)
            print(f"{item.name} kuşandın! Hasarın {item.value} arttı.")
        elif item.item_type =="armor":
            if self.equipped_armor :
                self.unequip_item("armor")
                print(f"Giyilen eşya çıkarıldı.")
            self.equipped_armor = item
            self.max_hp += item.value
            self.inventory.remove(item)
            print(f"{item.name} kuşandın! Canın {item.value} arttı.")
        else:
            print("Bu eşya kullanılamaz.")

    def  unequip_item(self,slot_type):
        if slot_type == "damage" and self.equipped_weapon:
            item = self.equipped_weapon
            self.base_dmg -= item.value
            self.inventory.append(item)
            self.equipped_weapon = None

        elif slot_type == "armor" and self.equipped_armor:
            item = self.equipped_armor
            self.max_hp -= item.value
            
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            self.inventory.append(item)
            self.equipped_armor = None
            print(f"{item.name} çıkartıldı ve çantaya konuldu.")
        else:
            print("Çıkartılacak bir eşya yok.")

    def take_dmg(self, enemy_dmg):
        self.hp -=  enemy_dmg
        if self.hp < 0:
            self.hp = 0
    
    def heal(self,heal_potion=None):
        self.hp += 15
        if self.hp > self.max_hp:
            self.hp = self.max_hp
    
    def gain_xp(self, is_enemy_killed,enemy_lvl):
        if is_enemy_killed:
            self.xp += int(enemy_lvl*(1.5))
            print(f"{int(enemy_lvl*(1.5))} XP kazandın.")
        
        while self.xp >= self.xp_to_lvl:
            self.xp -= self.xp_to_lvl
            self.lvl += 1
            print(F"Tebrikler! Level atladın. Yeni seviye: {player.lvl}")
            self.max_hp = int(self.max_hp * 1.09)
            self.base_dmg = int(self.base_dmg * 1.1)
    

class Enemy:
    def __init__(self,player_max_hp,player_base_dmg,player_lvl):
        self.name = random.choice(["Yandan Yemiş Ork","Japon Askeri","Akasya Durağı Obayana","Gerçek Joker","Sessiz Osuruk"])
        self.hp = int(player_max_hp * player_lvl * 0.9)
        self.base_dmg = int((player_base_dmg/5) * player_lvl * 0.92)
        self.lvl = random.choice([ lvl for lvl in range(player_lvl-1,player_lvl +3) if lvl >=1])



    def take_dmg(self, enemy_dmg):
        self.hp -=  enemy_dmg
        if self.hp < 0:
            self.hp = 0

class Item:
    def __init__(self,name,item_type,value):
        self.name = name
        self.item_type = item_type
        self.value = value    

ITEM_DB = {
    "yandan_yemis_orkun_annesinin_ordugu_yelek": {"name":"Yandan Yemiş Ork'un Annesinin Ördüğü Yelek","item_type":"armor","value":10},
    "xs_beden_zirh": {"name":"XS Beden Zırh","item_type":"armor","value":15},
    "fena_guzel_zırh": {"name":"Fena Güzel Zırh","item_type":"armor","value":20},
    "en_iyi_zirh": {"name":"En İyi Zırh (gerçekten)","item_type":"armor","value":25},
    "kucuk_iksir": {"name": "Küçük İksir", "item_type": "heal", "value": 15},
    "kucuk_tahta_kılıc": {"name": "Küçük Tahta Kılıç", "item_type": "damage", "value": 3},
    "kucuk_kılıc": {"name": "Küçük Kılıç", "item_type": "damage", "value": 5},
    "orta_boy_kılıc": {"name": "Orta Boy Kılıç", "item_type": "damage", "value": 9},
    "buyuk_kılıc": {"name": "Buyuk Kılıç", "item_type": "damage", "value": 12},
    "en_buyuk_kılıc": {"name": "En Büyük Kılıç", "item_type": "damage", "value": 15},
    "en_buyuk_kılıctan_biraz_buyuk_kılıc": {"name": "En Büyük Kılıç'tan Biraz Büyük Kılıç", "item_type": "damage", "value": 18}
}

player = Player()

def main_menu(player):
    while player.hp > 0:    
        choice = input("1- Mecaraya atıl. 2-Çantana göz at. 3-Durumunu gör.")
        if choice == '1':
            random_events(player)
        elif choice == '2':
            player.show_inventory()
            choice = input("1- Eşya değiştir/kullan 2- Ana menüye geri dön")
            if choice == '1':
                item_index = input("Kullanmak istediğin eşyanın numarasını yaz.")
                if item_index.isdigit():
                    idx = int(item_index)-1
                    if 0 <= idx <len(player.inventory):
                        picked_item = player.inventory[idx]
                        if picked_item.item_type == "heal":
                            player.heal()
                            print(f"{picked_item.name} kullandın. Canın yenilendi. Eşya çantandan silindi.")
                            player.inventory.remove(picked_item)
                        else:
                            player.equip_item(picked_item)

                else:
                    print("Çantada böyle bir numara yok.")
            else:
                print("Ana menüye dönüldü")
                pass
        elif choice == '3':
            weapon_name = player.equipped_weapon.name if player.equipped_weapon else "Yok"
            armor_name = player.equipped_armor.name if player.equipped_armor else "Yok"
            print(f"Karakterin Durumu:\nMaksimum Can:{player.max_hp}\nGüncel Can:{player.hp}\nHasar:{player.base_dmg}\nKullanılan Silah:{weapon_name}\nKullanılan Zırh:{armor_name}\nLevel:{player.lvl}\nXP:{player.xp}\nYeni Level'e kalan XP:{player.xp_to_lvl-player.xp}")        

    print(f"Öldün haha.")
    #death_menu()



def random_events(player):
    events=["fight_enemy","find_box","traps","hp_potion"]
    probabilities = [35,30,10,25]

    event = random.choices(events, weights=probabilities)[0]
    
    if event == "fight_enemy":
        print(f"Karşına bir yaratık çıktı ama karanlıkta ne olduğunu anlayamıyorsun")
        choice = input("1-Savaş(Belki ölebilirsin bile), 2- Kaç(Can kaybedersin)")
        if choice == '1':
            enemy= Enemy(player.max_hp,player.base_dmg,player.lvl)
            print(f"Savaşmayı seçtin. Yaratık yaklaştı o bir {enemy.name}. Eyvah!")
            fight_enemy(player,enemy)
        else:
            print("Kaçmayı seçtin... Yazık.")
            player.hp = int(player.hp * 0.9)
    
    elif event == "find_box":
        print(f"Bir kutu buldun açacak mısın? İçinden eşya veya canavar çıkabilir.")
        choice = input("1-Aç, 2- Bırakıp git")
        if choice == '1':
            events=["box","enemy","boss"]
            probabilities = [50,40,10]
            event = random.choices(events,weights=probabilities)[0]
            if event == "box":
                print("Kutudan item çıktı >:/")
                item_id = random.choice(list(ITEM_DB.keys()))
                item_data = ITEM_DB[item_id]
                new_item = Item(name=item_data["name"],item_type=item_data["item_type"],value=item_data["value"])
                if new_item.item_type =="armor":
                    ozellik = "maksimum can"
                    print(f"{new_item.name}. Sağladığı özellik: +{new_item.value} {ozellik}")

                elif new_item.item_type =="damage":
                    ozellik = "saldırı gücü"
                    print(f"{new_item.name}. Sağladığı özellik: +{new_item.value} {ozellik}")
                
                else:
                    print(f"Küçük iksir buldun +15 can sağlar. Çantana eklendi")
                player.add_item(new_item)
            elif event == "enemy":
                enemy= Enemy(player.max_hp,player.base_dmg,player.lvl)
                print(f"HAHAHA karşına {enemy.name} çıktı. ")
                fight_enemy(player,enemy)
            else:
                enemy= Enemy(player.max_hp*1.5,player.base_dmg*1.5,player.lvl)
                print(f"Bu sefer kesin öldün. Kutudan {enemy.name} patronunu çıkarttın haha.")
                fight_enemy(player,enemy)
    
    elif event == "traps":
        choice = input("1-Yavaş geç - Düşman yetişebilir, 2-Hızlı geç -can kaybet")
        if choice == '1':
            events=["enemy","safe"]
            probabilities = [40,60]
            event = random.choices(events,weights=probabilities)[0]
            if event == "safe":
                print("güvenle geçtin")
            else:
                enemy= Enemy(player.max_hp,player.base_dmg,player.lvl)
                fight_enemy(player,enemy)
        elif choice == '2':
            player.hp = int(player.hp * 0.9)

    else:
        print("Bir can iksiri buldun. Sana +15 can sağlayacak")
        choice = input("1-İç , 2-Çantaya at")
        if choice == '1':
            player.heal()
            print(f"İksiri içtin canın +15 arttı. (Güncel canın:{player.hp})")
        
        else:
            item_data = ITEM_DB["kucuk_iksir"]
            new_item = Item(name=item_data["name"],item_type=item_data["item_type"],value=item_data["value"])
            player.add_item(new_item)
            print(f"İksir çantaya eklendi.")

            
def fight_enemy (player: Player, enemy: Enemy):
    while enemy.hp != 0 and player.hp != 0 :
        choice = input("1-Saldır, 2-İyileş")
        if choice == '1':
            enemy.take_dmg(player.base_dmg)
            if enemy.hp == 0:
                is_enemy_killed = True
                player.gain_xp(is_enemy_killed,enemy.lvl)
                break
            player.take_dmg(enemy.base_dmg) 
            print(f"Canın:{player.hp}, {enemy.name} canı:{enemy.hp}")
            if player.hp == 0:
                print("oyun bitti öldün. İlerlemen imkansız zaten :D")
                
                break
        else :
            potion_to_use = None
            for item in player.inventory:
                if item.item_type == "heal":
                    potion_to_use = item
                    break
            if potion_to_use:
                player.heal()
                player.inventory.remove(potion_to_use)
                print("Bir can iksiri kullandın ve canın yenilendi. Eğer başka can iksirin yoksa çantanda iksir ararken yaratık sana saldıracak. Dikkatli ol!")
            else:
                print("Çantanda hiç can iksiri yok! Hamleni boşa harcadın.")
                player.take_dmg(enemy.base_dmg)
            

if __name__ == "__main__":
    main_menu(player)