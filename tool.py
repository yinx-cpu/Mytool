import os, time, base64, urllib.request, requests, socket, random

path = "/sdcard/Download/loginlog.txt"
now = strtime = time.strftime("%Y/%m/%d %H:%M:%S")
downapk = "/sdcard/Mytool/download/apk/"
downzip = "/sdcard/Mytool/download/zip/"
savea = (downapk + now + ".apk")
savez = (downzip + now + ".zip")

if not os.path.exists("/sdcard/Mytool/base64/"):
    os.makedirs("/sdcard/Mytool/base64/")
if not os.path.exists("/sdcard/Mytool/web/"):
    os.makedirs("/sdcard/Mytool/web/")
if not os.path.exists("/sdcard/Mytool/base64/baseen.txt"):
    with open("/sdcard/Mytool/base64/baseen.txt", "w", encoding="utf-8") as f:
        pass
if not os.path.exists("/sdcard/Mytool/base64/basede.txt"):
    with open("/sdcard/Mytool/base64/basede.txt", "w", encoding="utf-8") as f:
        pass
if not os.path.exists("/sdcard/Mytool/download/apk/"):
    os.makedirs("/sdcard/Mytool/download/apk/")
if not os.path.exists("/sdcard/Mytool/download/apk/"):
    os.makedirs("/sdcard/Mytool/download/apk/")
if not os.path.exists("/sdcard/Mytool/download/zip/"):
    os.makedirs("/sdcard/Mytool/download/zip/")
if not os.path.exists("/sdcard/Mytool/Unzip/"):
    os.makedirs("/sdcard/Mytool/Unzip/")



def logincode():
    return str(random.randint(100000, 999999))

def local():
    code = logincode()
    print(f"本次验证码：{code}")
    
    user_input = input("\n请输入验证码(防机器人)：")
    if user_input == code:
        print("验证成功")
        time.sleep(1)
    else:
        print("验证失败")
        time.sleep(5)
        exit()


os.system("clear")
if not os.path.exists(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("首次运行时间："+strtime)
        print(f"已写入此次运行时间到{path}\n" * 3)
        time.sleep(1)
else:
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n运行时间："+strtime)
        print(f"已写入此次运行时间到{path}\n" * 3)
        time.sleep(1)

def b64_encode(s):
    return base64.b64encode(s.encode("utf-8")).decode("utf-8")

def b64_decode(s):
    return base64.b64decode(s).decode("utf-8", errors="ignore")

def ourl(url):
    os.system(f'xdg-open "{url}"')

def c():
    os.system("clear")

time.sleep(1)
os.system("clear")
local()
os.system("clear")

while True:
    now = time.strftime("%Y/%m/%d %H:%M:%S")
    print("当前时间: ",now)
    time.sleep(0.000000000000001)
    
    
    
    
    print("----------------By.MY----------------")
    print("当前版本仅供开发者自行使用\n如若开发者做出违法行为，与工具开发者本人无关！")
    print("---------介绍---------")
    print("本工具由个人开发，并非集体开发\n如若有人恶意使用本工具做出违法犯罪行为\n与本人和本工具无关")
    print("---------功能区---------")
    print("1.base64加密/解密 2.获取网页源代码 3.各种网页")
    print("4.下载文件 5.学习编程 6.网速")
    print("7.更多功能 8.关于 9.退出")
    home = input()

    if home == "1":
        while True:
            os.system("clear")
            base = input("1.加密 2.解密\n")
            if base == "1":
                text = input("输入你要加密内容的路径:")
                bname = input("输入加密后输出的文件的名字: ")
                with open(text, "r", encoding="utf-8") as f:
                    enc = f.read()
                en = b64_encode(enc)
                with open("/sdcard/base64/baseen.txt", "w", encoding="utf-8") as f:
                    f.write(en)
                print(f"任务已完成\n内容已输出到内部储存mytool/base64/{bname}.txt")
            elif base == "2":
                text = input("输入你要解密内容的路径:")
                bname = input("输入解密后输出的文件的名字: ")
                if text:
                    with open(text, "r", encoding="utf-8") as f:
                        dec = f.read()
                    de = b64_decode(dec)
                    with open("/sdcard/base64/basede.txt", "w", encoding="utf-8") as f:
                        f.write(de)
                        f.write(de)
                    print(f"任务已完成\n内容已输出到mytool/base64/{bname}.txt")
                    input("按回车键返回")
                if not text:
                    print("请输入路径！\n请输入路径！\n请输入路径！")
                    time.sleep(1)
            else:
                break

    elif home == "2":
        while True:
            os.system("clear")
            surl = input("输入网址(不要携带http://  https://前缀):")
            if surl:
                url = ("http://" + surl)
                rename = input("输入名称:\n")
                res = requests.get(url, headers={"User-Agent":"Mozilla/5.0 (Android)"})
                with open(f"/sdcard/Mytool/web/{rename}.html","w",encoding="utf-8") as f:
                    f.write(res.text)
                print("任务已完成，文件已输出到Mytool/web目录下")
                time.sleep(3)
                break
            else:
                break
    elif home == "3":
        while True:
            os.system("clear")
            print("1.懂得都懂 2.刷机 3.海量视频资源网址 \n")
            third = input("输入以上数字跳转\n")
            if third == "1":
                sec = input("1.软件网站 2.在线网站\n")
                if sec == "1":
                    ourl("http://520521.com")
                if sec == "2":
                    print("https://520621.com")
                    time.sleep(3)
                else:
                    break
            elif third == "2":
                while True:
                    os.system("clear")
                    print("目前只有这几个 如果有更多资源网站请通过主页面的关于联系作者")
                    print("1.miui官方刷机包 2.一加(包括真我和oppo) \n3.其他(萤火虫资源网) 4.全系列线刷救砖合集(萤火虫资源网) 5.返回\n")
                    bootloader = input()
                    if bootloader == "1":
                        print("1.澎湃 2.miui 3.回车返回上级")
                        hypermiui = input()
                        if hypermiui == "1":
                            ourl("http://hyperos.fans")
                        elif hypermiui == "2":
                            miuii = input("1.主 2.备用\n")
                            if miuii == "1":
                                ourl("http://xiaomirom.com")
                            elif miuii == "2":
                                ourl("http://roms.miuier.com")
                            else:
                                break
                    elif bootloader == "2":
                        ourl("http://yun.daxiaamu.com")
                    elif bootloader == "3":
                        ourl("https://www.yhcres.top")
                    elif bootloader == "4":
                        ourl("https://www.yhcres.top/d/public/%E6%9C%80%E6%96%B0%E5%85%A8%E7%B3%BB%E5%88%97%E7%BA%BF%E5%88%B7%E6%95%91%E7%A0%96%E8%B5%84%E6%96%99%E9%9B%86%E5%90%88%E5%A4%A7%E5%85%A8%20190416.xls?sign=ssXpXHUr9KmAn9Op3kAouFOrvZTLtBgLLQkvoVn9uvo=:1775912346")
                    else:
                        break
            elif third == "3":
                ourl("http://www.hainatv.net")
            else:
                break
    elif home == "4":
        while True:
            os.system("clear")
            zipapk = input("下载:\n1.apk    2.压缩包    |3.返回|\n")
            if zipapk == "1":
                urldownload = input("输入下载链接:\n")
                
                urllib.request.urlretrieve(urldownload, savea)
                print(f"已下载到{savea}")
                time.sleep(3)
            
            if zipapk == "2":
                urldownload = input("输入下载链接:\n")
                
                urllib.request.urlretrieve(urldownload, savez)
                print(f"已下载到{savez}")
                print("是否需要解压？\n1.是(默认删除原文件) 2.否")
                uz = input()
                if uz == "1":
                    zpath = input("请输入zip文件路径：")
                    topath = input("解压到(默认Mytool)：") or "/sdcsrd/Mytool/Unzip/"
                    if os.path.exists(zpath):
                        os.system(f"unzip -o '{zpath}' -d '{topath}'")
                        print("解压完成")
                        print("正在删除文件......")
                        os.system(f"rm -rf {zpath}")
                    else:
                        print("错误：文件不存在")
                    time.sleep(3)
                else:
                    break
            if zipapk == "3":
                break
    elif home == "5":
        while True:
            c()
            print("1.软件 2.网页 |按回车返回|")
            cjp = input()
            if cjp == "1":
                urld = ("https://codetome.cn/downloads/codetome.apk")
                save = ("/sdcard/Mytool/download/apk/learn.apk")
                urllib.request.urlretrieve(urld, save)
                shutil.copy(save, "/sdcard/Download/")
                print("文件已在download目录下")
                time.sleep(3)
                c()
            elif cjp == "2":
                print("1.codecombat 2.screeps 3.coding\n4.程序员升职记(Human Resource Machine) 5.codehunt")
                fivth = input()
                if fivth == "1":
                    ourl("https://codecombat.cn/")
                    c()
                elif fivth == "2":
                    ourl("https://store.screeps.com/zh-CN")
                    c()
                elif fivth == "3":
                    ourl("https://codinggame.com/start")
                    c()
                elif fivth == "4":
                    ourl("https://tomorrowcorporation.com")
                    c()
                elif fivth == "5":
                    ourl("https://codehunt.com")
                    c()
                else:
                    break
            else:
                break
    elif home == "6":
        while True:
            print("输入选择项")
            sixird = input("1.测试 2.返回\n")
            if sixird == "1":
                print("测试下载速度...")
                try:
                    url = "http://speed.hetzner.de/10MB.bin"
                    st = time.time()
                    tmp_file = os.path.join("./", "tmp_speed.tmp")
                    urllib.request.urlretrieve(url, tmp_file)
                    cost = time.time() - st
                    speed = 10 / cost
                    print(f"下载速度：{speed:.2f} MB/s")
                    os.remove(tmp_file)
                except Exception as e:
                    print(f"测速失败：{e}")
                time.sleep(2)
            elif sixird == "2":
                break
    
    elif home == "7":
        while True:
            print("输入选择项")
            sevenird = input("1.设备信息 2.解压文件 3.返回\n")
            if sevenird == "1":
                print("===== 设备信息 =====")
                os.system("uname -a")
                print("===== 内存信息 =====")
                os.system("free -h")
                print("===== 磁盘信息 =====")
                os.system("df -h")
                input("\n回车返回")
            elif sevenird == "2":
                zpath = input("请输入zip文件路径：")
                topath = input("解压到(默认Mytool)：") or "/sdcsrd/Mytool/Unzip/"
                if os.path.exists(zpath):
                    os.system(f"unzip -o '{zpath}' -d '{topath}'")
                    print("解压完成")
                    print("正在删除文件......")
                    os.system(f"rm -rf {zpath}")
                else:
                    print("错误：文件不存在")
                time.sleep(3)
            elif sevenird == "3":
                break
    elif home == "8":
        while True:
            print("\033c")
            print("该工具仅为个人开发\n作者联系方式↓(快手网页 TG应用)")
            print("目前只有两个平台！")
            eightird = input("1.快手 2.TG(需vpn) 3.返回\n")
            if eightird == "1":
                ourl("https://v.kuaishou.com/KhI3VnPa")
            elif eightird == "2":
                ourl("https://t.me/Myo_tool")
            elif eightird == "3":
                break
    elif home == "9":
        print("\033c")
        exit()
    else:
        print("请输入1-9！")
        time.sleep(0.5)
    os.system("clear")