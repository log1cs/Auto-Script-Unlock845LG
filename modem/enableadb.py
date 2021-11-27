#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) B.Kerler 2020-2021 under MIT license
# If you use my code, make sure you refer to my name
# If you want to use in a commercial product, ask me before integrating it
import time
from telnetlib import Telnet
import serial
import serial.tools.list_ports
import argparse
import requests
import hashlib
from diag import qcdiag
import usb.core
from enum import Enum
import crypt
from sierrakeygen import SierraKeygen

try:
    from Library.utils import LogBase
except Exception as e:
    import os,sys,inspect
    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)
    from Library.utils import LogBase

class vendor(Enum):
    sierra = 0x1199
    quectel = 0x2c7c
    zte = 0x19d2
    telit = 0x413c
    netgear = 0x0846

class deviceclass:
    vid=0
    pid=0
    def __init__(self,vid,pid):
        self.vid=vid
        self.pid=pid

class connection:
    def __init__(self, port=""):
        self.serial = None
        self.tn = None
        self.connected = False
        if port == "":
            port = self.detect(port)
        if port != "":
            self.serial = serial.Serial(port=port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)
            self.connected = self.serial.is_open

    def waitforusb(self,vid,pid):
        timeout = 0
        while timeout < 10:
            for device in self.detectusbdevices():
                if device.vid == vid:
                    if device.pid == pid:
                        return True
            time.sleep(1)
            timeout += 1
        return False

    def websend(self,url):
        headers = {'Referer': 'http://192.168.0.1/index.html', 'Accept-Charset': 'UTF-8'}
        r = requests.get(url, headers=headers)
        if b"FACTORY:ok" in r.content or b"success" in r.content:
            print(f"Detected a ZTE in web mode .... switching mode success (convert back by sending \"AT+ZCDRUN=F\" via AT port)")
            return self.waitforusb(vendor.zte.value,0x0016)
        return False

    def getserialports(self):
        return [port for port in serial.tools.list_ports.comports()]

    def detectusbdevices(self):
        dev = usb.core.find(find_all=True)
        ids=[deviceclass(cfg.idVendor,cfg.idProduct) for cfg in dev]
        return ids

    def detect(self, port):
        atvendortable={
            0x1199:["Sierra Wireless",3],
            0x2c7c:["Quectel",3],
            0x19d2:["ZTE",2],
            0x413c:["Telit",3],
            0x0846:["Netgear",2],
            0x04E8:["Samsung", -1]
        }
        mode="Unknown"
        for device in self.detectusbdevices():
            if device.vid==vendor.zte.value:
                if device.pid==0x0016:
                    print(f"Detected a {atvendortable[device.vid][0]} device with pid {hex(device.pid)} in AT mode")
                    mode="AT"
                    break
                elif device.pid==0x1403:
                    print(f"Detected a {atvendortable[device.vid][0]} device with pid {hex(device.pid)} in Web mode")
                    mode="Web"
                    url = 'http://192.168.0.1/goform/goform_set_cmd_process?goformId=USB_MODE_SWITCH&usb_mode=6'
                    if self.websend(url):
                        print("Successfully enabled adb.")
                    break
            elif device.vid==vendor.netgear.value:
                try:
                    # vid 0846, netgear mr1100, mr5100
                    self.tn = Telnet("192.168.1.1", 5510, 5)
                    self.connected = True
                except:
                    self.connected = False
        if mode=="AT" or mode=="Unknown":
            for port in self.getserialports():
                if port.vid in atvendortable:
                    portid = port.location[-1:]
                    if int(portid) == atvendortable[port.vid][1]:
                        print(f"Detected a {atvendortable[port.vid][0]} at interface at: " + port.device)
                        return port.device
        return ""

    def readreply(self):
        info = []
        timeout=0
        if self.serial is not None:
            while True:
                tmp = self.serial.readline().decode('utf-8').replace('\r', '').replace('\n', '')
                if "OK" in tmp:
                    info.append(tmp)
                    return info
                elif "ERROR" in tmp:
                    return -1
                if tmp!="":
                    info.append(tmp)
                else:
                    timeout+=1
                    if timeout==20:
                        break
        return info

    def send(self, cmd):
        if self.tn is not None:
            self.tn.write(bytes(cmd + "\r", 'utf-8'))
            time.sleep(0.05)
            data = ""
            while True:
                tmp = self.tn.read_eager()
                if tmp != b"":
                    data += tmp.strip().decode('utf-8')
                else:
                    break
            if "ERROR" in data:
                return -1
            return data.split("\r\n")
        elif self.serial is not None:
            self.serial.write(bytes(cmd + "\r", 'utf-8'))
            time.sleep(0.05)
            resp=self.readreply()
            return resp

    def close(self):
        if self.tn is not None:
            self.tn.close()
            self.connected = False
        if self.serial is not None:
            self.serial.close()
            self.connected = False

    def ati(self):
        data={}
        info = self.send("ATI")
        if info != -1:
            for line in info:
                if "Revision" in line:
                    data["revision"] = line.split(":")[1].strip()
                if "Model" in line:
                    data["model"] = line.split(":")[1].strip()
                if "Quectel" in line:
                    data["vendor"] = "Quectel"
                if "Manufacturer" in line:
                    data["manufacturer"]=line.split(":")[1].strip()
                    if "Sierra Wireless" in data["manufacturer"]:
                        data["vendor"]="Sierra Wireless"
                    elif "ZTE CORPORATION" in data["manufacturer"]:
                        data["vendor"]="ZTE"
                    elif "SIMCOM INCORPORATED" in data["manufacturer"]:
                        data["vendor"]="Simcom"
                    elif "Alcatel" in data["manufacturer"]:
                        data["vendor"]="Alcatel"
                    elif "Netgear" in data["manufacturer"]:
                        data["vendor"]="Netgear"
                    elif "SAMSUNG" in data["manufacturer"]:
                        data["vendor"]="Samsung"
        info = self.send("AT+CGMI")
        if info!=-1:
            for line in info:
                if "Quectel" in line:
                    data["vendor"] = "Quectel"
                    break
                elif "Fibucom" in line:
                    data["vendor"]="Fibucom"
                    break
                elif "Netgear" in line:
                    data["vendor"]="Netgear"
                    break
                elif "SAMSUNG" in line:
                    data["vendor"]="Samsung"
                    break
        info = self.send("AT+CGMR")
        if info!=-1:
            if len(info)>1:
                data["model"]=info[1]
        return data

class adbtools(metaclass=LogBase):
    def sendcmd(self, tn,cmd):
        tn.write(bytes(cmd,'utf-8')+b"\n")
        time.sleep(0.05)
        return tn.read_eager().strip().decode('utf-8')

    def run(self, args):
        port = args.port
        cn = connection(port)
        if cn.connected:
            info=cn.ati()
            if "vendor" in info:
                if info["vendor"]=="Sierra Wireless" or info["vendor"]=="Netgear":
                    print("Sending at switch command")
                    kg=SierraKeygen(cn)
                    if kg.openlock():
                        if cn.send('AT!CUSTOM="ADBENABLE",1\r')==-1:
                            print("Error on sending adb enable command.")
                            kg.openlock()
                        if cn.send('AT!CUSTOM="TELNETENABLE",1\r')!=-1:
                                time.sleep(5)
                                tn = Telnet("192.168.1.1", 23, 15)
                                tn.write(b"adbd &\r\n")
                                info = tn.read_eager()
                                print(info)
                                print("Enabled adb via telnet")
                        else:
                            print("Error on sending telnet enable command.")
                        if kg.openlock():
                            if info["vendor"] == "Netgear":
                                print("Enabling new port config")
                                if cn.send("AT!UDPID=68E2"):
                                    print("Successfully enabled PID 68E2")
                elif info["vendor"]=="Quectel":
                    print("Sending at switch command")
                    salt=cn.send("AT+QADBKEY?\r")
                    if salt!=-1:
                        if len(salt)>1:
                            salt=salt[1]
                        code = crypt.crypt("SH_adb_quectel", "$1$" + salt)
                        code = code[12:]
                        cn.send("AT+QADBKEY=\"%s\"\r" % code)
                    if cn.send("AT+QCFG=\"usbcfg\",0x2C7C,0x125,1,1,1,1,1,1,0\r")==-1:
                        if cn.send("AT+QLINUXCMD=\"adbd\"")!=-1: #echo test > /dev/ttyGS0
                            print("Success enabling adb")
                    else:
                        print("Success enabling adb")
                        print("In order to disable adb, send AT+QCFG=\"usbcfg\",0x2C7C,0x125,1,1,1,1,1,0,0")
                elif info["vendor"]=="ZTE":
                    print("Sending switch command via diag")
                    if cn.send("AT+ZMODE=1")!=-1:
                        print("Success enabling adb")
                    else:
                        interface = 0
                        diag = qcdiag(loglevel=self.__logger.level, portconfig=[[0x19d2, 0x0016, interface]])
                        if diag.connect():
                            res = diag.send(b"\x4B\xA3\x06\x00")
                            if res[0]==0x4B:
                                challenge=res[4:4+8]
                                response=hashlib.md5(challenge).digest()
                                res = diag.send(b"\x4B\xA3\x07\x00"+response)
                                if res[0]==0x4B:
                                    if res[3]==0x00:
                                        print("Auth success")
                            res=diag.send(b"\x41" + b"\x30\x30\x30\x30\x30\x30")
                            if res[1]==0x01:
                                print("SPC success")
                            sp=b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFE"
                            res = diag.send(b"\x46" + sp)
                            if res[0] == 0x46 and res[1]==0x01:
                                print("SP success")
                            else:
                                res = diag.send(b"\x25" + sp)
                                if res[0]==0x46 and res[1]==0x01:
                                    print("SP success")
                            res = diag.send(b"\x4B\xFA\x0B\x00\x01") #Enable adb serial
                            if res[0]!=0x13:
                                print("Success enabling adb serial")
                            res = diag.send(b"\x4B\x5D\x05\x00") #Operate ADB
                            if res[0]!=0x13:
                                print("Success enabling adb")
                            diag.disconnect()
                elif info["vendor"]=="Simcom":
                    print("Sending at switch command")
                    # Simcom7600
                    if cn.send("AT+CUSBADB=1,1")!=-1:
                        print("Success enabling adb")
                elif info["vendor"]=="Fibocom":
                    print("Sending at switch command")
                    # FibocomL718:
                    if cn.send("AT+ADBDEBUG=1")!=-1:
                        print("Success enabling adb")
                elif info["vendor"]=="Alcatel":
                    print("Send scsi switch command")
                    print("Run \"sudo sg_raw /dev/sg0 16 f9 00 00 00 00 00 00 00 00 00 00 00 00 00 00 -v\" to enable adb")
                elif info["vendor"]=="Samsung":
                    if cn.send("AT+USBMODEM=1"):
                        print("Success enabling adb")
                    elif cn.send("AT+SYSSCOPE=1,0,0"):
                        print("Success enabling adb")

        cn.close()

def main():
    version = "1.1"
    info = 'Modem Gimme-ADB ' + version + ' (c) B. Kerler 2020-2021'
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=info)
    parser.add_argument(
        '-port', '-p',
        help='use com port for at',
        default="")
    parser.add_argument(
        '-logfile', '-l',
        help='use logfile for debug log',
        default="")
    args = parser.parse_args()
    ad=adbtools()
    ad.run(args)

if __name__=="__main__":
    main()

