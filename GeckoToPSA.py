def interp(code):
    lines = code.split("* ")[1:]
    address = int(lines[0].split(" ")[0],16)-0x6000000+0x80000000
    length = int(int(lines[0].split(" ")[1],16) / 8) + 1
    output = ""
    for line in lines[1:length]:
        if int(line.split(" ")[0],16) > 0x10:
            command = line.split(" ")[0]
            args = int(line.split(" ")[1], 16)
            argcount = int(command[4:6],16)
            output += "E=" + command + ":"
            for i in range(0, argcount):
                offset = int((args - address)/4) + 1 + i
                if offset <= length:
                    data = lines[offset].split(" ")
                    output += str(int(data[0])) + "-" + hex(int(data[1],16))[2:].zfill(8) + ","
            
    print(output)

interp("* 06545F68 00000030* 00000000 00000009* 00000002 80FAD9DC* 00000002 80545F80* 07020000 00000000* 0D000200 80545F68* 00080000 00000000")

#E=07020000:E=0D000200:0-00000009,2-80FAD9DC,
#E=07020000:E=0D000200:0-00000009,2-80FAD9DC,E=07020000:
#E=07020000:E=0D000200:0-00000009,2-2163923420,E=00080000:
