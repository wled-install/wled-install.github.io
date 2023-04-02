# (c) Wladislaw Waag, 2022-2023
import os, shutil, string

output_dir="_build"
bin_dir = "bin_dir"
suppl_dir = "suppl_dir"
manifest_dir = "manifest_dir"
output_bin_dir=os.path.join(output_dir,bin_dir)
output_suppl_dir=os.path.join(output_dir,suppl_dir)
output_manifest_dir=os.path.join(output_dir,manifest_dir)

def isbinfile_esp32(filename):
    if ("ESP32" in filename) or ("esp32" in filename):
        return True
    else:
        return False

def keyfunc(description):
    value=0
    if "ESP32" in description:
        value=value+100000
    if "1MB" in description:
        value=value+4000
    if "2MB" in description:
        value=value+2000
    if "original" not in description:
        value=value+10000
    if "Ethernet" in description:
        value=value+100
    return value
        
def proceed_dir(dir_path, dir_text, dir_path_forhtml):
    print(os.path.join(dir_path,"lastupdate.txt"))
    if os.path.exists(os.path.join(dir_path,"lastupdate.txt")):
        f_lastupdate=open(os.path.join(dir_path,"lastupdate.txt"),"r")
        datetext=f_lastupdate.read()
        f_lastupdate.close()
        html_list="<optgroup label=\""+dir_text+" (build date: "+datetext+")\">"+"\n"
    else:
        html_list="<optgroup label=\""+dir_text+"\">"+"\n"
    html_list_array=[]
    filelist=sorted(os.listdir(dir2_path))
    for bin_file in filelist:
        if bin_file[-4:]==".bin":
            # create manifest file
            manifest_filename="manifest_"+''.join(e for e in dir_text.replace(" ","_").replace(".","_") if (e.isalnum() or e=="_"))+"_"+bin_file[:-4]+".json"           
            manifest_path_forhtml="/"+manifest_dir+"/"+manifest_filename
            download_path_forhtml=dir_path_forhtml+"/"+bin_file
            manifest_path=os.path.join(output_manifest_dir,manifest_filename)
            f_manifest=open(manifest_path,"w+")
            template_filename=""
            dict={}
            AddInfo=", 4MB Flash";
            ESPtype=""
            if isbinfile_esp32(bin_file):
                ESPtype="ESP32"
                template_filename="./scripts/manifest_esp32_template.json"
                if ("_ETH" in bin_file) or ("_Ethernet" in bin_file):
                    AddInfo=AddInfo+", Ethernet";
            else:
                ESPtype="ESP8266"
                template_filename="./scripts/manifest_esp8266_template.json"
                AddInfo=", 4MB Flash: D1 mini etc.";
                if ("_1MB" in bin_file) or ("_ESP01" in bin_file):
                    AddInfo=", 1MB Flash";
                if ("_2MB" in bin_file) or ("_ESP02" in bin_file):
                    AddInfo=", 2MB Flash";
                
            if ("_AE" in bin_file) or ("_withAlexa" in bin_file):
                AddInfo=AddInfo+", Alexa enabled";
            if ("_ARE" in bin_file) :
                AddInfo=AddInfo+", with Audio reactive Usermod";
            if ("_AHI" in bin_file):
                AddInfo=AddInfo+", APA102 2MHz + Alexa/Hue/Infrared enabled";
            if ("_ABHI" in bin_file):
                AddInfo=AddInfo+", APA102 2MHz + Alexa/Blink/Hue/Infrared enabled";
            if ("_APA102FIX2MHZ" in bin_file):
                AddInfo=AddInfo+", APA102 2MHz";
            if ("_v41" in bin_file):
                AddInfo=AddInfo+", LEDPIN=16, DigMic = Generic I2S";
            if ("_OB" in bin_file):
                AddInfo=AddInfo+", original Build";
            if ("_OB" in bin_file) and ("SR_" in bin_file):
                AddInfo=AddInfo+", Alexa/Hue/Infrared disabled";
            if ("_MQTT" in bin_file):
                AddInfo=AddInfo+", MQTT enabled";
            if ("_MDEVMAX" in bin_file) or (("WLEDMM_" in bin_file) and (("_max" in bin_file) or  ("_M.bin" in bin_file))):
                AddInfo=AddInfo+", M: mods included: audio reactive, games, weather, custom effects, mpu6050 + other improvements";
            if ("WLEDMM_" in bin_file) and ("_S.bin" in bin_file):
                AddInfo=AddInfo+", S: mods included: audio reactive";
            if ("WLEDMM_" in bin_file) and ("_XL.bin" in bin_file):
                AddInfo=AddInfo+", XL: almost all mods included";
            if (("WLEDSR_" in bin_file) and ("_max" in bin_file)):
                AddInfo=AddInfo+", some additional mods included";
            if (("WLEDSR_" in bin_file) and ("_M" in bin_file)):
                AddInfo=AddInfo+", M: some additional mods included: temp Sensor, 4-L Display, rotary encoder, auto Save";
            if (("WLEDSR_" in bin_file) and ("_S" in bin_file)):
                AddInfo=AddInfo+", S: no additional mods";
            if ("_debug" in bin_file):
                AddInfo=AddInfo+", DEBUG enabled"
            if ("_micdebug" in bin_file):
                AddInfo=AddInfo+", Microphone debug enabled"
            if ("_DIGIN" in bin_file):
                AddInfo=AddInfo+", digital line-in support";
            if ("_HSDIGIN" in bin_file):
                AddInfo=AddInfo+", high sense digital line-in support";
            dict["ADDINFO"]=AddInfo;
            dict["VERSION"]=dir_text;    
            dict["BINFILE"]=dir_path_forhtml+"/"+bin_file; 
            f_template=open(template_filename, "r")
            template=string.Template(f_template.read())
            f_manifest.write(template.substitute(dict));
            f_manifest.close()
            #html_list=html_list+(bin_file+" "+manifest_path_forhtml+ " "+ ESPtype+" ("+AddInfo[2:]+")" + "\n")
            html_list_array.append("<option data-manifest_file=\""+manifest_path_forhtml+ "\" data-download_file=\"" +download_path_forhtml+ "\">"+ ESPtype+" ("+AddInfo[2:]+")" + "</option>")
    html_list_array_sorted=sorted(html_list_array, key=keyfunc)
    for item in html_list_array_sorted:
        html_list=html_list+item+"\n"
    return html_list
    
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if os.path.exists(output_bin_dir):
    shutil.rmtree(output_bin_dir)
if os.path.exists(output_manifest_dir):
    shutil.rmtree(output_manifest_dir)
shutil.copytree(bin_dir,output_bin_dir)
if os.path.exists(output_suppl_dir):
    shutil.rmtree(output_suppl_dir)
shutil.copytree(suppl_dir,output_suppl_dir)
if not os.path.exists(output_manifest_dir):
    os.makedirs(output_manifest_dir)

dirs1=sorted(os.listdir(output_bin_dir))
html_list=""
for dir1 in dirs1:
    dir1_path=os.path.join(output_bin_dir,dir1)
    if os.path.isdir(dir1_path):
        dir1_text=dir1[2:].replace("_"," ")
        dirs2=sorted(os.listdir(dir1_path), reverse=True)
        for dir2 in dirs2:
            dir2_path=os.path.join(dir1_path,dir2)
            if os.path.isdir(dir2_path):
                dir2_text=dir1_text + ": " + dir2.replace("_"," ")
                html_list = html_list + proceed_dir(dir2_path, dir2_text, "/"+bin_dir+"/"+dir1+"/"+dir2)
                
f_template=open("./scripts/index_template.html", "r")
template=string.Template(f_template.read())
dict={}
dict["HTMLLIST"]=html_list
f_index= open(os.path.join(output_dir,"index.html"),"w+")
f_index.write(template.substitute(dict))
f_index.close()
