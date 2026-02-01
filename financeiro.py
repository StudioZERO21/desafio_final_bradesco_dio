import os
import time
from google import genai
from google.genai import errors

# 1. Configuração de acesso
MINHA_CHAVE = "DIGITE AQUI A SUA CHAVE"  
MODELO_ID = "gemini-2.5-flash"


client = genai.Client(api_key=MINHA_CHAVE)

def iniciar_assistente():
    print(f"Bem-vindo ao Assistente  Financeiro (Modelo: {MODELO_ID})")
    print("Digite 'sair' para encerrar.\n")
    
    
    chat = client.chats.create(
        model=MODELO_ID,
        config={
            "system_instruction": "Você é um especialista em investimentos e tecnologia. Ajude o usuário de forma clara."
        }
    )
    return chat

def executar_conversa():
    try:
        sessao_chat = iniciar_assistente()

        while True:
            pergunta = input("Você: ")
            
            if pergunta.lower() in ["sair", "exit"]:
                print("Encerrando... Boa Sorte e até mais!")
                break
            
            if not pergunta.strip():
                continue

            try:
                # Envio da mensagem
                response = sessao_chat.send_message(pergunta)
                print(f"\nAssistente: {response.text}\n")
            
            except errors.ClientError as e:
                if "429" in str(e):
                    print("\n[AVISO]: Limite atingido. Aguardando 30 segundos...")
                    time.sleep(35)
                    # Tenta novamente uma vez após o descanso
                    response = sessao_chat.send_message(pergunta)
                    print(f"\nAssistente: {response.text}\n")
                else:
                    print(f"\nErro na chamada: {e}")

    except Exception as e:
        print(f"\nErro crítico na sessão: {e}")

if __name__ == "__main__":
    executar_conversa()



