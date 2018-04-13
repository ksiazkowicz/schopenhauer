import { csrfPOST, ajaxGET, ReconnectingWebsocketHandler } from "../modules/utils";
import { show_info_block, ErrorOptions, include_from_template } from "../modules/decadence";


export class SchopenhauerTournament extends ReconnectingWebsocketHandler {
    player: string;
    tournament: string;

    invite(username: any) {
        /*
            Uses ajax to invite user with specified username to tournament.
         */
        csrfPOST("/api/v1/tournament/" + this.tournament + "/invite/", {
            "username": username
        }).then((response) => {
            return response.json();
        }).then((json) => {
            if (json.session_id)
                location.href = "/game/t/" + json.session_id;
            show_info_block("success", "Wysłano zaproszenie do użytkownika '" + username + "'.", new ErrorOptions);
        }).catch((reason) => {
            show_info_block("danger", "Dodanie użytkownika '" + username + "' do turnieju nie powiodło się.", new ErrorOptions);
        });
    }

    newRound() {
        /*
            Uses ajax to create a new round.
        */
        csrfPOST("/api/v1/tournament/" + this.tournament + "/new_round/", {

        }).then((response) => {
            return response.json();
        }).then((json) => {
            show_info_block("success", "Utworzono nową rundę.", new ErrorOptions);
        }).catch((reason) => {
            show_info_block("danger", "Stworzenie nowej rundy nie powiodło się.", new ErrorOptions);
        });
    }

    constructor(f: any) {
        super();
        this.tournament = f.getAttribute("data-tournament", "");
        this.player = f.getAttribute("data-player", "");
        this.url = "/tournament/" + this.tournament;
        this.connect();

        document.getElementById("invite_button").onclick = () => {
            var username = (<HTMLInputElement>document.getElementById("invite_name_input")).value;
            this.invite(username);
        };
        document.getElementById("new_round_button").onclick = () => {
            this.newRound();
        };
    }

    onMessage(e: any) {
        let bread = JSON.parse(e.data);
        if (bread["redirect"] && bread["player"] == this.player)
            location.href = "/game/g/" + bread["game"] + "/";
    }
}