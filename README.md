Implements all gecko codetypes that are ram writes with no memory, so 00, 02, 04, 06, C2, C6

Converts all of these into dolphin "Patches" 

Filters out every line that doesnt follow the standard of `* ` at the start
```
Ellipsoidal Shields
* C2874CD8 00000005
* EC1F0072 3C003F40
* 90010008 C0210008
* 3C003FA0 90010008
* C0410008 EC200072
* EC0000B2 00000000
* 04874CE0 D0210008
* 04874CE8 D0210010
```
 
becomes 
```
[OnFrame]
$Ellipsoidal shields
0x80874cd8:dword:0x4bccc528
0x80541200:dword:0xec1f0072
0x80541204:dword:0x3c003f40
0x80541208:dword:0x90010008
0x8054120c:dword:0xc0210008
0x80541210:dword:0x3c003fa0
0x80541214:dword:0x90010008
0x80541218:dword:0xc0410008
0x8054121c:dword:0xec200072
0x80541220:dword:0xec0000b2
0x80541224:dword:0x48333ab8
0x80874ce0:dword:0xd0210008
0x80874ce8:dword:0xd0210010
```
This is done since in the games I play, these codes can be used to create fun gameplay etc, but due to a bug in the way the emulator works, it can't handle the .elf launcher entering into the game instead of just starting in the game, so gecko codes dont work 

I noticed that the patches thing works, so i wrote this to convert gecko codes into functionally equivalent individual memwrites, including calculating branching to and from the hook codetype (C2)

This means we can synchronise gameplay between clients without having to transfer 2GB .raw files between each other as long as we have the same base file. 


any C2 commands will prompt you to provide a path to safe space to place the code into

if you just press enter it will continue on from last spot, so just update codeLoc above to somewhere you want and it'll be good

after everything is done, it will print "------------"

right click brawl in dolphin, go to properties, and click the bottom left button "edit config"

copy paste everything after the dashes to the very bottom of the config file shown, save and close (changing its name if you want)

toggle will be available on the patches page of brawl properties, and you can edit name from there instead if you want
