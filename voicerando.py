#KH2FM Voice Rando
#By Tasos500

#The point of this script is to get all files from folders
#corresponding to all versions of KH2 (JP,US,FR,GR,SP,IT),
#and specifically voice files, check which ones exist in each version,
#due to FM having extra content, then randomizing either through RANDOM.ORG,
#or an offline randomizer, then picking the file for each language, and
#adding it to a "voice" folder, which can then be used to create a .kh2patch
#file. This *might* be possible automatically, if Python can interact with
#CrazyCatz's Patcher, or possibly making a YAML file for OpenKH compatibility,
#using the bodge of a script I made eariler.

#NOTE:The working directory (AKA where this script is run)
#should be the same as this script's, or else this won't work.
#Also, if you don't want this to crash and burn, you NEED
#KH2FM files in there, as a failsafe.

#CHANGELOG
#
#V1.1
#Added automatic .kh2patch creation (Using KH2FM Toolkit), and OpenKH Mod creation (By making the mod.yml and zipping everything)

#import everything needed
import requests
import os
import random
import shutil
import zipfile
import subprocess
import requests

#functions for later
def KH2FM_Toolkit():
    text = open("event.txt", "r")
    event_pre = text.read()
    event_pre = list(event_pre.split("\n"))
    text.close()
    text = open("battle.txt", "r")
    battle_pre = text.read()
    battle_pre = list(battle_pre.split("\n"))
    text.close()
    log = open("log.txt", "w+")
    log.write("\n")
    for item in event_pre:
        log.write("voice/fm/event/" + item + "\n\nn\n\nn\n")
    for item in battle_pre:
        log.write("voice/us/battle/" + item + "\n\nn\n\nn\n")
    log.write("voice/fm/gumibattle/gumi.vsb\n\nn\n\nn\n")
    log.write("\n\n\n")
    log.close()

    args = "KH2FM_Toolkit.exe -patchmaker -batch -author Voice_Rando -version 1 -skipcredits -skipchangelog -uselog log.txt".split()
    FNULL = open(os.devnull, "w")
    p = subprocess.call(args, stdout=FNULL)
    FNULL.close()
    os.remove("log.txt")
    os.rename("output.kh2patch", "Voice_Rando.kh2patch")

def OpenKH():
    #Create mod.yml file, and fill it with data
    yml = open("mod.yml", "w+")
    text = open("event.txt", "r")
    text = text.read()
    text = list(text.split("\n"))
    
    yml.write("title: Rando Voices\nassets:\n")
    for x in text:
        yml.write("  - name: voice/fm/event/" + x + "\n")
        yml.write("    method: copy"+ "\n")
        yml.write("    source:"+ "\n")
        yml.write("      - name: voice/fm/event/" + x+ "\n")

    text = open("battle.txt", "r")
    text = text.read()
    text = list(text.split("\n"))

    for x in text:
        yml.write("  - name: voice/us/battle/" + x + "\n")
        yml.write("    method: copy"+ "\n")
        yml.write("    source:"+ "\n")
        yml.write("      - name: voice/us/battle/" + x+ "\n")

    yml.write("  - name: voice/fm/gumibattle/gumi.vsb" + "\n")
    yml.write("    method: copy"+ "\n")
    yml.write("    source:"+ "\n")
    yml.write("      - name: voice/fm/gumibattle/gumi.vsb" + "\n")

    openkhzip = zipfile("Voice_Rando.zip", "w")
    openkhzip.write("mod.yml")
    for root, dirs, files in os.walk("voice"):
        for f in files:
            openkhzip.write(os.path.join(root, f))
    openkhzip.close()
    yml.close()
    os.remove("mod.yml")

#checking if language folder exists
print("Checking for languages...\n")
lang = ["jp", "us", "fr", "gr", "sp", "it"]
langs = []
for item in lang:
    if (os.path.isdir(item)):
        langs.append(item)
print("Found " + str(len(langs)) + " languages.")

#Check for folders existing (jp,us,fr,gr,sp,it), and make a list of all files.
#Structure should be similar to a non-FM build's "voice" folder. (\lang\category\file.extension)
#Make sure the directory structure is identical in all languages.
#e.g. FM uses three internal languages (fj,fm,us), but this script only recognizes the folders listed above, for simplicity's sake.
print("Sorting every file...\nThis may take some time...\n")

text = open("event.txt", "r")
event_pre = text.read()
event_pre = list(event_pre.split("\n"))
text = open("battle.txt", "r")
battle_pre = text.read()
battle_pre = list(battle_pre.split("\n"))

battle = []
gumibattle = []
event = []
for item in langs:
#    if (os.path.isdir(os.path.join(item, "battle"))):
#        battle.append (os.listdir(os.path.join(item, "battle")))
    battle.append(battle_pre)
    if (os.path.isdir(os.path.join(item, "gumibattle"))):
        gumibattle.append (os.listdir(os.path.join(item, "gumibattle")))
#    if (os.path.isdir(os.path.join(item, "event"))):
#        event.append (os.listdir(os.path.join(item, "event")))
    event.append(event_pre)

#Check how many versions of each file exist per unique file.
#First, find every unique file.
#Objects in sets are unique, hence we're using sets here.
battle_u = set()
gumibattle_u = set()
event_u = set()
for item in battle:
    stuff = set(item)
    battle_u = battle_u.union(stuff)
for item in gumibattle:
    stuff = set(item)
    gumibattle_u = gumibattle_u.union(stuff)
for item in event:
    stuff = set(item)
    event_u = event_u.union(stuff)
    
#Next, for every item in each set of unique filenames, make a list of each language each file exists in (in numbers starting from zero).
battle_u_langs = []
gumibattle_u_langs = []
event_u_langs = []
for stuff in battle_u:
    langs_num = []
    for item in langs:
        if(stuff in battle[langs.index(item)]):
            langs_num.append(langs.index(item))
    battle_u_langs.append(langs_num)
for stuff in gumibattle_u:
    langs_num = []
    for item in langs:
        if(stuff in gumibattle[langs.index(item)]):
            langs_num.append(langs.index(item))
    gumibattle_u_langs.append(langs_num)
for stuff in event_u:
    langs_num = []
    for item in langs:
        if(stuff in event[langs.index(item)]):
            langs_num.append(langs.index(item))
    event_u_langs.append(langs_num)
print("Sorting complete!")
#Get number of files to randomize
battle_len = len(battle_u)
gumibattle_len = len(gumibattle_u)
event_len = len(event_u)
total = battle_len + gumibattle_len + event_len
print("Total files to be randomized:", total)

#Randomize using RANDOM.ORG
print("Randomizing...\n")
url = ("https://www.random.org/integers/?num=" + str(total) + "&min=0&max=" + str((len(langs)-1)) + "&col=1&base=10&format=plain&rnd=new")
response = requests.get(url)
if (response.status_code == 200):
    print("Online randomization successful!\n")
    numbers = list(response.text.split("\n"))
    numbers.remove("")
    for i in range(0, len(numbers)): 
        numbers[i] = int(numbers[i])
#If randomization fails for whatever reason, use a pseudorandomizer,
#to avoid spamming RANDOM.ORG.
else:
    print("Online randomization failed. Using pseudorandomizer instead...\n")
    numbers = []
    for x in range(total):
        numbers.append(random.randint(0, (len(langs)-1)))
    print("Pseudorandomization successful!\n")

#Add everything to a "voice" folder, based on the (pseudo)randomized numbers.
#(THAT FOLDER WILL GET CLEARED, MAKE BACKUPS OF ITS CONTENTS IF YOU CARE ABOUT THEM)
#This part sucks A LOT. If anyone could fix it so that it doesn't need a failsafe,
#that would save me oh so much trouble.
print("Sorting files...\nThis will take a LONG time. Please be patient...")
if (os.path.isdir("voice")):
    shutil.rmtree("voice")
os.mkdir("voice")
battle_dest = "voice/us/battle"
gumibattle_dest = "voice/fm/gumibattle"
event_dest = "voice/fm/event"
os.mkdir("voice/us")
os.mkdir("voice/fm")
os.mkdir("voice/us/battle")
os.mkdir("voice/fm/gumibattle")
os.mkdir("voice/fm/event")
battle_list = battle_pre
gumibattle_list = list(gumibattle_u)
event_list = event_pre
count = 0
for x in range(battle_len):
    if numbers[count] in battle_u_langs[x]:
        file_source = (str(langs[numbers[count]]) + "/battle/" + str(battle_list[x]))
        file_dest = (battle_dest + "/" + str(battle_list[x]))
        try:
            shutil.copyfile(file_source, file_dest)
        except FileNotFoundError:
            file_source = ("us/battle/" + str(battle_list[x]))
            shutil.copyfile(file_source, file_dest)
    else:
        while (True):
            newint = random.randint(0, (len(langs)-1))
            if newint in battle_u_langs[x]:
                file_source = (str(langs[numbers[count]]) + "/battle/" + str(battle_list[x]))
                file_dest = (battle_dest + "/" + str(battle_list[x]))
                try:
                    shutil.copyfile(file_source, file_dest)
                except FileNotFoundError:
                    file_source = ("us/battle/" + str(battle_list[x]))
                    shutil.copyfile(file_source, file_dest)
                break
    count += 1
for x in range(gumibattle_len):
    if numbers[count] in gumibattle_u_langs[x]:
        file_source = (str(langs[numbers[count]]) + "/gumibattle/" + str(gumibattle_list[x]))
        file_dest = (gumibattle_dest + "/" + str(gumibattle_list[x]))
        try:
            shutil.copyfile(file_source, file_dest)
        except FileNotFoundError:
            file_source = ("us/gumibattle/" + str(gumibattle_list[x]))
            shutil.copyfile(file_source, file_dest)
    else:
        while (True):
            newint = random.randint(0, (len(langs)-1))
            if newint in gumibattle_u_langs[x]:
                file_source = (str(langs[numbers[count]]) + "/gumibattle/" + str(gumibattle_list[x]))
                file_dest = (gumibattle_dest + "/" + str(gumibattle_list[x]))
                try:
                    shutil.copyfile(file_source, file_dest)
                except FileNotFoundError:
                    file_source = ("us/gumibattle/" + str(gumibattle_list[x]))
                    shutil.copyfile(file_source, file_dest)
                break
    count += 1
for x in range(event_len):
    if numbers[count] in event_u_langs[x]:
        file_source = (str(langs[numbers[count]]) + "/event/" + str(event_list[x]))
        file_dest = (event_dest + "/" + str(event_list[x]))
        try:
            shutil.copyfile(file_source, file_dest)
        except FileNotFoundError:
            file_source = ("us/event/" + str(event_list[x]))
            shutil.copyfile(file_source, file_dest)
    else:
        while (True):
            newint = random.randint(0, (len(langs)-1))
            if newint in event_u_langs[x]:
                file_source = (str(langs[numbers[count]]) + "/event/" + str(event_list[x]))
                file_dest = (event_dest + "/" + str(event_list[x]))
                try:
                    shutil.copyfile(file_source, file_dest)
                except FileNotFoundError:
                    file_source = ("us/event/" + str(event_list[x]))
                    shutil.copyfile(file_source, file_dest)
                break
    count += 1
#Give an option to automatically create a patch.
while True:
    os.system("cls")
    print("\nSorting complete!\nWhat would you like to do next?\n")
    print("1 - Create .kh2patch File")
    print("2 - Create OpenKH Mod")
    print("3 - Create both a patch and a mod")
    print("4 - Quit (You'll need to make your patch/mod manually)\n")
    ans=input("Your choice (1-4): ")
    try:
        ans = int(ans)
    except ValueError:
        continue
    if (ans==1):
        print("\nCreating patch... Please wait a bit...")
        KH2FM_Toolkit()
        print("Done!")
        break
    elif (ans==2):
        if not os.path.isfile("KH2FM_Toolkit.exe"):
            print("\nKH2FM_Toolkit was not found. Downloading...")
            r = requests.get("https://code.govanify.com/api/v1/repos/govanify/KH2FM_Toolkit/releases/5/assets/6")
            if r.status_code == 200:
                r = r.json()
                req = requests.get(r["browser_download_url"])
                f = open("KH2FM_Toolkit.zip", "wb")
                f.close()
                zipped = zipfile.ZipFile("KH2FM_Toolkit.zip")
                zipped.extractall()
                zipped.close()
                os.remove("KH2FM_Toolkit.zip")
            else:
                raw_input("\nDownload failed.\nCheck your Internet connection, or Govanify's Repository at:\nhttps://code.govanify.com/govanify/KH2FM_Toolkit \n\nPress any key to go back to the previous menu...")
                continue
        print("\nCreating mod... Please wait a bit...")
        OpenKH()
        print("Done!")
        break
    elif (ans==3):
        print("\nCreating patch... Please wait a bit...")
        KH2FM_Toolkit()
        print("Patch done!")
        if not os.path.isfile("KH2FM_Toolkit.exe"):
            print("\nKH2FM_Toolkit was not found. Downloading...")
            r = requests.get("https://code.govanify.com/api/v1/repos/govanify/KH2FM_Toolkit/releases/5/assets/6")
            if r.status_code == 200:
                r = r.json()
                req = requests.get(r["browser_download_url"])
                f = open("KH2FM_Toolkit.zip", "wb")
                f.close()
                zipped = zipfile.ZipFile("KH2FM_Toolkit.zip")
                zipped.extractall()
                zipped.close()
                os.remove("KH2FM_Toolkit.zip")
            else:
                raw_input("\nDownload failed.\nCheck your Internet connection, or Govanify's Repository at:\nhttps://code.govanify.com/govanify/KH2FM_Toolkit \n\nPress any key to go back to the previous menu...")
                continue
        print("\nCreating mod... Please wait a bit...")
        OpenKH()
        print("Mod done!")
        break
    elif (ans==4):
        break
    else:
        continue

