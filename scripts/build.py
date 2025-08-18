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

def isbinfile_esp32c3(filename):
    if (("ESP32C3" in filename) or ("esp32c3" in filename) or ("esp32C3" in filename) or ("ESP32c3" in filename) or ("ESP32-C3" in filename) or ("esp32-c3" in filename)):
        return True
    else:
        return False

def isbinfile_esp32s2(filename):
    if (("ESP32S2" in filename) or ("esp32s2" in filename) or ("esp32S2" in filename) or ("ESP32s2" in filename) or ("ESP32-S2" in filename) or ("esp32-s2" in filename)):
        return True
    else:
        return False

def isbinfile_esp32s3(filename):
    if (("ESP32S3" in filename) or ("esp32s3" in filename) or ("esp32S3" in filename) or ("ESP32s3" in filename) or ("ESP32-S3" in filename) or ("esp32-s3" in filename)):
        return True
    else:
        return False

def keyfunc(description):
    value=0
    if "ESP32" in description:
        value=value+100000
    if "ESP32C3" in description:
        value=value+200000
    if "ESP32S2" in description:
        value=value+300000
    if "ESP32S3" in description:
        value=value+400000
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
        if bin_file[-4:]==".bin" and "_partitions.bin" not in bin_file:
            # create manifest file
            manifest_filename_prefix="manifest_"+''.join(e for e in dir_text.replace(" ","_").replace(".","_") if (e.isalnum() or e=="_"))+"_"+bin_file[:-4];
            download_path_forhtml=dir_path_forhtml+"/"+bin_file

            partitions_filename=bin_file.replace(".bin","_partitions.bin")
            if not os.path.isfile(os.path.join(dir2_path,partitions_filename)):
                partitions_filename="/suppl_dir/partitions_v2022.bin"
            else:
                partitions_filename=dir_path_forhtml+"/"+partitions_filename
            
            manifest_filename=manifest_filename_prefix+".json"
            manifest_path_forhtml="/"+manifest_dir+"/"+manifest_filename
            manifest_path=os.path.join(output_manifest_dir,manifest_filename)
            f_manifest=open(manifest_path,"w+")
            
            manifest_filename_noimprov = manifest_filename_prefix+"_noimprov.json"       
            manifest_path_forhtml_noimprov="/"+manifest_dir+"/"+manifest_filename_noimprov
            manifest_path_noimprov=os.path.join(output_manifest_dir,manifest_filename_noimprov)
            f_manifest_noimprov=open(manifest_path_noimprov,"w+")
            
            template_filename=""
            dict={}
            AddInfo=", 4MB Flash";
            AddInfoShort=", 4MB";
            ESPtype=""
            if isbinfile_esp32(bin_file):                    
                if ("ABCV41" in bin_file):
                    ESPtype="WLED Controller V41, ESP32, 5V, Audio Reactive (Mic. or Line-In)"
                    template_filename="./scripts/manifest_esp32_template.json"
                elif (("ABCV43" in bin_file) and ("DMX" in bin_file)):
                    ESPtype="WLED Controller V43, ESP32, 5-24V, Ethernet, DMX out on pin 32)"
                    template_filename="./scripts/manifest_esp32_template.json"
                elif ("ABCV43" in bin_file):
                    ESPtype="WLED Controller V43, ESP32, 5-24V, Ethernet, Audio Reactive (Mic. or Line-In)"
                    template_filename="./scripts/manifest_esp32_template.json"
                elif ("ABCV70" in bin_file):
                    ESPtype="WLED Controller mini V70, ESP32, 5-12V, Audio Reactive (Mic. or Line-In)"
                    template_filename="./scripts/manifest_esp32_template.json"
                elif ("ABCV73" in bin_file):
                    ESPtype="WLED Controller mini V73, ESP32, 5-24V, Audio Reactive (Mic. or Line-In)"
                    template_filename="./scripts/manifest_esp32_template.json"
                elif ("ABCV63" in bin_file):
                    ESPtype="WLED Shield V63, used with ESP32, 5-12V, Audio Reactive (Mic. or Line-In)"
                    template_filename="./scripts/manifest_esp32_template.json"
                elif isbinfile_esp32c3(bin_file):
                    ESPtype="ESP32-C3"
                    if(("_0.16." in bin_file) or ("_0.17." in bin_file) or ("_0.18." in bin_file) or ("_0.19." in bin_file) or ("_0.20." in bin_file)):
                        template_filename="./scripts/manifest_esp32c3_template_idf4tasmota.json"
                    else:
                        template_filename="./scripts/manifest_esp32c3_template.json"
                elif isbinfile_esp32s2(bin_file):
                    ESPtype="ESP32-S2"
                    if(("_0.16." in bin_file) or ("_0.17." in bin_file) or ("_0.18." in bin_file) or ("_0.19." in bin_file) or ("_0.20." in bin_file)):
                        template_filename="./scripts/manifest_esp32s2_template.json"
                    else:
                        template_filename="./scripts/manifest_esp32s2_template_idf4tasmota.json"
                elif isbinfile_esp32s3(bin_file):                         
                    ESPtype="ESP32-S3"
                    if(("_OPI" in bin_file) or ("_opi" in bin_file)):
                        if(("_0.16." in bin_file) or ("_0.17." in bin_file) or ("_0.18." in bin_file) or ("_0.19." in bin_file) or ("_0.20." in bin_file)):
                            template_filename="./scripts/manifest_esp32s3_opi_template.json"
                        else:
                            template_filename="./scripts/manifest_esp32s3_opi_template_idf4tasmota.json"
                    else:
                        if(("_0.16." in bin_file) or ("_0.17." in bin_file) or ("_0.18." in bin_file) or ("_0.19." in bin_file) or ("_0.20." in bin_file)):
                            template_filename="./scripts/manifest_esp32s3_template_idf4tasmota.json"
                        else:
                            template_filename="./scripts/manifest_esp32s3_template.json"
                    if ("_8MB" in bin_file):
                        if(("_OPI" in bin_file) or ("_opi" in bin_file)):
                            if(("_0.16." in bin_file) or ("_0.17." in bin_file) or ("_0.18." in bin_file) or ("_0.19." in bin_file) or ("_0.20." in bin_file)):
                                template_filename="./scripts/manifest_esp32s3_8MB_opi_template_idf4tasmota.json"
                            else:
                                template_filename="./scripts/manifest_esp32s3_8MB_opi_template.json"
                        else:
                            if(("_0.16." in bin_file) or ("_0.17." in bin_file) or ("_0.18." in bin_file) or ("_0.19." in bin_file) or ("_0.20." in bin_file)):
                                template_filename="./scripts/manifest_esp32s3_8MB_template_idf4tasmota.json"
                            else:
                                template_filename="./scripts/manifest_esp32s3_8MB_template.json"
                        AddInfo=", 8MB Flash";
                        AddInfoShort=", 8MB";
                    if ("_16MB" in bin_file):
                        if(("_OPI" in bin_file) or ("_opi" in bin_file)):
                            if(("_0.16." in bin_file) or ("_0.17." in bin_file) or ("_0.18." in bin_file) or ("_0.19." in bin_file) or ("_0.20." in bin_file)):
                                template_filename="./scripts/manifest_esp32s3_16MB_opi_template_idf4tasmota.json"
                            else:
                                template_filename="./scripts/manifest_esp32s3_16MB_opi_template.json"
                        else:
                            if(("_0.16." in bin_file) or ("_0.17." in bin_file) or ("_0.18." in bin_file) or ("_0.19." in bin_file) or ("_0.20." in bin_file)):
                                template_filename="./scripts/manifest_esp32s3_16MB_template_idf4tasmota.json"
                            else:
                                template_filename="./scripts/manifest_esp32s3_16MB_template.json"
                        AddInfo=", 16MB Flash";
                        AddInfoShort=", 16MB";
                    if ("_NOPSRAM" in bin_file):
                        AddInfo=AddInfo+", no PSRAM";
                        AddInfoShort=AddInfoShort;
                else:
                    ESPtype="ESP32"
                    template_filename="./scripts/manifest_esp32_template.json"
                    if ("_ETH" in bin_file) or ("_Ethernet" in bin_file):
                        AddInfo=AddInfo+", Ethernet";
                        AddInfoShort= AddInfoShort+", Ethernet";
            else:
                if ("ABCV31" in bin_file):
                    ESPtype="WLED Controller V31, ESP8266, 5V"
                    template_filename="./scripts/manifest_esp8266_template.json"
                elif ("ABCV63" in bin_file):
                    ESPtype="WLED Shield V63, used with ESP8266, 5-12V"
                    template_filename="./scripts/manifest_esp8266_template.json"
                else:
                    ESPtype="ESP8266"
                    template_filename="./scripts/manifest_esp8266_template.json"
                    AddInfo=", 4MB Flash: D1 mini etc.";
                    AddInfoShort=", 4MB";
                    if ("_1MB" in bin_file) or ("_ESP01" in bin_file):
                        AddInfo=", 1MB Flash";
                        AddInfoShort=", 1MB";
                    if ("_2MB" in bin_file) or ("_ESP02" in bin_file):
                        AddInfo=", 2MB Flash";
                        AddInfoShort=", 1MB";
            
            if ("WLEDSR_" in bin_file[0:7]):
                if (("_S." in bin_file) or ("_S_" in bin_file)):
                    AddInfo=AddInfo+", S: Alexa/Infrared/MQTT/Loxone disabled, no Usermods included";
                    AddInfoShort=AddInfoShort+", S: Alexa/IR etc. disabled";
                if (("_M." in bin_file) or ("_M_" in bin_file)):
                    AddInfo=AddInfo+", M: Alexa/MQTT/Loxone disabled, IR enabled, Usermods incl: Temp, AutoSave, 4-L Display, Rotary encoder";
                    AddInfoShort=AddInfoShort+", M: some usermods";
                if (("_Sext." in bin_file) or ("_Sext_" in bin_file)):
                    AddInfo=AddInfo+", S++: Ethernet, Alexa/Infrared/MQTT/Loxone enabled";
                    AddInfoShort=AddInfoShort+", S++: Ethernet";
                if (("_Mext." in bin_file) or ("_Mext_" in bin_file)):
                    AddInfo=AddInfo+", M++: Ethernet, Alexa/Infrared/MQTT/Loxone enabled, Usermods: Temp, AutoSave, 4-L Display, Rotary encoder";
                    AddInfoShort=AddInfoShort+", M++: Ethernet";
                    
            elif ("WLEDMM_" in bin_file[0:7]):
                if (("_S." in bin_file) or ("_S_" in bin_file)):
                    AddInfo=AddInfo+", S: Audioreactive, no other Usermods included";
                    AddInfoShort=AddInfoShort+", S: Audioreactive";
                if (("_M." in bin_file) or ("_M_" in bin_file)):
                    AddInfo=AddInfo+", M: Audioreactive, Usermods incl: Temp, AutoSave, 4-L Display, Rotary encoder";
                    AddInfoShort=AddInfoShort+", M: some usermods";
                if (("_XL." in bin_file) or ("_XL_" in bin_file)):
                    AddInfo=AddInfo+", XL: Audioreactive, Lots of usermods included";
                    AddInfoShort=AddInfoShort+", XL: lots of usermods";
                if ("_V4_" in bin_file):
                    AddInfo=AddInfo+", ESPIDF V4 based (fixes reboot issues)";
                    AddInfoShort=AddInfoShort+", ESPIDF4";
            
            else:
                if(("_OPI" in bin_file) or ("_opi" in bin_file)):
                    AddInfo=AddInfo+", OPI FLASH";
                if ("_PIR" in bin_file):
                    AddInfo=AddInfo+", PIR Usermod incl.";
                    AddInfoShort=AddInfoShort+", PIR";
                if ("_MULTIRELAY" in bin_file):
                    AddInfo=AddInfo+", Multirelay Usermod incl.";
                    AddInfoShort=AddInfoShort+", Multirelay";
                if ("_Staircase" in bin_file):
                    AddInfo=AddInfo+", Usermod Animated Staircase included";
                    AddInfoShort=AddInfoShort+", Staircase";
                if ("_WIFIFIX" in bin_file):
                    AddInfo=AddInfo+", Lolin WiFiFix for some C3 mini V1.0.0";
                    AddInfoShort=AddInfoShort+", WIFIFIX";
                if ("_AE" in bin_file) or ("_withAlexa" in bin_file):
                    AddInfo=AddInfo+", Alexa enabled";
                    AddInfoShort=AddInfoShort+", Alexa";
                if ((("_0.16" in bin_file) or ("_0.15" in bin_file)) and (("_NOARE") not in bin_file)  and (("ESP8266") not in bin_file) and (not isbinfile_esp32c3(bin_file))):
                    AddInfo=AddInfo+", with Audio reactive Usermod";
                    AddInfoShort=AddInfoShort+", Audio reactive";
                elif ("_ARE" in bin_file) or ("_AR." in bin_file) or ("_AR_" in bin_file) or ("_audioreactive" in bin_file):
                    AddInfo=AddInfo+", with Audio reactive Usermod";
                    AddInfoShort=AddInfoShort+", Audio reactive";
                if ("_AHI" in bin_file):
                    AddInfo=AddInfo+", APA102 2MHz + Alexa/Hue/Infrared enabled";
                    AddInfoShort=AddInfoShort+", Alexa+Hue+IR";
                if ("_ABHI" in bin_file):
                    AddInfo=AddInfo+", APA102 2MHz + Alexa/Blink/Hue/Infrared enabled";
                    AddInfoShort=AddInfoShort+", Alexa+Blink+Hue+IR";
                if ("_APA102FIX2MHZ" in bin_file):
                    AddInfo=AddInfo+", APA102 2MHz";
                    AddInfoShort=AddInfoShort+", APA102 2MHz";
                if ("_v41" in bin_file):
                    AddInfo=AddInfo+", LEDPIN=16, DigMic = Generic I2S";
                    AddInfoShort=AddInfoShort+", I2S Mic";
                if ("_OB" in bin_file):
                    AddInfo=AddInfo+", original Build";
                    AddInfoShort=AddInfoShort+", original Build";
                if ("_OB" in bin_file) and ("SR_" in bin_file):
                    AddInfo=AddInfo+", Alexa+Hue+IR disabled";
                    AddInfoShort=AddInfoShort+"";
                if ("_MQTT" in bin_file):
                    AddInfo=AddInfo+", MQTT enabled";
                    AddInfoShort=AddInfoShort+", MQTT";
                if ("_MDEVMAX" in bin_file) or (("WLEDMM_" in bin_file) and (("_max" in bin_file) or  ("_M.bin" in bin_file) or  ("_M_" in bin_file))):
                    AddInfo=AddInfo+", M: mods included: audio reactive, games, weather, custom effects, mpu6050 + other improvements";
                    AddInfoShort=AddInfoShort+", M: many mods included";
                if ("WLEDMM_" in bin_file) and ("_S.bin" in bin_file):
                    AddInfo=AddInfo+", S: mods included: audio reactive";
                    AddInfoShort=AddInfoShort+", S: some mods included";
                if ("WLEDMM_" in bin_file) and ("_XL.bin" in bin_file):
                    AddInfo=AddInfo+", XL: almost all mods included";
                    AddInfoShort=AddInfoShort+", XL: almost all mods";
                if (("WLEDSR_" in bin_file) and ("_max" in bin_file)):
                    AddInfo=AddInfo+", some additional mods included";
                    AddInfoShort=AddInfoShort+", some additional mods";
                if (("WLEDSR_" in bin_file) and ("_M" in bin_file)):
                    AddInfo=AddInfo+", M: some additional mods included: temp Sensor, 4-L Display, rotary encoder, auto Save";
                    AddInfoShort=AddInfoShort+", M: some additional mods";
                if (("WLEDSR_" in bin_file) and ("_S" in bin_file)):
                    AddInfo=AddInfo+", S: no additional mods";
                    AddInfoShort=AddInfoShort+", S: no additional mods";
                if ("_DIGIN" in bin_file):
                    AddInfo=AddInfo+", digital line-in support";
                    AddInfoShort=AddInfoShort+", line-in";
                if ("_HSDIGIN" in bin_file):
                    AddInfo=AddInfo+", high sense digital line-in support";
                    AddInfoShort=AddInfoShort+", line-in";
                if ("_compat" in bin_file):
                    AddInfo=AddInfo+", COMPAT: better for some ESP8266 boards";
                    AddInfoShort=AddInfoShort+", compat.";
                if ("_160" in bin_file):
                    AddInfo=AddInfo+", overclock to 160 MHz";
                    AddInfoShort=AddInfoShort+", overclocked";
                if ("_WROVER" in bin_file):
                    AddInfo=AddInfo+", for WROVER: with PSRAM";
                    AddInfoShort=AddInfoShort+", wrover";
                if (("_V4" in bin_file) and (("0.14." in bin_file) or ("0.15." in bin_file))):
                    AddInfo=AddInfo+", ESPIDF V4 based";
                    AddInfoShort=AddInfoShort+", IDF V4";
            
            # common
            if ("_debug" in bin_file):
                AddInfo=AddInfo+", DEBUG enabled"
                AddInfoShort=AddInfoShort+", DEBUG enabled";
            if ("_micdebug" in bin_file):
                AddInfo=AddInfo+", Microphone debug enabled";
                AddInfoShort=AddInfoShort+", Microphone debug";
            
            if ("ABCV" in bin_file):
                dict["ADDINFO"]="";
                AddInfo="";
            else:
                dict["ADDINFO"]=AddInfoShort;
                AddInfo=" ("+AddInfo[2:]+")";
            dict["VERSION"]=dir_text;    
            dict["BINFILE"]=dir_path_forhtml+"/"+bin_file; 
            dict["IMPROVWAITTIME"] = "10";
            dict["PARTITIONSFILENAME"] = partitions_filename;
            f_template=open(template_filename, "r")
            template=string.Template(f_template.read())
            f_manifest.write(template.substitute(dict));
            f_manifest.close()
            
            dict["IMPROVWAITTIME"] = "0";
            f_manifest_noimprov.write(template.substitute(dict));
            f_manifest_noimprov.close()
            
            #html_list=html_list+(bin_file+" "+manifest_path_forhtml+ " "+ ESPtype +" ("+AddInfo[2:]+")" + "\n")
            html_list_array.append("<option data-manifest_file=\""+manifest_path_forhtml+ "\" data-manifest_file_noimprov=\"" +manifest_path_forhtml_noimprov + "\" data-download_file=\"" +download_path_forhtml+ "\">"+ ESPtype +AddInfo+ "</option>")
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
                dir2_text=dir1_text.replace("for ABC WLED Controllers","for ABC! WLED controllers (shop.myhome-control.de, wled.shop)") + ": " + dir2.replace("_"," ")
                html_list = html_list + proceed_dir(dir2_path, dir2_text, "/"+bin_dir+"/"+dir1+"/"+dir2)
                
f_template=open("./scripts/index_template.html", "r")
template=string.Template(f_template.read())
f_template.close()
dict={}
dict["HTMLLIST"]=html_list
dict["WEBTOOLMODULE"]='https://unpkg.com/esp-web-tools@9.4.3/dist/web/install-button.js?module'
f_index= open(os.path.join(output_dir,"index.html"),"w+")
f_index.write(template.substitute(dict))
f_index.close()

f_template=open("./scripts/index_template.html", "r")
template=string.Template(f_template.read())
f_template.close()
f_index= open(os.path.join(output_dir,"oldmethod.html"),"w+")
dict["WEBTOOLMODULE"]='https://unpkg.com/esp-web-tools@8.0.6/dist/web/install-button.js?module'
f_index.write(template.substitute(dict))
f_index.close()
