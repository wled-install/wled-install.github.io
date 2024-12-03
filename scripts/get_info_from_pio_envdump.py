import sys
import re

def GetChipType(line):
    expr=re.search('(?<=--chip )\S*',line)
    if(expr):
        return expr[0]
    else:
        return ""

def GetChipFamily(line):
    chiptype=GetChipType(line);
    if chiptype=="esp8266":
        return "ESP8266"
    if chiptype=="esp32":
        return "ESP32"
    if chiptype=="esp32c3":
        return "ESP32-C3"
    if chiptype=="esp32s2":
        return "ESP32-S2"
    if chiptype=="esp32s3":
        return "ESP32-S3"
    if chiptype=="esp32c6":
        return "ESP32-C6"
    return ""

def GetBootloaderFilePath(line):
    expr=re.search('(?<= )\S*bootloader\S*.bin',line)
    if(expr):
        return expr[0]
    else:
        return ""

def GetBootloaderAddress(line):
    expr=re.search('(?<= )0x\S+(?= \S*bootloader\S*.bin)',line)
    if(expr):
        return expr[0]
    else:
        return ""

def GetBoot0FilePath(line):
    expr=re.search('(?<= )\S*boot_app0\S*.bin',line)
    if(expr):
        return expr[0]
    else:
        return ""

def GetBoot0Address(line):
    expr=re.search('(?<= )0x\S+(?= \S*boot_app0\S*.bin)',line)
    if(expr):
        return expr[0]
    else:
        return ""

def GetPartitionsFilePath(line):
    expr=re.search('(?<= )\S*partitions\S*.bin',line)
    if(expr):
        return expr[0]
    else:
        return ""

def GetPartitionsAddress(line):
    expr=re.search('(?<= )0x\S+(?= \S*partitions\S*.bin)',line)
    if(expr):
        return expr[0]
    else:
        return ""
        
def GetFirmwareFilePath(line):
    expr=re.search('(?<= )\S*firmware\S*.bin',line)
    if(expr):
        return expr[0]
    else:
        return ""

filename = sys.argv[1]
rettype  = sys.argv[2]
f=open(filename)
file_lines=f.read();
#print(file_lines.replace("\n","").replace("\r",""))
expr=re.search(r'(?<=\'UPLOADERFLAGS\')[^\]]*(?=\])',file_lines.replace("\n","").replace("\r",""))
if(expr):
    line = expr[0].replace("'","").replace(","," ").replace("\\\\","\\")
    while '  ' in line:
        line = line.replace('  ', ' ')
    #print(line)
    line2=""
    if(GetChipType(line)!="esp8266"):
        expr2=re.search(r'(?<=\'ESP32_APP_OFFSET\')[^,]*(?=,)',file_lines.replace("\n","").replace("\r",""))
        if(expr2):
            line2=expr2[0].replace(":","").replace("'","").replace(" ","");
            if(line2==None):
                line2="0x10000"
            if(line2=="None"):
                line2="0x10000"
    else:
        line2="0x0"
    if(rettype=="CT"):
        print(GetChipType(line))
    if(rettype=="CF"):
        print(GetChipFamily(line))
    if(rettype=="BFP"):
        # bootloader file path
        print(GetBootloaderFilePath(line))
    if(rettype=="BA"):
        # bootloader file path
        print(GetBootloaderAddress(line))
        
    if(rettype=="B0FP"):
        # bootloader file path
        print(GetBoot0FilePath(line))
    if(rettype=="B0A"):
        # bootloader file path
        print(GetBoot0Address(line))
        
    if(rettype=="PFP"):
        # bootloader file path
        print(GetPartitionsFilePath(line))
    if(rettype=="PA"):
        # bootloader file path
        print(GetPartitionsAddress(line))
    
    if(rettype=="FFP"):
        # bootloader file path
        print(GetFirmwareFilePath(line))
    if(rettype=="FA"):
        # bootloader file path
        print(line2)
    
    if(rettype=="MF"):
        # manifest file
        if(len(sys.argv)>=4):
            addpath = sys.argv[3]
        else:
            addpath = "";
        print("{");
        print("  \"name\": \"WLED (custom build for "+GetChipType(line)+")\",");
        print("  \"version\": \"custom version\",");
        print("  \"new_install_prompt_erase\": false,");
        print("  \"builds\": [");
        print("    {");
        print("      \"chipFamily\": \""+GetChipFamily(line)+"\",\n      \"parts\": [");
        FA=line2;
        PA=GetPartitionsAddress(line);
        BA=GetBootloaderAddress(line);
        B0A=GetBoot0Address(line);
        if(BA!=""):
            print("        { \"path\": \""+addpath+"bootloader.bin\", \"offset\": "+str(int(BA,16))+" },");
        if(PA!=""):    
            print("        { \"path\": \""+addpath+"partitions.bin\", \"offset\": "+str(int(PA,16))+" },");
        if(B0A!=""):    
            print("        { \"path\": \""+addpath+"boot_app0.bin\", \"offset\": "+str(int(B0A,16))+" },");
        if(FA!=""):    
            print("        { \"path\": \""+addpath+"wled.bin\", \"offset\": "+str(int(FA,16))+" }");   
        print("      ]");
        print("    }");
        print("  ]");
        print("}");

f.close()
