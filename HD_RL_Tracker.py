from difflib import get_close_matches
import pandas as pd
import re
import os

Names = ["69Klim69", "Abdulleq", "AlessioQ", "Amarilus", "Amelena", "AminhaVida", "Anubis I", "AoDCthulhu", "Arthurion", "Ashrak Jaffa", "Athena Owl",
    "Ba1erion", "Birdyy", "Bobwire", "BANK k101", "BROLIK", "Capt Black", "Cearmada", "Cid Kagenou", "CoRtEx", "CrimsonMage", "DayO", "Diablita", "DiAvolA", "Didic",
    "Dopehop", "DR D00M", "DYDY", "DynamoDave", "Effe", "Env0y", "Favofest", "Fe4rLess", "GeorgeBylis",
    "GryphoS", "Hadzy", "HSU Y", "Irysman", "Jaken Y", "JerSi", "Kazeh", "Khraan", "Kissabath", "Knowbody",
    "L T", "Lady Dirla", "LadyAyla", "LARISSA", "Lord Goblin", "Lord Tulip",
    "mituk86", "Moneta", "Mr Boombastc", "MUDKIP", "MyLord", "ninna", "nobrownie", "PacoVega", "pic", "Problemka", "ProtheaN",
    "Ragnarek", "RhaeNyrA", "Rosamunde91", "S Blackstar", "samkoukai", "SavageHenry", "Sentinelle12", "SexyPup", "ShakesPeareX", "Shatoni",
    "shinigamisan", "shrike", "SlackOfDoom", "Spartan1313", "SSC", "Stormerhavoc",
    "Stunnz", "Tershav", "The Doge", "The Plague", "Thor Ride", "Two faces", "Virgiliy", "Vit121",
    "Vredesbyrdd", "WEBANGEL", "WELISSA", "WINDOWLICKER", "x Neo x", "Xarcon", "xRACHELx", "XxKENPACHIxX", "XPred Taly X", "xXoGenooXx", "xxWATTYxx",
    "Zarachiel", "Zaratus", "Ksaltotun", "Cypherr", "Herr Knispel", "lowells", "Raimund"]

def isPlayer(row):
    if(row.find('(') != -1):
        return False
    else:
        return True

def player_list(lines):
    Name = []
    for row in lines:
        row = row.strip('\n')
        if (isPlayer(row)):
            Name.append(row)
        else:
            return Name  

def clear_char(char):
    score = ""
    cpt = 0
    while((char[cpt] != '(') and cpt < len(char)-1):
        score = score + char[cpt]
        cpt = cpt + 1
    return score

def find_closest_string(input_string, string_list, cutoff=0.5):
    matches = get_close_matches(input_string, string_list, n=1, cutoff=cutoff)
    return matches[0] if matches else find_specific_match(input_string)

def find_specific_match(name):
    print(name)
    if name == "XXWA'I'I'YXX":
        return "xxWATTYxx"
    return "ERROR :" + name

def process_text(text_file_path, csv_folder):
    csv_filename = os.path.basename(text_file_path).replace('.txt', '.csv')
    csv_file_path = os.path.join(csv_folder, csv_filename)
    List = []
    with open(text_file_path, 'r') as input_file:
        for row in input_file.readlines():
            clean_row = re.sub(r"\s+\(", "(", row)
            clean_row = clean_row.replace(")(", ") (")
            clean_row = re.sub(r"\(\s*(.*?)\s*\)", lambda m: f"({m.group(1).replace(' ', '')})", clean_row)
            data = clean_row.strip('\n').split(' ')
            if len(data) == 1:
                continue
            PlayerName = data[:-6]
            name = ""
            if len(PlayerName) > 1:
                for txt in PlayerName:
                    name = name + " " + txt
            else:
                print(data)
                name = PlayerName[0]
            name = name.strip(" ")
            if name not in Names:
                name = find_closest_string(name, Names)
            RL6 = clear_char(data[-1])
            RL5 = clear_char(data[-2])
            List.append([name, RL5, RL6])
        input_file.close

    df = pd.DataFrame(data=List, columns=["Name","L5","L6"])
    with open(csv_file_path, 'w', newline='') as csv_file:
        df.to_csv(csv_file, index=False)
    return csv_filename