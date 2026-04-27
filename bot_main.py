import aiohttp
import asyncio
from state_manage import get_user,set_user,delete_user,_memory
from main import Player, Enemy, ITEM_DB
import random
from collections import Counter

TOKEN = "8761395880:AAFoMqQV1ob7CN7TYT27GHvt9b7GgBqAJhI"
URL = f"https://api.telegram.org/bot{TOKEN}"


async def top_main_menu_handler(session,chat_id,text,user_data):
    
    if text == '1':
        user_data["state"] = "MAIN_MENU"
        await send_message(session,chat_id,f"\n1- Maceraya atıl\n2- Çantana göz at\n3- Durumunu gör")
    if text == '2':
        user_data["state"] = "TOP_MAIN_MENU"
        await send_message(session,chat_id,f"Burası daha hazır değil. Daha sonra.\nAna menüdesin\n1-Oyuna başla\n2-Liderler tablosunu gör")

async def main_menu_handler(session,chat_id,text,user_data,current_player):
    if text == "1":
        events = ["fight","find_box","hp_potion","traps"]
        prob_event = [0,65,35,0]
        event = random.choices(events,weights=prob_event)[0]
        if event == "fight":
            user_data["state"] = "CHOOSE_FIGHT"
            user_data["enemy"]= Enemy(current_player.max_hp,current_player.base_dmg,current_player.lvl)
            current_enemy = user_data.get("enemy")
            await send_message(session,chat_id,f"{current_enemy.name} ile karşılaştın.\n1- Savaşa hazırlan!\n2- Kaç")
        elif event == "find_box":
            user_data["state"] = "FIND_BOX"
            await send_message(session,chat_id,"Zindanın derinliklerinde ilerliyorsun...\nKutu buldun!\n1- Aç\n2- Açmadan devam et.")
                                                
        elif event == "hp_potion":
            user_data["state"] = "HP_POTION"
            await send_message(session,chat_id,"Can iksiri buldun!\n1- Kullan\n2- Çantana at")

        elif event == "traps":
            user_data["state"] = "TRAPS"
            await send_message(session,chat_id,"Tuzağa yakalandın!\n1- Hızlıca geç\n2- Dikkatli geç.")

    elif text == '2':
        if current_player.inventory :
            ans_text = "Zırh ve Silahlar:"
            potion_counter = 0
            item_idx = 1
            ans_list = set()
            for index, item in enumerate((current_player.inventory),1):
                if item.name in ans_list or (item.name == "Küçük İksir"):
                    potion_counter += 1
                    continue
            else:
                ans_text += f"\n{item_idx}- {item.name} -> +{item.value} {item.item_type}\n"
                ans_list.add(item.name)
                item_idx += 1 
                print(item.name)
                                                        
                print("*****")
                print(ans_list)
                print("*****")
            ans_text += f"--------\nTek Kullanımlık Eşyalar: "
            await send_message(session,chat_id,ans_text+f"\nGiymek istediğin eşyanın numarasını gir. (Menüden devam etmek için 0 yaz.)")
            user_data["state"] = "CHANGE_ITEM"
        else:
            await send_message(session,chat_id,"Çantanda eşya yok.\n1- Maceraya atıl\n2- Çantana göz at\n3- Durumunu gör")
    elif text == '3':
        weapon_name = current_player.equipped_weapon.name if current_player.equipped_weapon else "Yok"
        armor_name = current_player.equipped_armor.name if current_player.equipped_armor else "Yok"
        await send_message(session,chat_id,f"Özelliklerin:\nMaksimum Can:{current_player.max_hp}\nGüncel Can:{current_player.hp}\nHasar:{current_player.base_dmg}\nKullanılan Silah:{weapon_name}\nKullanılan Zırh:{armor_name}\nLevel:{current_player.lvl}\nXP:{current_player.xp}\nYeni Level'e kalan XP:{current_player.xp_to_lvl-current_player.xp}\n---------------\n1- Maceraya atıl\n2- Çantana göz at\n3- Durumunu gör")

async def choosing_fight_handler(session,chat_id,text,user_data):
    if text == '1':
        user_data["state"] = "FIGHT"
        await send_message(session,chat_id,f"1- Saldır\n2- Can iksiri iç.")
    elif text == '2':
        await send_message(session,chat_id,"Kaçıyorsun.\n1- Maceraya atıl\n2- Çantana göz at\n3- Durumunu gör")
        user_data["state"] = "MAIN_MENU"

async def fight_handle(session,chat_id,current_player,current_enemy,text,user_data):
    if text == '1':
        print(_memory)
        current_player.hp -= current_enemy.base_dmg
        current_enemy.hp -= current_player.base_dmg
        if current_player.hp <=0 :
            user_data["state"] = "TOP_MAIN_MENU"
            await send_message(session,chat_id,f"Öldün.\nAna menüdesin\n1-Oyuna başla\n2-Liderler tablosunu gör")                
        elif current_enemy.hp <=0 :
            await send_message(session,chat_id,f"Düşmanı öldürdün.\n{int(current_enemy.lvl*(1.5))} tecrübe puanı kazandın.\n----------\n1- Maceraya atıl\n2- Çantana göz at\n3- Durumunu gör")
            user_data["state"] = "MAIN_MENU"    
            current_player.xp += int(current_enemy.lvl*(1.5))
            while current_player.xp >= current_player.xp_to_lvl:
                current_player.xp -= current_player.xp_to_lvl
                current_player.lvl += 1
                print(F"Tebrikler! Level atladın. Yeni seviye: {current_player.lvl}!")
                current_player.max_hp = int(current_player.max_hp * 1.09)
                current_player.base_dmg = int(current_player.base_dmg * 1.1)
        else:
            await send_message(session,chat_id,f"Saldırdın.\nDüşmanın canı:{current_enemy.hp}, Senin canın:{current_player.hp}\n1-Saldır\n2-Can iksiri iç")
    if text == '2':
        await send_message(session,chat_id,f"Burada normalde canının artması lazım ama daha heal fonksiyonu yok :D")
        # TODO: Can fonksiyonu ekle eğer çanta varsa. 
        user_data["state"] = "FIGHT"

async def find_box_handle(session,chat_id,text,user_data,current_player,current_enemy):
    if text == "1":
        user_data["state"] = "MAIN_MENU"
        events = ["hp_potion","enemy","item","empty"]
        events_prob = [35,0,65,0]
        event = random.choices(events, weights=events_prob)[0]
        if event == "hp_potion":
            user_data["state"] = "HP_POTION"
            await send_message(session,chat_id,"Kutudan can iksiri çıktı! \n1- Kullan\n2- Çantana at")
            if event == "enemy":                                        
                user_data["state"] = "FIGHT"
                user_data["enemy"]= Enemy(current_player.max_hp,current_player.base_dmg,current_player.lvl)
                current_enemy = user_data.get("enemy")
                await send_message(session,chat_id,f"{current_enemy.name} ile karşılaştın.\n1-Saldır\n2-Can iksiri iç")
            elif event == "item":                                    
                itemm = random.choice(list(ITEM_DB.keys()))
                current_player.add_item(itemm)
                await send_message(session,chat_id,f"Kutudan {ITEM_DB[itemm]['name']} çıktı çantaya atıldı.\n1- Maceraya atıl\n2- Çantana göz at\n3- Durumunu gör")
                user_data["state"] = "MAIN_MENU"
            elif event == "empty":
                await send_message(session,chat_id,"Hiçbir şey çıkmadı.\n1- Maceraya atıl\n2- Çantana göz at\n3- Durumunu gör")
                user_data["state"] = "MAIN_MENU"
    else:
        user_data["state"] = "MAIN_MENU"
        await send_message(session,chat_id,"Kutuyu açmadın.")
        await send_message(session,chat_id,f"\n1- Maceraya atıl\n2- Çantana göz at\n3- Durumunu gör")
                                            
async def trap_handler(session,chat_id,text,user_data,current_player,current_enemy):
    
        if text == "1":
            user_data["state"] = "MAIN_MENU"
            hp_loss = [True,False]
            hp_loss_prob = [40,60]
            event = random.choices(hp_loss,weights=hp_loss_prob)[0]
            if event:
                if int(current_player.hp*0.2)  == 0:
                    current_player.hp -= 1
                    if current_player.hp <=0 :
                        user_data["state"] = "TOP_MAIN_MENU"
                        await send_message(session,chat_id,f"Öldün.\nAna menüdesin\n1-Oyuna başla\n2-Liderler tablosunu gör")
                    else:
                        await send_message(session,chat_id,f"Tuzaklardan yara aldın. {int(current_player.hp*0.2)} hasar aldın.\n1- Maceraya atıl\n2- Çantana göz at\n3- Durumunu gör")
                        current_player.hp -= int(current_player.hp*0.2)
                        if current_player.hp <=0 :
                            user_data["state"] = "TOP_MAIN_MENU"
                            await send_message(session,chat_id,f"Öldün.\nAna menüdesin\n1-Oyuna başla\n2-Liderler tablosunu gör")
                
            else:
                await send_message(session,chat_id,"Başarıyla tuzaklardan sıyrıldın.\n1- Maceraya atıl\n2- Çantana göz at\n3- Durumunu gör")
        elif text == "2":
            trap_enemy = [True,False]
            trap_enemy_prob = [35,65]
            event = random.choices(trap_enemy,weights=trap_enemy_prob)[0]
            if event:
                user_data["state"] = "FIGHT"
                user_data["enemy"] = Enemy(current_player.max_hp,current_player.base_dmg,current_player.lvl)
                current_enemy = user_data.get("enemy")
                await send_message(session,chat_id,f"Yavaşça geçerken {current_enemy.name} seni yakaladı. \n1-Saldır\n2-Can iksiri iç")
            else:
                await send_message(session,chat_id,f"Can kaybetmeden geçtin. \n1- Maceraya atıl\n2- Çantana göz at\n3- Durumunu gör")
                user_data["state"] = "MAIN MENU"

async def change_item_handler(session,chat_id,text,current_player,user_data):
    if text != "0" :
        idx = int(text)-1
        if 0 <= idx <len(current_player.inventory):
            picked_item = current_player.inventory[idx]
            current_player.equip_item(picked_item)
            await send_message(session,chat_id,f"\n1- Maceraya atıl\n2- Çantana göz at\n3- Durumunu gör")
            user_data["state"] = "MAIN_MENU"

async def hp_potion_handler(session,chat_id,current_player,text,user_data):
    if text != "0" :
        idx = int(text)-1
        if 0 <= idx <len(current_player.inventory):
            picked_item = current_player.inventory[idx]
            current_player.equip_item(picked_item)
            await send_message(session,chat_id,f"\n1- Maceraya atıl\n2- Çantana göz at\n3- Durumunu gör")
            user_data["state"] = "MAIN_MENU"
        else:
            await send_message(session,chat_id,f"\n1- Maceraya atıl\n2- Çantana göz at\n3- Durumunu gör")
            user_data["state"] = "MAIN_MENU"
                                            
    else:
        await send_message(session,chat_id,f"\n1- Maceraya atıl\n2- Çantana göz at\n3- Durumunu gör")
        user_data["state"] = "MAIN_MENU"
async def send_message(session,chat_id,text):
    url = f"{URL}/sendMessage"
    context={
        "chat_id":chat_id,
        "text": text
    }
    async with session.post(url, json=context) as response:
        return await response.json()
        
async def direct(session,chat_id,text):
    url = f"{URL}/sendMessage"
    context={
        "chat_id":chat_id,
        "text": text
    }
    async with session.post(url, json=context) as response:
        return await response.json()

async def listen_telegram_bot():
    async with aiohttp.ClientSession() as session:
        offset = None
        url = f"{URL}/getUpdates"
        param = {}
        async with session.get(url=url) as response:
                cleanup_data = await response.json()
                if cleanup_data.get("ok") and cleanup_data.get("result"):
                    last_message = cleanup_data["result"][-1]
                    offset = last_message["update_id"] + 1
                    print("Eski mesajlar temizlendi.")
                
                while True:
                    if "timeout" not in param:
                        param["timeout"]= 15
                        
                    if offset is not None:  
                        param["offset"] = offset
                    async with session.get(url=url,params=param) as response:
                        data = await response.json()
                        if data.get("ok") and data.get("result"):
                            for update in data["result"]:
                                message_data=update.get("message") 
                                if message_data:
                                    chat_id = message_data["chat"]["id"]
                                    text = message_data.get("text")
                                    user_data = get_user(chat_id)
                                    if user_data is None:
                                        new_player = {
                                            "player_obj" : Player(),
                                            "state" : "TOP_MAIN_MENU"
                                        }
                                        set_user(chat_id,new_player)   
                                        await send_message(session,chat_id,"Karakter Yaratıldı. Ana menüdesin\n1-Oyuna başla\n2-Liderler tablosunu gör")
                                        print(_memory)
                                    else:
                                        print("user_data",user_data)
                                        current_player = user_data["player_obj"]
                                        current_state = user_data["state"]
                                        current_enemy = user_data.get("enemy")

                                        if current_state == "TOP_MAIN_MENU":
                                            await top_main_menu_handler(session,chat_id,text,user_data)
                                            
                                        elif current_state == "MAIN_MENU":
                                            await main_menu_handler(session,chat_id,text,user_data,current_player)
                                        
                                        elif current_state == "CHOOSE_FIGHT":
                                            await choosing_fight_handler(session,chat_id,text,user_data)
                                        
                                        elif current_state == "FIGHT":
                                            await fight_handle(session,chat_id,current_player,current_enemy,text,user_data)
                                        
                                        elif current_state == "FIND_BOX":
                                            await find_box_handle(session,chat_id,text,user_data,current_player,current_enemy)
                                           
                                        elif current_state == "TRAPS":
                                            await trap_handler(session,chat_id,text,user_data,current_player,current_enemy)
                                        
                                        elif current_state == "CHANGE_ITEM":
                                           await change_item_handler(session,chat_id,text,current_player,user_data)
                                            
                                                

                                    
                                print(chat_id, text)
                                offset =update["update_id"]+1




if __name__ == "__main__":
    asyncio.run(listen_telegram_bot())


