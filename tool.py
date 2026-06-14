import os
import time
import base64
import urllib.request
import requests
import shutil
import random
import hashlib
import binascii
import codecs
import zipfile
import socket

LOG_PATH = "storage/emulated/10/Android/data/coding.yu.pythoncompiler.new/loginlog.txt"
BASE_DIR = "storage/emulated/10/Android/data/coding.yu.pythoncompiler.new/Mytool"
BASE64_DIR = os.path.join(BASE_DIR, "base64")
WEB_DIR = os.path.join(BASE_DIR, "web")
APK_DIR = os.path.join(BASE_DIR, "downloadapk")
ZIP_DIR = os.path.join(BASE_DIR, "downloadzip")
UNZIP_DIR = os.path.join(BASE_DIR, "Unzip")
ENCRYPT_DIR = os.path.join(BASE_DIR, "加密解密")

# 创建各算法子文件夹
for algo in ["Base64", "MD5", "SHA1", "SHA256", "SHA512", "Hex", "ROT13", "Composite"]:
    os.makedirs(os.path.join(ENCRYPT_DIR, algo), exist_ok=True)

for d in [BASE64_DIR, WEB_DIR, APK_DIR, ZIP_DIR, UNZIP_DIR]:
    os.makedirs(d, exist_ok=True)

for fname in ["baseen.txt", "basede.txt"]:
    fpath = os.path.join(BASE64_DIR, fname)
    if not os.path.exists(fpath):
        open(fpath, "w", encoding="utf-8").close()

def check_command(cmd):
    return shutil.which(cmd) is not None

HAS_GCC = check_command("gcc") or check_command("clang")
HAS_JAVAC = check_command("javac")
HAS_JAVA = check_command("java")
HAS_NODE = check_command("node")

def clear():
    os.system("clear")

def open_url(url):
    os.system(f'xdg-open {url}')

def b64_encode(s):
    return base64.b64encode(s.encode("utf-8")).decode("utf-8")

def b64_decode(s):
    return base64.b64decode(s).decode("utf-8", errors="ignore")

def get_time_str():
    return time.strftime("%Y%m%d %H%M%S")

def get_safe_filename_time():
    return time.strftime("%Y-%m-%d_%H-%M-%S")

def log_runtime():
    now = get_time_str()
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"运行时间：{now}")

def repeat_b64_encode(text: str, times: int) -> str:
    result = text
    for _ in range(times):
        result = base64.b64encode(result.encode("utf-8")).decode("utf-8")
    return result

def repeat_b64_decode(text: str, times: int) -> str:
    result = text
    for i in range(times):
        try:
            result = base64.b64decode(result).decode("utf-8", errors="ignore")
        except Exception as e:
            print(f"第{i+1}次解码失败：{e}")
            return None
    return result

# ---------- 纯英文加密函数 ----------
def caesar_encrypt(text: str, shift: int) -> str:
    result = []
    for ch in text:
        if ch.isupper():
            result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
        elif ch.islower():
            result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
        else:
            result.append(ch)
    return ''.join(result)

def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)

def atbash_encrypt(text: str) -> str:
    result = []
    for ch in text:
        if ch.isupper():
            result.append(chr(ord('Z') - (ord(ch) - ord('A'))))
        elif ch.islower():
            result.append(chr(ord('z') - (ord(ch) - ord('a'))))
        else:
            result.append(ch)
    return ''.join(result)

def composite_encrypt(text: str, method: str, shift: int = 3) -> str:
    if method == "caesar":
        step1 = caesar_encrypt(text, shift)
    elif method == "atbash":
        step1 = atbash_encrypt(text)
    else:
        step1 = text
    step2 = codecs.encode(step1, 'rot_13')
    return step2

def composite_decrypt(text: str, method: str, shift: int = 3) -> str:
    step1 = codecs.decode(text, 'rot_13')
    if method == "caesar":
        step2 = caesar_decrypt(step1, shift)
    elif method == "atbash":
        step2 = atbash_encrypt(step1)
    else:
        step2 = step1
    return step2

# ================== 加密解密工具 ==================
def encrypt_decrypt_tool():
    while True:
        clear()
        print("=== 加密解密工具 ===")
        print("1. Base64（编码解码循环）")
        print("2. MD5（哈希，不可逆）")
        print("3. SHA1（哈希，不可逆）")
        print("4. SHA256（哈希，不可逆）")
        print("5. SHA512（哈希，不可逆）")
        print("6. Hex（十六进制编解码）")
        print("7. ROT13（字母替换编解码）")
        print("8. 复合加密（纯英文 + ROT13，完美加密）")
        print("9. 返回上级菜单")
        choice = input("请选择：")

        if choice == "1":
            while True:
                clear()
                print("--- Base64 操作 ---")
                print("1. 普通编码")
                print("2. 普通解码")
                print("3. 循环编码")
                print("4. 循环解码")
                print("5. 返回")
                sub = input()
                if sub == "1":
                    source = input("输入文本或文件路径（'file'前缀）：")
                    if source.startswith("file"):
                        try:
                            with open(source[5], "r", encoding="utf-8") as f:
                                content = f.read()
                        except Exception as e:
                            print(e)
                            input()
                            continue
                    else:
                        content = source
                    encoded = b64_encode(content)
                    out_name = input("输出文件名：") or get_safe_filename_time()
                    out_path = os.path.join(ENCRYPT_DIR, "Base64", f"{out_name}.txt")
                    with open(out_path, "w") as f:
                        f.write(encoded)
                    print(f"保存至 {out_path}")
                    input()
                elif sub == "2":
                    source = input("输入 Base64 文本或文件路径：")
                    if source.startswith("file"):
                        try:
                            with open(source[5], "r") as f:
                                content = f.read().strip()
                        except Exception as e:
                            print(e)
                            input()
                            continue
                    else:
                        content = source
                    try:
                        decoded = b64_decode(content)
                        out_name = input("输出文件名：") or get_safe_filename_time()
                        out_path = os.path.join(ENCRYPT_DIR, "Base64", f"{out_name}.txt")
                        with open(out_path, "w") as f:
                            f.write(decoded)
                        print(f"保存至 {out_path}")
                    except Exception as e:
                        print(f"解码失败 {e}")
                    input()
                elif sub == "3":
                    source = input("输入文本或文件路径：")
                    if source.startswith("file"):
                        with open(source[5], "r") as f:
                            content = f.read()
                    else:
                        content = source
                    try:
                        times = int(input("循环次数："))
                        encoded = repeat_b64_encode(content, times)
                        out_name = input("输出文件名：") or get_safe_filename_time()
                        out_path = os.path.join(ENCRYPT_DIR, "Base64", f"{out_name}.txt")
                        with open(out_path, "w") as f:
                            f.write(encoded)
                        print(f"保存至 {out_path}")
                    except:
                        print("无效次数")
                    input()
                elif sub == "4":
                    source = input("输入 Base64 文本或文件路径：")
                    if source.startswith("file"):
                        with open(source[5], "r") as f:
                            content = f.read().strip()
                    else:
                        content = source
                    try:
                        times = int(input("循环次数："))
                        decoded = repeat_b64_decode(content, times)
                        if decoded:
                            out_name = input("输出文件名：") or get_safe_filename_time()
                            out_path = os.path.join(ENCRYPT_DIR, "Base64", f"{out_name}.txt")
                            with open(out_path, "w") as f:
                                f.write(decoded)
                            print(f"保存至 {out_path}")
                        else:
                            print("解码失败")
                    except:
                        print("无效次数")
                    input()
                elif sub == "5":
                    break
                else:
                    print("无效输入")
                    time.sleep(1)

        elif choice in ["2", "3", "4", "5"]:
            algo_map = {"2": "MD5", "3": "SHA1", "4": "SHA256", "5": "SHA512"}
            algo_name = algo_map[choice]
            hash_func = getattr(hashlib, algo_name.lower())
            source = input("输入文本或文件路径（'file'前缀）：")
            if source.startswith("file"):
                try:
                    with open(source[5], "rb") as f:
                        data = f.read()
                    result = hash_func(data).hexdigest()
                except Exception as e:
                    print(f"文件错误 {e}")
                    input()
                    continue
            else:
                result = hash_func(source.encode("utf-8")).hexdigest()
            out_name = input("输出文件名：") or get_safe_filename_time()
            out_path = os.path.join(ENCRYPT_DIR, algo_name, f"{out_name}.txt")
            with open(out_path, "w") as f:
                f.write(result)
            print(f"{algo_name} 结果保存至 {out_path}")
            input()

        elif choice == "6":
            while True:
                clear()
                print("--- Hex 操作 ---")
                print("1. 编码")
                print("2. 解码")
                print("3. 返回")
                sub = input()
                if sub == "1":
                    source = input("输入文本或文件路径：")
                    if source.startswith("file"):
                        with open(source[5], "r") as f:
                            content = f.read()
                    else:
                        content = source
                    hex_str = content.encode("utf-8").hex()
                    out_name = input("输出文件名：") or get_safe_filename_time()
                    out_path = os.path.join(ENCRYPT_DIR, "Hex", f"{out_name}.txt")
                    with open(out_path, "w") as f:
                        f.write(hex_str)
                    print(f"保存至 {out_path}")
                    input()
                elif sub == "2":
                    source = input("输入 Hex 字符串或文件路径：")
                    if source.startswith("file"):
                        with open(source[5], "r") as f:
                            hex_data = f.read().strip()
                    else:
                        hex_data = source.strip()
                    try:
                        text = bytes.fromhex(hex_data).decode("utf-8", errors="ignore")
                        out_name = input("输出文件名：") or get_safe_filename_time()
                        out_path = os.path.join(ENCRYPT_DIR, "Hex", f"{out_name}.txt")
                        with open(out_path, "w") as f:
                            f.write(text)
                        print(f"保存至 {out_path}")
                    except:
                        print("Hex 解码失败")
                    input()
                elif sub == "3":
                    break

        elif choice == "7":
            while True:
                clear()
                print("--- ROT13 操作 ---")
                print("1. 编码/解码")
                print("2. 返回")
                sub = input()
                if sub == "1":
                    source = input("输入文本或文件路径：")
                    if source.startswith("file"):
                        with open(source[5], "r") as f:
                            content = f.read()
                    else:
                        content = source
                    result = codecs.encode(content, 'rot_13')
                    out_name = input("输出文件名：") or get_safe_filename_time()
                    out_path = os.path.join(ENCRYPT_DIR, "ROT13", f"{out_name}.txt")
                    with open(out_path, "w") as f:
                        f.write(result)
                    print(f"保存至 {out_path}")
                    input()
                elif sub == "2":
                    break

        elif choice == "8":
            while True:
                clear()
                print("--- 复合加密（完美加密）---")
                print("1. 加密（先纯英文加密，再ROT13）")
                print("2. 解密（先ROT13，再反向纯英文解密）")
                print("3. 返回")
                sub = input()
                if sub == "1":
                    print("请选择纯英文加密方法：")
                    print("1. 凯撒密码（可自定义偏移）")
                    print("2. Atbash 密码（自动）")
                    method_choice = input()
                    if method_choice == "1":
                        try:
                            shift = int(input("输入偏移量（整数，默认3）：") or 3)
                        except:
                            shift = 3
                        method = "caesar"
                    elif method_choice == "2":
                        shift = 0
                        method = "atbash"
                    else:
                        print("无效选择")
                        input()
                        continue
                    source = input("输入要加密的文本或文件路径（'file'前缀）：")
                    if source.startswith("file"):
                        try:
                            with open(source[5], "r", encoding="utf-8") as f:
                                plain = f.read()
                        except Exception as e:
                            print(f"文件读取失败 {e}")
                            input()
                            continue
                    else:
                        plain = source
                    encrypted = composite_encrypt(plain, method, shift if method=="caesar" else 0)
                    out_name = input("输出文件名：") or get_safe_filename_time()
                    out_path = os.path.join(ENCRYPT_DIR, "Composite", f"{out_name}.txt")
                    with open(out_path, "w", encoding="utf-8") as f:
                        f.write(encrypted)
                    print(f"复合加密完成，保存至 {out_path}")
                    input()
                elif sub == "2":
                    print("请选择对应的纯英文加密方法：")
                    print("1. 凯撒密码（需知道偏移量）")
                    print("2. Atbash 密码")
                    method_choice = input()
                    if method_choice == "1":
                        try:
                            shift = int(input("输入加密时的偏移量："))
                        except:
                            print("无效偏移")
                            continue
                        method = "caesar"
                    elif method_choice == "2":
                        shift = 0
                        method = "atbash"
                    else:
                        print("无效选择")
                        input()
                        continue
                    source = input("输入要解密的文本或文件路径（'file'前缀）：")
                    if source.startswith("file"):
                        try:
                            with open(source[5], "r", encoding="utf-8") as f:
                                cipher = f.read()
                        except Exception as e:
                            print(f"文件读取失败 {e}")
                            input()
                            continue
                    else:
                        cipher = source
                    decrypted = composite_decrypt(cipher, method, shift if method=="caesar" else 0)
                    out_name = input("输出文件名：") or get_safe_filename_time()
                    out_path = os.path.join(ENCRYPT_DIR, "Composite", f"{out_name}.txt")
                    with open(out_path, "w", encoding="utf-8") as f:
                        f.write(decrypted)
                    print(f"复合解密完成，保存至 {out_path}")
                    input()
                elif sub == "3":
                    break
                else:
                    print("无效输入")
                    time.sleep(1)

        elif choice == "9":
            break
        else:
            print("无效选择，请输入1-9")
            time.sleep(1)

def fetch_webpage():
    clear()
    surl = input("输入网址(不要带http): ")
    if not surl:
        return
    url = "http://" + surl
    name = input("保存的文件名: ")
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Android)"})
        out_path = os.path.join(WEB_DIR, f"{name}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(res.text)
        print(f"已保存至 {out_path}")
    except Exception as e:
        print(f"获取失败 {e}")
    time.sleep(3)

def web_shortcuts():
    while True:
        clear()
        print("1. 懂得都懂")
        print("2. 刷机")
        print("3. 海量视频")
        print("4. 漫画")
        print("其他返回")
        choice = input()
        if choice == "1":
            sec = input("1. 软件网站\n2. 在线网站\n3. JM漫画\n")
            if sec == "1":
                open_url("http://520521.com")
            elif sec == "2":
                open_url("https://1pvfnn.0450.me")
            elif sec == "3":
                open_url("https://18comic.vip")
        elif choice == "2":
            clear()
            print("1. MIUI澎湃")
            print("2. 一加真我OPPO")
            print("3. 萤火虫资源网")
            print("4. 全系列线刷救砖合集")
            sub = input()
            if sub == "1":
                hyper = input("1. 澎湃\n2. MIUI\n")
                if hyper == "1":
                    open_url("https://hyperos.fans")
                elif hyper == "2":
                    mi = input("1. 主站\n2. 备用\n")
                    if mi == "1":
                        open_url("https://xiaomirom.com")
                    else:
                        open_url("http://roms.miuier.com")
            elif sub == "2":
                open_url("http://yun.daxiaamu.com")
            elif sub == "3":
                open_url("https://www.yhcres.top")
            elif sub == "4":
                open_url("https://www.yhcres.top/d/public/%E6%9C%80%E6%96%B0%E5%85%A8%E7%B3%BB%E5%88%97%E7%BA%BF%E5%88%B7%E6%95%91%E7%A0%96%E8%B5%84%E6%96%99%E9%9B%86%E5%90%88%E5%A4%A7%E5%85%A8%20190416.xls?sign=ssXpXHUr9KmAn9Op3kAouFOrvZTLtBgLLQkvoVn9uvo=&_=1775912346")
        elif choice == "3":
            open_url("http://www.hainatv.net")
        elif choice == "4":
            man = input("1. 漫蛙网页\n2. 漫蛙APK\n")
            if man == "1":
                open_url("https://fuwbi.cc/mw666")
            elif man == "2":
                open_url("https://manwa.me")
        else:
            break

def download_file():
    while True:
        clear()
        tp = input("1. 下载APK\n2. 下载ZIP\n3. 返回\n")
        if tp == "1":
            url = input("下载链接: ")
            save_name = os.path.join(APK_DIR, f"{get_safe_filename_time()}.apk")
            try:
                urllib.request.urlretrieve(url, save_name)
                print(f"已保存至 {save_name}")
            except Exception as e:
                print(f"下载失败 {e}")
            time.sleep(3)
        elif tp == "2":
            url = input("下载链接: ")
            save_name = os.path.join(ZIP_DIR, f"{get_safe_filename_time()}.zip")
            try:
                urllib.request.urlretrieve(url, save_name)
                print(f"已保存至 {save_name}")
                if input("是否解压并删除原文件？(1/2): ") == "1":
                    topath = input("解压目录(留空默认Mytool/Unzip): ") or UNZIP_DIR
                    if os.path.exists(save_name):
                        os.system(f"unzip -o '{save_name}' -d '{topath}'")
                        os.remove(save_name)
                        print("解压完成，原文件已删除")
            except Exception as e:
                print(f"下载失败 {e}")
            time.sleep(3)
        else:
            break

def learning():
    while True:
        clear()
        print("1. 下载学习APK")
        print("2. 编程学习网站")
        print("其他返回")
        ch = input()
        if ch == "1":
            url = "https://codetome.cn/downloads/codetome.apk"
            save = os.path.join(APK_DIR, "learn.apk")
            try:
                urllib.request.urlretrieve(url, save)
                shutil.copy(save, "sdcard/Download")
                print("已下载并复制到 Download 目录")
            except Exception as e:
                print(f"失败 {e}")
            time.sleep(3)
        elif ch == "2":
            print("1. CodeCombat\n2. Screeps\n3. CodingGame\n4. 程序员升职记\n5. CodeHunt")
            sub = input()
            urls = {
                "1": "https://codecombat.cn",
                "2": "https://store.screeps.com/zh-CN",
                "3": "https://codinggame.com/start",
                "4": "https://tomorrowcorporation.com",
                "5": "https://codehunt.com"
            }
            if sub in urls:
                open_url(urls[sub])
        else:
            break

def speed_test():
    print("测速中...")
    try:
        url = "https://speed.hetzner.de/10MB.bin"
        tmp = "/sdcard/Download/speedtest.tmp"
        start = time.time()
        urllib.request.urlretrieve(url, tmp)
        cost = time.time() - start
        speed = 10 / cost
        print(f"速度 {speed:.2f} MB/s")
        os.remove(tmp)
    except Exception as e:
        print(f"测速失败 {e}")
    time.sleep(2)

def My_unzip():
    while True:
        clear()
        zpath = input("zip文件路径: ")
        topath = input("解压目录(默认Mytool/Unzip): ") or UNZIP_DIR
        if os.path.exists(zpath):
            os.system(f"unzip -o '{zpath}' -d '{topath}'")
            if input("删除原文件？(1/2): ") == "1":
                os.remove(zpath)
            print("完成\n是否返回？ 返回请输入1")
            exitt = input()
            if exitt == "1":
                break
            else:
                time.sleep(1)
        else:
            print("文件不存在\n是否返回 返回请输入1")
            exitt = input()
            if exitt == "1":
                break
            else:
                time.sleep(1)
        time.sleep(2)

def about():
    while True:
        clear()
        print("作者 BY.MY\n联系方式")
        print("1. 快手")
        print("2. Telegram")
        print("3. 返回")
        ch = input()
        if ch == "1":
            open_url("https://v.kuaishou.com/KhI3VnPa")
        elif ch == "2":
            open_url("https://t.me/By_Mytool")
        else:
            break

def video_edit():
    while True:
        clear()
        print("剪辑专区")
        print("1. 下载软件")
        print("2. 返回")
        ch = input()
        if ch == "1":
            print("1. 快影\n2. 剪映")
            app = input()
            if app == "1":
                open_url("https://js.a.kspkg.com/kos/nlav/10814/kuaiying-generic--7.44.0.744005_x64_84ad90.apk")
            elif app == "2":
                open_url("https://lf9-apk.ugapk.cn/package/apk/videocut/18076_199001600/videocut_pc_jianying_android_v18076_199001600_c6cd_1779881403.apk")
            else:
                break
        else:
            break

def device_info_detailed():
    clear()
    print("========== 设备信息 1 ==========")
    props = [
        ("ro.product.manufacturer", "厂商"),
        ("ro.product.model", "型号"),
        ("ro.build.version.release", "Android 版本"),
        ("ro.build.version.sdk", "SDK 版本"),
        ("ro.build.fingerprint", "指纹"),
        ("ro.product.cpu.abi", "CPU 架构"),
    ]
    for prop, name in props:
        cmd = f"getprop {prop}"
        result = os.popen(cmd).read().strip()
        print(f"{name}: {result if result else '未知'}")
    size = os.popen("wm size").read().strip()
    print(f"屏幕: {size}")
    density = os.popen("wm density").read().strip()
    print(f"密度: {density}")
    battery = os.popen("dumpsys battery 2>/dev/null | grep -E 'level|temperature|status'").read().strip()
    if battery:
        print("\n电池信息")
        print(battery)
    else:
        print("\n电池信息 无法获取（需系统权限）")
    print("===== 设备信息 2 =====")
    os.system("uname -a")
    os.system("free -h")
    os.system("df -h")
    input("回车返回")

def export_app_list():
    clear()
    print("导出已安装应用列表...")
    out_path = os.path.join(BASE_DIR, "app_list.txt")
    os.system(f"pm list packages > {out_path}")
    friendly_path = os.path.join(BASE_DIR, "app_list_friendly.txt")
    with open(friendly_path, "w", encoding="utf-8") as f:
        f.write("包名列表（共")
        count = len(open(out_path).readlines())
        f.write(f"{count} 个应用)\n")
        os.system(f"pm list packages >> {friendly_path}")
    print(f"已保存到\n{out_path}\n{friendly_path}")
    input("回车返回")

def clean_sdcard():
    clear()
    print("扫描 sdcard 下的大文件及空文件夹...")
    target_dirs = ["/sdcard/Download", "/sdcard/DCIM", "/sdcard/Pictures", "/sdcard/Movies", "/sdcard/Android/data"]
    large_files = []
    for d in target_dirs:
        if os.path.exists(d):
            for root, dirs, files in os.walk(d):
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        size = os.path.getsize(fp)
                        if size > 50 * 1024 * 1024:
                            large_files.append((fp, size))
                    except:
                        pass
    if large_files:
        print("发现以下大文件（>50MB）：")
        for i, (fp, sz) in enumerate(large_files[:20]):
            print(f"{i+1}. {fp} ({sz/(1024*1024):.2f} MB)")
        if input("是否删除这些文件？(y/n): ").lower() == 'y':
            for fp, _ in large_files:
                try:
                    os.remove(fp)
                    print(f"已删除 {fp}")
                except:
                    print(f"删除失败 {fp}")
    else:
        print("未发现大文件。")

    empty_dirs = []
    for d in target_dirs:
        if os.path.exists(d):
            for root, dirs, files in os.walk(d):
                if not files and not dirs:
                    empty_dirs.append(root)
    if empty_dirs:
        print(f"\n发现 {len(empty_dirs)} 个空文件夹，是否删除？(y/n): ")
        if input().lower() == 'y':
            for d in empty_dirs:
                try:
                    os.rmdir(d)
                    print(f"已删除 {d}")
                except:
                    pass
    else:
        print("未发现空文件夹。")
    input("清理完成，回车返回")

def network_tools():
    while True:
        clear()
        print("网络工具")
        print("1. Ping 测试")
        print("2. TCP 端口扫描（局域网）")
        print("3. 返回")
        ch = input()
        if ch == "1":
            target = input("输入域名或 IP: ")
            os.system(f"ping -c 4 {target}")
            input("回车继续")
        elif ch == "2":
            ip = input("输入目标 IP: ")
            ports = input("输入端口范围（如 1-1000）: ")
            try:
                start, end = map(int, ports.split('-'))
                print(f"扫描 {ip} 端口 {start}-{end}...")
                open_ports = []
                for port in range(start, min(end+1, 65536)):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((ip, port))
                    if result == 0:
                        open_ports.append(port)
                        print(f"端口 {port} 开放")
                    sock.close()
                print(f"\n扫描完成，开放端口 {open_ports}")
            except Exception as e:
                print(f"扫描失败 {e}")
            input("回车继续")
        else:
            break

def backup_folder():
    clear()
    src = input("请输入要备份的文件夹路径（如 /sdcard/DCIM）: ")
    if not os.path.exists(src):
        print("路径不存在")
        input("回车返回")
        return
    dest_name = input("备份文件名（不含扩展名）: ")
    backup_path = os.path.join(BASE_DIR, "backup", f"{dest_name}.zip")
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    print(f"正在打包 {src} 到 {backup_path}...")
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(src):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, os.path.dirname(src))
                zipf.write(full_path, arcname)
    print(f"备份完成 {backup_path}")
    input("回车返回")

def restore_backup():
    clear()
    backup_dir = os.path.join(BASE_DIR, "backup")
    if not os.path.exists(backup_dir):
        print("无备份文件")
        input("回车返回")
        return
    backups = [f for f in os.listdir(backup_dir) if f.endswith('.zip')]
    if not backups:
        print("没有找到备份文件")
        input("回车返回")
        return
    print("可用备份")
    for i, b in enumerate(backups):
        print(f"{i+1}. {b}")
    idx = int(input("选择序号: ")) - 1
    if 0 <= idx < len(backups):
        zip_path = os.path.join(backup_dir, backups[idx])
        extract_to = input("解压到目录（默认 /sdcard/restore）: ") or "/sdcard/restore"
        os.makedirs(extract_to, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(extract_to)
        print(f"已解压到 {extract_to}")
    else:
        print("无效选择")
    input("回车返回")

def file_tools():
    while True:
        clear()
        print("文件工具")
        print("1. 批量重命名（添加前缀后缀）")
        print("2. 按文件名搜索文件")
        print("3. 计算文件 MD5")
        print("4. 返回")
        ch = input()
        if ch == "1":
            path = input("目录路径: ")
            if not os.path.isdir(path):
                print("无效目录")
                input()
                continue
            prefix = input("前缀（直接回车跳过）: ")
            suffix = input("后缀（直接回车跳过）: ")
            for fname in os.listdir(path):
                full = os.path.join(path, fname)
                if os.path.isfile(full):
                    name, ext = os.path.splitext(fname)
                    new_name = prefix + name + suffix + ext
                    new_full = os.path.join(path, new_name)
                    os.rename(full, new_full)
            print("重命名完成")
            input("回车返回")
        elif ch == "2":
            root_dir = input("搜索起始目录（默认 /sdcard）: ") or "/sdcard"
            keyword = input("文件名关键字: ")
            print("搜索中...")
            for r, ds, fs in os.walk(root_dir):
                for f in fs:
                    if keyword in f:
                        print(os.path.join(r, f))
            input("搜索完毕，回车继续")
        elif ch == "3":
            file_path = input("文件路径: ")
            if os.path.isfile(file_path):
                import hashlib
                with open(file_path, 'rb') as f:
                    md5 = hashlib.md5(f.read()).hexdigest()
                print(f"MD5: {md5}")
            else:
                print("文件不存在")
            input("回车返回")
        else:
            break

def c_editor():
    clear()
    print("C 语言小助手（需安装 gcc/clang）")
    if not HAS_GCC:
        print("警告 未检测到 gcc 或 clang，无法编译运行。请在 Termux 中执行 pkg install clang")
        input("回车继续")
        return
    code = input("请输入 C 代码（单条语句或定义）...\n或输入 'file' 从文件加载: ")
    if code.strip() == "file":
        fpath = input("C 文件路径: ")
        if os.path.exists(fpath):
            with open(fpath, 'r') as f:
                code = f.read()
        else:
            print("文件不存在")
            return
    exec_dir = os.path.expanduser("~/.temp_c")
    os.makedirs(exec_dir, exist_ok=True)
    tmp_c = os.path.join(exec_dir, "temp.c")
    tmp_bin = os.path.join(exec_dir, "temp")
    with open(tmp_c, 'w') as f:
        f.write(code)
    ret = os.system(f"gcc {tmp_c} -o {tmp_bin} 2>&1")
    if ret != 0:
        print("编译失败")
    else:
        os.system(f"chmod +x {tmp_bin}")
        print("编译成功，运行结果:")
        os.system(tmp_bin)
    input("\n回车返回")
    for f in [tmp_c, tmp_bin]:
        if os.path.exists(f):
            os.remove(f)
    try:
        os.rmdir(exec_dir)
    except OSError:
        pass

def python_shell():
    clear()
    print("Python 交互式终端（输入 exit() 或 quit 返回）")
    while True:
        code = input(">>> ")
        if code.strip() in ("exit()", "quit"):
            break
        try:
            exec(code)
        except Exception as e:
            print(f"错误 {e}")

def java_editor():
    clear()
    print("Java 小助手（需安装 javac 和 java）")
    if not HAS_JAVAC or not HAS_JAVA:
        print("警告 未检测到 javac 或 java。请在 Termux 中安装 pkg install openjdk-17")
        input("回车返回")
        return
    code = input("请输入 Java 代码（类名必须为 Main）...\n或输入 'file' 从文件加载: ")
    if code.strip() == "file":
        fpath = input("Java 文件路径: ")
        if os.path.exists(fpath):
            with open(fpath, 'r') as f:
                code = f.read()
        else:
            print("文件不存在")
            return
    tmp_dir = os.path.expanduser("~/.temp_java")
    os.makedirs(tmp_dir, exist_ok=True)
    java_file = os.path.join(tmp_dir, "Main.java")
    with open(java_file, 'w') as f:
        f.write(code)
    ret = os.system(f"javac {java_file} 2>&1")
    if ret != 0:
        print("编译失败")
    else:
        print("编译成功，运行结果:")
        os.system(f"cd {tmp_dir} && java Main")
    input("回车返回")
    for f in os.listdir(tmp_dir):
        os.remove(os.path.join(tmp_dir, f))
    os.rmdir(tmp_dir)

def js_editor():
    clear()
    print("JavaScript 运行环境 (Node.js)")
    if not HAS_NODE:
        print("未检测到 Node.js，请在 Termux 中执行 pkg install nodejs")
        input("回车返回")
        return
    code = input("请输入 JavaScript 代码（可直接运行）...\n或输入 'file' 从文件加载: ")
    if code.strip() == "file":
        fpath = input("JS 文件路径: ")
        if os.path.exists(fpath):
            with open(fpath, 'r') as f:
                code = f.read()
        else:
            print("文件不存在")
            return
    tmp_dir = os.path.expanduser("~/.temp_js")
    os.makedirs(tmp_dir, exist_ok=True)
    tmp_file = os.path.join(tmp_dir, "script.js")
    with open(tmp_file, 'w') as f:
        f.write(code)
    print("\n----- 运行结果 -----")
    os.system(f"node {tmp_file}")
    print("--------------------")
    input("回车返回")
    os.remove(tmp_file)
    try:
        os.rmdir(tmp_dir)
    except OSError:
        pass

def startgame():
    while True:
        print("选择你要启动的游戏")
        print("1.和平精英 2.王者荣耀 3.暗区突围 4.PUBG MOBILE 5.返回")
        gamestart = input()
        if gamestart == "1":
            os.system("am start -n com.tencent.tmgp.pubgmhd/com.epicgames.ue4.SplashActivity")
        elif gamestart == "2":
            os.system("am start -n com.tencent.tmgp.sgame/com.tencent.tmgp.sgame.SGameActivity")
        elif gamestart == "3":
            os.system("am start -n com.tencent.mf.uam/com.epicgames.ue4.GameActivity")
        elif gamestart == "4":
            while True:
                print("1.全球 2.日韩 3.台湾 4.越南 5.返回")
                pubgm = input()
                if pubgm == "1":
                    os.system("am start -n com.tencent.ig/com.epicgames.ue4.SplashActivity")
                elif pubgm == "2":
                    os.system("am start -n com.pubg.krmobile/com.epicgames.ue4.SplashActivity")
                elif pubgm == "3":
                    os.system("am start -n com.rekoo.pubgm/com.epicgames.ue4.SplashActivity")
                elif pubgm == "4":
                    os.system("am start -n com.vng.pubgmobile/com.epicgames.ue4.SplashActivity")
                else:
                    break
        else:
            break

def main():
    clear()
    old_current_log = """本次更新日志
1.增加功能快捷启动游戏
2.更改页面名称以及部分功能排序
        ----2026.6.6"""
    old_past_log = """过往更新日志
1.增加更多功能已安装应用名称列表-网络工具-备份恢复文件-文件工具-三种主流语言可执行窗口(需要装载对应命令)
         ----2026.6.4

1.增加剪辑页面
2.增加一个大分支
3.启动界面改为运行时间本次更新日志过往更新日志
         ----2026.6.3

1.将文件下载改为选择单多线程下载
2.将解压合并到zip文件下载内
         ----2026.4.18"""
    new_current_log = """本次更新日志
1. 新增加密解密工具（集成Base64、MD5、SHA1/256/512、Hex、ROT13）
2. 新增复合加密（先纯英文加密：凯撒/Atbash，再ROT13，输出纯英文）
3. 界面重构：所有功能直接主界面展示
        ----2026.6.13"""

    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            f.write(f"首次运行时间：{get_time_str()}")
        print(new_current_log)
        time.sleep(1)
        print(old_current_log)
        print(old_past_log)
        time.sleep(3)
    else:
        log_runtime()
        print(new_current_log)
        time.sleep(1)
        print(old_current_log)
        print(old_past_log)
        time.sleep(3)

    while True:
        clear()
        print(f"当前时间 {get_time_str()}")
        print("----------------By.MY----------------")
        print("当前版本仅供开发者自行使用\n如若开发者做出违法行为，与工具开发者本人无关！")
        print("---------介绍---------")
        print("本工具由个人开发，并非集体开发\n如若有人恶意使用本工具做出违法犯罪行为\n与本人和本工具无关")
        print("---------功能区---------")
        print("1. 加密解密工具          2. 获取网页源码")
        print("3. 常用网址             4. 下载文件")
        print("5. 学习编程             6. 网速测试")
        print("7. 解压文件             8. 关于")
        print("9. 编程窗口            10. 详细设备信息")
        print("11. 应用列表导出       12. 清理垃圾文件")
        print("13. 网络工具            14. 备份恢复")
        print("15. 文件工具            16. 游戏快速启动")
        print("17. 剪辑专区")
        print("18. 退出")
        cmd = input("请选择: ")

        if cmd == "1":
            encrypt_decrypt_tool()
        elif cmd == "2":
            fetch_webpage()
        elif cmd == "3":
            web_shortcuts()
        elif cmd == "4":
            download_file()
        elif cmd == "5":
            learning()
        elif cmd == "6":
            speed_test()
        elif cmd == "7":
            My_unzip()
        elif cmd == "8":
            about()
        elif cmd == "9":
            while True:
                print("编程语言窗口")
                print("1. Python 交互终端")
                print("2. C 编辑器 (需编译器)")
                print("3. Java 编辑器 (需 JDK)")
                print("4. JavaScript (需 Node.js)")
                print("5. 返回")
                lang = input()
                if lang == "1":
                    python_shell()
                elif lang == "2":
                    c_editor()
                elif lang == "3":
                    java_editor()
                elif lang == "4":
                    js_editor()
                else:
                    break
        elif cmd == "10":
            device_info_detailed()
        elif cmd == "11":
            export_app_list()
        elif cmd == "12":
            clean_sdcard()
        elif cmd == "13":
            network_tools()
        elif cmd == "14":
            while True:
                print("1. 备份文件夹  2. 恢复备份  3. 返回")
                sub = input()
                if sub == "1":
                    backup_folder()
                elif sub == "2":
                    restore_backup()
                else:
                    break
        elif cmd == "15":
            file_tools()
        elif cmd == "16":
            startgame()
        elif cmd == "17":
            video_edit()
        elif cmd == "18":
            print("谢谢使用，欢迎下次使用.")
            time.sleep(1)
            exit()
        else:
            print("请正确输入序号！")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序已退出")
        time.sleep(1)
        exit(0)