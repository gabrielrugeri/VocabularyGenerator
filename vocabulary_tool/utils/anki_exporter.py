"""
anki_exporter.py - Exportador de cartões para Anki com suporte a TTS em inglês via AwesomeTTS

Requisitos:
- Anki rodando com AnkiConnect instalado (https://foosoft.net/projects/anki-connect/)
- Add-on AwesomeTTS instalado no Anki (para geração de áudio)
"""

import json
import urllib.request
from typing import Dict, List, Optional

# Starndard CSS for Anki cards
CARD_CSS = """
.card {
    font-family: Arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}
"""

def boldweight(word: str, sentence: str) -> str:
    return sentence.replace(word, f"<b>{word}</b>")
class AnkiExporter:
    def __init__(self, anki_connect_url: str = "http://localhost:8765"):
        self.anki_connect_url = anki_connect_url

    def _request(self, action: str, params: Dict = None) -> str:
        """
        Envia uma requisição para o AnkiConnect com tratamento de erros amigável
        
        Args:
            action: Ação do AnkiConnect (ex: "addNote", "createModel")
            params: Parâmetros da ação
            
        Returns:
            Mensagem de status formatada (✅/⚠️/❌)
        """
        payload = {"action": action, "version": 6, "params": params or {}}
        
        try:
            req = urllib.request.Request(
                self.anki_connect_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req) as response:
                result = json.load(response)
                
            if result.get("error"):
                return f"⚠️ Erro no AnkiConnect: {result['error']}"
            return "✅ Operação realizada com sucesso!" 
        except urllib.error.URLError as e:
            return f"❌ Não foi possível conectar ao Anki: {e.reason}"
        except json.JSONDecodeError:
            return "❌ Resposta inválida do AnkiConnect"
        except Exception as e:
            return f"❌ Erro inesperado: {str(e)}"

    def create_tts_model(self, model_name: str = "TTS_English") -> Dict:
        """
        Cria um modelo de cartão com suporte a TTS em inglês
        
        Args:
            model_name: Nome do modelo a ser criado
            
        Returns:
            Resposta do AnkiConnect
        """
        fields = ["Front", "Back", "TTS_English"]
        template = {
            "Name": "Card 1",
            "Front": "{{Front}}<br>{{tts en_US voices=AwesomeTTS:TTS_English}}",
            "Back": "{{FrontSide}}<hr id=answer>{{Back}}"
        }
        
        return self._request(
            "createModel",
            {
                "modelName": model_name,
                "inOrderFields": fields,
                "css": CARD_CSS,
                "cardTemplates": [template]
            }
        )

    def add_tts_card(
        self,
        deck_name: str,
        front: str,
        back: str,
        tts_text: str,
        model_name: str = "TTS_English",
        tags: Optional[List[str]] = None
    ) -> Dict:
        """
        Adiciona um cartão com suporte a TTS em inglês
        
        Args:
            deck_name: Nome do deck de destino
            front: Texto da frente do cartão
            back: Texto do verso do cartão
            tts_text: Texto a ser convertido em TTS (inglês)
            model_name: Nome do modelo a ser usado
            tags: Lista de tags para o cartão
            
        Returns:
            Resposta do AnkiConnect
        """
        return self._request(
            "addNote",
            {
                "note": {
                    "deckName": deck_name,
                    "modelName": model_name,
                    "fields": {
                        "Front": front,
                        "Back": back,
                        "TTS_English": tts_text
                    },
                    "options": {"allowDuplicate": False},
                    "tags": tags or []
                }
            }
        )

    def ensure_model_exists(self, model_name: str = "TTS_English") -> None:
        """Verifica se o modelo existe ou cria um novo"""
        models = self._request("modelNames")
        if model_name not in models.get("result", []):
            self.create_tts_model(model_name)

# Exemplo de uso
if __name__ == "__main__":
    exporter = AnkiExporter()
    
    # 1. Garantir que o modelo existe
    exporter.ensure_model_exists()
    
    # 2. Adicionar um cartão de exemplo
    result = exporter.add_tts_card(
        deck_name="English::Vocabulary",
        front="What is the English word for 'maçã'?",
        back="apple",
        tts_text="apple",
        tags=["fruit", "basic"]
    )
    
    print("Cartão adicionado com sucesso!" if result.get("result") else "Erro:", result)
