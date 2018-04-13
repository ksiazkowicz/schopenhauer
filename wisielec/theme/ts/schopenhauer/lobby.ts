import { ajaxGET, ReconnectingWebsocketHandler } from "../modules/utils";
import { show_info_block, ErrorOptions, include_from_template } from "../modules/decadence";

export class SchopenhauerLobby extends ReconnectingWebsocketHandler {
    running_game_list: Element;
    your_tournament_list: Element;

    constructor() {
        super();
        this.url = "/lobby";
        this.running_game_list = document.getElementById("running-games-list");
        this.your_tournament_list = document.getElementById("your-tournament-list");
        this.connect();
        this.refreshTournaments();
    }

    updatePlayers(block_id: any, players: any) {
        var players_list = document.getElementById(block_id);
        if (players != "") {
            var new_players = "";
            for (var i = 0; i < players.length; i++) {
                var player = players[i];
                new_players += "<a href='/profiles/view/" + player + "/'>" + player + "</a>";
                if (i != players.length - 1)
                    new_players += ", ";
                players_list.innerHTML = new_players;
            }
        } else if (players_list) players_list.innerHTML = "nie żyją!";
    }

    refreshTournaments() {
        ajaxGET("/api/v1/tournament", { "in_progress": 1 }).then((response) => {
            return response.json()
        }).then((json) => {
            this.your_tournament_list.innerHTML = "";
            for (let tournament of json.tournaments) {
                include_from_template(this.your_tournament_list,
                    "includes/decadence/tournament_item.html",
                    tournament, "beforeend");
            }
        }).catch((reason) => {
            show_info_block("danger", "Odświeżenie listy turniejów nie powiodło się.", new ErrorOptions);
        });
    }

    appendGame(session_id: string, progress: string) {
        if (!document.getElementById("game-" + session_id)) {
            include_from_template(this.running_game_list, "includes/decadence/lobby_game.html", { "session_id": session_id, "progress": progress }, "beforeend");
        }
    }

    onMessage(evt: any) {
        let data_json = JSON.parse(evt.data);
        let games = data_json.running_games;
        let players = data_json.players;
        let game_id = data_json.session_id;

        if (games) {
            for (var i = 0, len = games.length; i < len; i++) {
                this.appendGame(games[i].session_id, games[i].progress);
            }
        }
        if (game_id) {
            this.appendGame(game_id, "");
            this.updatePlayers("players-for-" + game_id, String(players).split(","));
        }
        if (players && !game_id) {
            this.updatePlayers("players-list", String(players).split(","));
        }
    }
}