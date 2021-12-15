ba = 0x80000000
po = 0x90000000
patch = []
codeLoc = 0x80541200
path = "./codeset.txt" #first convert code to just the general wall of hex normal codesets (not gctrm) and point to it here

#any C2 commands will prompt you to provide a path to safe space to place the code into
#if you just press enter it will continue on from last spot, so just update codeLoc above to somewhere you want and it'll be good
 
#after everything is done, it will print "------------"
#right click brawl in dolphin, go to properties, and click the bottom left button "edit config"
#copy paste everything after the dashes to the very bottom of the config file shown, save and close (changing its name if you want)
#toggle will be available on the patches page of brawl properties, and you can edit name from there instead if you want
 
 

def getLine(file):
    l = file.readLine()
    return l

def extractCommand(line):
    parts = [int(d,16) for d in line.split(" ")]
    data ={
        "type" : (parts[0] & 0xE0000000)>>29,
        "subType" : (parts[0] & 0x0E000000)>>25,
        "address" : parts[0] & 0x01FFFFFF,
        "secondWord" : parts[1]
        }

    bapo = parts[0] & 0x10000000
    if bapo == 0:
        data["address"] += ba
    else:
        data["address"] += po
    
    return data
    
def patchLine(address, data, size):
    sizeLabel = "n/a"
    if size == 4:
        sizeLabel = "dword"
    elif size == 2:
        sizeLabel = "word"
    elif size == 1:
        sizeLabel = "byte"

    patchLine = hex(address) + ":" + sizeLabel + ":" + hex(data)
    patch.append(patchLine)

    print(patchLine)
    return patchLine

def directRamWrites(gecko, code):
    if gecko["subType"] == 0: #00 command, 8 bit write & fill
        data = gecko["secondWord"]
        repeat = (data&0xFFFF0000)>>16
        val = data&0xFF
        for i in range(repeat+1): 
            patchLine(gecko["address"] + i, val, 1)
    elif gecko["subType"] == 1: #02 command, 16 bit write & fill
        data = gecko["secondWord"]
        repeat = (data&0xFFFF0000)>>16
        val = data&0xFFFF
        for i in range(repeat+1):
            patchLine(gecko["address"] + i, val, 2)
    elif gecko["subType"] == 2: #04 command, 32 bits write
        patchLine(gecko["address"], gecko["secondWord"], 4)
    elif gecko["subType"] == 3: #06 command, String Write
        repeat = gecko["secondWord"]
        data = "";
        
        for i in range(repeat):
            if data == "":
                data = code.pop(0).replace(" ", "")
                print(data)
            patchLine(gecko["address"]+i, int(data[0:2],16), 1)
            data = data[2::]
    else:
        return False #else subType not handled
    return True

def asmCodes(gecko, code):
    if gecko["subType"] == 1: #C2 command, hook
        hookAddr = gecko["address"]
        length = gecko["secondWord"]
        
        #print("hook " + hex(hookAddr))

        print("please provide address for hook at " + hex(hookAddr))
        newLoc = input()
        
        global codeLoc
        if newLoc:
            codeLoc = int(newLoc, 16)
        
            
        branchThere = 0x48000000 + ((codeLoc-hookAddr) & 0x03FFFFFF)
        
        patchLine(hookAddr, branchThere, 4)
        for i in range(length):
            line = [int(d,16) for d in code.pop(0).split(" ")]
            patchLine(codeLoc, line[0], 4)
            if i+1 != length:
                patchLine(codeLoc+4, line[1], 4)
            else:
                branchBack = 0x48000000 + ((hookAddr-codeLoc)&0x03FFFFFF)
                patchLine(codeLoc+4, branchBack, 4)
            codeLoc += 8
    elif gecko["subType"] == 3: #C6 command, branch look
        branch = 0x48000000 + ((gecko["secondWord"]-gecko["address"])&0x03FFFFFF)
        patchLine(gecko["address"], branch, 4)
    else:
        return False #else subType not handled
    return True

def processLine(code):
    if len(code) == 0:
        return False
    gecko = extractCommand(code.pop(0))
    if gecko["type"] == 0: #ramWrite codetype
        return directRamWrites(gecko, code)
    elif gecko["type"] == 6: #asm codetype
        return asmCodes(gecko, code)
    return False #else codeType not handled
        
codesetAddr = path
lines = []
with open(codesetAddr) as codeset:
    lines = [l[2:19] for l in codeset if l.startswith("*")]

print(lines)


while processLine(lines):
    pass

if len(lines):
    print("didnt finish handling data, reached just before this line")
    print(lines)
    print("didnt finish handling data, reached just before this line")
else:
    print("------------")

    print("[OnFrame]")
    print("$Code name goes here")
    for line in patch:
        print(line)
