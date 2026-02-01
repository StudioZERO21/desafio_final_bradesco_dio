import os
import time
from google import genai
from google.genai import errors

# --- CONFIGURAÇÃO DE AMBIENTE ---
MINHA_CHAVE = "DIGITE AQUI A SUA CHAVE"
MODELO_ID = "gemini-2.5-flash"

client = genai.Client(api_key=MINHA_CHAVE)


INSTRUCAO_SISTEMA = (
    "Você é um Assistente de Relacionamento Financeiro Digital. "
    "Seu objetivo é oferecer interações claras, seguras e personalizadas. "
    "Ao explicar produtos (como Selic ou FIIs), use linguagem simples. "
    "Se o usuário pedir cálculos, ajude-o a entender os conceitos por trás dos números. "
    "Sempre mantenha o foco em educação financeira e boas práticas de mercado."
)

def iniciar_sessao():
    return client.chats.create(
        model=MODELO_ID,
        config={"system_instruction": INSTRUCAO_SISTEMA}
    )

def simulador_poupanca_vs_selic(valor):
    """Exemplo de funcionalidade de cálculo demonstrativo citada no roteiro"""
    # Lógica simples de Python para simulação
    selic_estimada = 0.1075  # 10.75% ao ano
    poupanca_estimada = 0.0617 # ~6.17% ao ano
    
    res_selic = valor * (1 + selic_estimada)
    res_poup = valor * (1 + poupanca_estimada)
    
    return (f"\n[SIMULAÇÃO RÁPIDA]: Se você investir R${valor:.2f} hoje:\n"
            f"- Em 1 ano com Selic (10.75%): R${res_selic:.2f}\n"
            f"- Em 1 ano na Poupança (6.17%): R${res_poup:.2f}\n")

def executar_assistente():
    chat = iniciar_sessao()
    print("--- EXPERIÊNCIA DIGITAL FINANCEIRA ---")
    print("Olá! Sou seu assistente guiado por IA. Como posso ajudar seu bolso hoje?")
    print("(Digite 'sair' para encerrar ou 'simular' para um exemplo de cálculo)\n")

    while True:
        entrada = input("Você: ").strip()

        if entrada.lower() in ["sair", "exit"]:
            print("\nObrigado por utilizar nossa solução financeira. Até logo!")
            break
        
        if entrada.lower() == "simular":
            valor = float(input("Qual valor deseja simular para 1 ano? R$"))
            print(simulador_poupanca_vs_selic(valor))
            continue

        if not entrada:
            continue

        try:
            response = chat.send_message(entrada)
            print(f"\nAssistente: {response.text}\n")
        
        except errors.ClientError as e:
            if "429" in str(e):
                print(" Sistema processando muitas requisições. Aguarde instantes...")
                time.sleep(30)
            else:
                print(f"Erro técnico: {e}")

if __name__ == "__main__":
    executar_assistente()
