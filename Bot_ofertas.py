import requests
import json
import os
import random
from datetime import datetime

# ==========================================
# CONFIGURAÇÕES - EDITE AQUI
# ==========================================

# Lista dos seus links de afiliado do Mercado Livre
# Substitua pelos seus links reais do formato https://meli.la/xxxxx
LINKS_AFILIADOS = [
    "https://meli.la/xxxxx",  # Produto 1
    "https://meli.la/yyyyy",  # Produto 2
    "https://meli.la/zzzzz",  # Produto 3
    # Adicione quantos links quiser...
]

# Configurações do WhatsApp (CallMeBot - gratuito)
NUMERO_WHATSAPP = "5511999999999"  # Seu número com DDI (55) + DDD + número
API_KEY_CALLMEBOT = "12345678"      # Sua chave do CallMeBot

# Configurações de envio
INTERVALO_MINUTOS = 30  # Intervalo entre envios (em minutos)
MENSAGEM_POR_VEZ = 1    # Quantas ofertas enviar a cada vez

# ==========================================
# FUNÇÕES DO BOT
# ==========================================

def carregar_historico():
    """
    Carrega o histórico de links já enviados
    """
    try:
        if os.path.exists("historico.json"):
            with open("historico.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except:
        return []

def salvar_historico(link):
    """
    Salva um link no histórico de enviados
    """
    historico = carregar_historico()
    historico.append({
        "link": link,
        "data": datetime.now().isoformat()
    })
    # Mantém apenas últimos 50 registros
    historico = historico[-50:]
    
    with open("historico.json", "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

def escolher_link():
    """
    Escolhe um link que ainda não foi enviado recentemente
    """
    historico = carregar_historico()
    links_enviados = [h["link"] for h in historico]
    
    # Filtra links não enviados recentemente
    links_disponiveis = [link for link in LINKS_AFILIADOS if link not in links_enviados]
    
    # Se todos já foram enviados, reinicia o ciclo
    if not links_disponiveis:
        print("🔄 Todos os links foram enviados. Reiniciando ciclo...")
        # Limpa histórico antigo (mantém apenas últimos 20%)
        historico = historico[-int(len(LINKS_AFILIADOS)*0.2):]
        with open("historico.json", "w", encoding="utf-8") as f:
            json.dump(historico, f, ensure_ascii=False, indent=2)
        links_disponiveis = LINKS_AFILIADOS
    
    # Retorna um link aleatório dos disponíveis
    return random.choice(links_disponiveis)

def criar_mensagem(link):
    """
    Cria a mensagem formatada para o WhatsApp
    """
    mensagem = f"""🔥 OFERTA

🛒 Comprar agora:
{link}"""
    return mensagem

def enviar_whatsapp(mensagem):
    """
    Envia mensagem via CallMeBot (API gratuita)
    """
    try:
        url = "https://api.callmebot.com/whatsapp.php"
        params = {
            "phone": NUMERO_WHATSAPP,
            "text": mensagem,
            "apikey": API_KEY_CALLMEBOT
        }
        
        print(f"📤 Enviando mensagem para {NUMERO_WHATSAPP}...")
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            print("✅ Mensagem enviada com sucesso!")
            return True
        else:
            print(f"❌ Erro ao enviar: {response.text}")
            return False
            
    except Exception as erro:
        print(f"❌ Erro na conexão: {erro}")
        return False

def main():
    """
    Função principal - executa o bot
    """
    print("=" * 40)
    print("🤖 BOT DE OFERTAS - Mercado Livre")
    print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 40)
    
    # Verifica se há links configurados
    if not LINKS_AFILIADOS or LINKS_AFILIADOS[0] == "https://meli.la/xxxxx":
        print("⚠️ ERRO: Você precisa configurar seus links de afiliado!")
        print("Edite o arquivo bot_ofertas.py e substitua os links na lista LINKS_AFILIADOS")
        return
    
    print(f"📦 Total de links cadastrados: {len(LINKS_AFILIADOS)}")
    
    # Escolhe link para enviar
    link_escolhido = escolher_link()
    print(f"🔗 Link escolhido: {link_escolhido[:40]}...")
    
    # Cria mensagem
    mensagem = criar_mensagem(link_escolhido)
    print("\n📋 Mensagem criada:")
    print("-" * 40)
    print(mensagem)
    print("-" * 40)
    
    # Envia para WhatsApp
    sucesso = enviar_whatsapp(mensagem)
    
    if sucesso:
        salvar_historico(link_escolhido)
        print(f"\n✅ Oferta enviada e salva no histórico!")
    else:
        print(f"\n❌ Falha ao enviar oferta")
    
    print(f"\n🕐 Próximo envio em {INTERVALO_MINUTOS} minutos")
    print("=" * 40)

if __name__ == "__main__":
    main()
