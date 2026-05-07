ProjectX: Ferramenta abrangente de força bruta
O ProjectX é uma poderosa ferramenta de força bruta projetada para realizar ataques baseados em dicionário em diversos protocolos. Ele inclui várias listas de palavras para diferentes tipos de alvos e oferece amplas opções de personalização.

Características
Suporte a múltiplos protocolos (SSH, HTTP, FTP, SMTP)
Listas de palavras integradas para alvos comuns
Suporte para listas de palavras personalizadas
Execução de ataque paralelo
Acompanhamento do progresso e estatísticas
Geração automática de credenciais
Opções avançadas de filtragem
Instalação
bash
Download
Copiar código
git clone https://github.com/kindo/projectx.git
cd projectx
pip install -r requirements.txt
Exemplos de uso
Ataques básicos de força bruta em SSH
bash
Download
Copiar código
python3 projectx.py --protocol ssh --target 192.168.1.100 --username admin --wordlist ssh_wordlist.txt
Autenticação HTTP Avançada
bash
Download
Copiar código
python3 projectx.py --protocol http --target https://example.com/login --username-list users.txt --password-list passwords.txt --threads 10 --timeout 5
Suporte a protocolos personalizados
bash
Download
Copiar código
python3 projectx.py --protocol custom --config custom_config.json --target example.com --wordlist custom_words.txt
Listas de palavras incluídas
ssh_wordlist.txtCredenciais SSH comuns
http_wordlist.txtCredenciais de autenticação web
ftp_wordlist.txtCredenciais do servidor FTP
smtp_wordlist.txtCredenciais do servidor de e-mail
custom_words.txtCredenciais genéricas
Exemplo de arquivo de configuração
json
Download
Copiar código
{
  "protocol": "ssh",
  "target": "192.168.1.100",
  "port": 22,
  "username_list": ["admin", "root", "test"],
  "password_list": ["password", "123456", "admin"],
  "timeout": 5,
  "threads": 5
}
Configuração de desenvolvimento
Para desenvolvedores:

bash
Download
Copiar código
git clone https://github.com/kindo/projectx.git
cd projectx
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/
Contribuindo
Faça um fork do repositório.
Criar branch de recurso ( git checkout -b feature/new-feature)
Confirmar alterações ( git commit -am 'Add new feature')
Enviar para o branch ( git push origin feature/new-feature)
Criar nova solicitação de pull request
Licença
Licença MIT

Contato
Para problemas ou sugestões, abra uma issue no GitHub ou entre em contato com a equipe pelo endereço security@kindo.io.

Copiar mensagem
Deslize para o final da página.

Resposta regenerada
