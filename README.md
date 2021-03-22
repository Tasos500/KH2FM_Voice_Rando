# KH2FM Voice Randomizer
A Python script that randomizes voice files and creates a patch or mod for use in KH2FM.

# How to use
Create a folder that includes `voicerando.py`, `battle.txt`, and `event.txt`. Next, inside the above folder, create folders matching each language KH2 has been released in that you want to include in the randomizer (jp,us,fr,gr,sp,it), with the following layout:
```
├───fr
│   ├───battle
│   ├───event
│   └───gumibattle
├───gr
│   ├───battle
│   ├───event
│   └───gumibattle
├───it
│   ├───battle
│   ├───event
│   └───gumibattle
├───jp
│   ├───battle
│   ├───event
│   └───gumibattle
├───sp
│   ├───battle
│   ├───event
│   └───gumibattle
├───us
│   ├───battle
│   ├───event
│   └───gumibattle
```

For `us`, it's recommended to use KH2FM's English language files, as a failsafe in case a language chosen doesn't have a file that matches a voiceline in English 2FM cutscenes.

After this setup is complete, run `python voicerando.py` on the CLI of your choice, and the randomizer will either use RANDOM.ORG's number generator for true randomness, or in case there's any issue with the service, Python's pseudorandomizer.

After all the files are assembled, you will be given the option to either create an OpenKH-compatible mod, which should in theory also be usable with the PC port (will need to check that once that is out), a .kh2patch file to be used with CrazyCatz' patcher or KH2FM_Toolkit, or both.
If you want to create a patch, KH2FM_Toolkit will be downloaded first, as it's required for this process. In case this fails, you will be notified of this. No such prerequisite is required for creating an OpenKH mod.

At the end, `Voice_rando.zip` and `Voice_Rando.kh2patch` will be created in the folder for mods and patches, respectively.
