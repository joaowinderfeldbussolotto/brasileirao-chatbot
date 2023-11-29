# actions/actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from config import settings
API_ENDPOINT =  settings.API_URL

class ActionResultadosRodada(Action):
    def name(self) -> Text:
        return "action_resultados_rodada"
    

    def format_games(self, data):
        formatted_data = """
            **Resultados dos Jogos - Rodada {}**
            {}
            """.format(data['number'], "\n\n".join(
                "{}. {} vs. {}\n   - Placar: {}".format(
                    idx + 1, game['home_team'], game['away_team'], game['score']
                    
                )
                for idx, game in enumerate(data['games'])
            ))
        return formatted_data

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        rodada = tracker.get_slot('rodada')
        print(rodada)
        api_endpoint = f'{API_ENDPOINT}rodada/{rodada}'
        print(api_endpoint)
        response = requests.get(api_endpoint)
        data = response.json()
        if response.status_code == 200:
            games = self.format_games(data)
            dispatcher.utter_message(games)
            return []
        print(data)
        dispatcher.utter_message("Algo deu errado")
        return []
            


class ActionResultadosRodada(Action):
    def name(self) -> Text:
        return "action_tabela"

    def format_standings_table(self, data):
        formatted_data = """
        **Classificação do Campeonato Brasileiro:**

        {}
        """.format("\n\n".join(
            "{}. **{}**\n   - Posição: {}\n   - Pontos: {}\n   - Jogos: {}".format(
                entry['position'], entry['team'], entry['position'], entry['points'], entry['games_played']
            )
            for entry in data
        ))

        return formatted_data

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        endpoint = f'{API_ENDPOINT}tabela/'
        response = requests.get(endpoint)
        data = response.json()

        if response.status_code == 200:
            standings = self.format_standings_table(data)
            dispatcher.utter_message(standings)
            return []
        
        dispatcher.utter_message("Algo deu errado")
        return []
            
