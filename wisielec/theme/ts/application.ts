// styles
import "../scss/main.scss";

// bootstrap plugins
import bootbox = require("bootbox");

import { SchopenhauerLobby } from "./schopenhauer/lobby";
import { SchopenhauerTournament } from "./schopenhauer/tournaments";
import { SchopenhauerGame } from "./schopenhauer/game";

import { csrfPOST, replaceLink, query, queryInElement, ReconnectingWebsocketHandler } from "./modules/utils";
import { include_from_template, ErrorOptions, show_info_block } from "./modules/decadence";

function fake_tournament_invite() {
    var options = new ErrorOptions({
        "has_button": true,
        "button_text": "Dołącz!",
        "button_href": "/game/t/test",
        "icon": "fa fa-trophy",
        "extra_data": { "tournament_name": "Fejkowe zaproszenie do turnieju", "username": "MrocznaPleśńŚmierci" },
        "custom_template": "includes/decadence/alerts/tournament_invite.html"
    });
    show_info_block("info", "", options)
}

function create_game(modifiers: any, name: string = "", tournament: boolean = false) {
    /*
        Uses ajax to create a game with given parameters.
     */

    csrfPOST("/api/v1/" + (tournament ? "tournament" : "game") + "/create/", {
        "modifiers": modifiers,
        "name": name,
    }).then((response) => {
        return response.json();
    }).then((response) => {
        if (response.session_id)
            location.href = "/game/" + (tournament ? "t" : "g") + "/" + response.session_id;
    }).catch((reason) => {
        show_info_block("danger", "Stworzenie gry nie powiodło się, spróbuj ponownie.", new ErrorOptions);
    });
}

class SchopenhauerChat extends ReconnectingWebsocketHandler {
    template: string = "<tr><td><a href='/profiles/view/[[ author ]]' style='font-weight: bold;'>[[ author ]]</a>: [[ message ]]</td></tr>";
    chat_block: Element;
    chat_input: HTMLInputElement;
    context: string = "";

    constructor(f: Element) {
        super();
        this.context = f.getAttribute("data-context");
        this.chat_block = queryInElement(f, ".chat-list")[0];
        this.chat_input = queryInElement(f, "input[type='text']")[0];

        queryInElement(f, "input[type='submit']").map((e: Element) => {
            e.addEventListener("click", (evt: any) => {
                this.sendMessage();
            })
        })
        this.chat_input.addEventListener("keypress", (evt: any) => {
            if (evt.keyCode == 13)
                this.sendMessage();
        })

        this.url = "/chat/" + this.context;
        this.connect();
    }

    sendMessage() {
        this.send({ "message": this.chat_input.value });
        this.chat_input.value = "";
    }

    onMessage(e: any) {
        var data = JSON.parse(e.data);
        // use API to insert a message into chat block
        include_from_template(this.chat_block, "includes/decadence/chat_message.html", {
            "author": data.author, "message": data.message
        }, "afterbegin");
    }
}

if (document.body.classList.contains("lobby")) {
    let lobby = new SchopenhauerLobby();
}

query(".schopenhauer-chat").map((element: Element) => {
    let chat = new SchopenhauerChat(element);
});

query(".schopenhauer-tournament").map((element: Element) => {
    let tournament = new SchopenhauerTournament(element);
});

query(".schopenhauer-game").map((element: Element) => {
    let game = new SchopenhauerGame(element);
})

let modifiers = "";
query(".modifier-button").map((button: Element) => {
    replaceLink(button, (url: string, element: Element) => {
        let modifier = element.getAttribute("data-modifier");
        if (modifier == "no_modifiers") {
            query(".mode").map((e: Element) => {
                e.classList.remove("current-mode");
            });
            modifiers = "";
        } else {
            document.getElementById("modifier-no_modifiers").classList.remove("current-mode");
            if (modifiers) {
                modifiers += ";";
            }
            modifiers += modifier;
        }
        document.getElementById("modifier-" + modifier).classList.add("current-mode");
    })
});

query("#new_game_button").map((button: Element) => {
    button.addEventListener("click", (evt: any) => {
        if (button.getAttribute("data-tournament")) {
            let name = (<HTMLInputElement>document.getElementById("name_input")).value;
            create_game(modifiers, name, true);
        } else {
            create_game(modifiers);
        }
    })
})


// tooltips
$('[data-toggle="tooltip"]').tooltip();
$().alert()