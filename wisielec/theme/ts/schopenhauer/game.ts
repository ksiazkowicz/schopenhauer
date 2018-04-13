import { replaceLink, query, queryInElement, ReconnectingWebsocketHandler } from "../modules/utils";
import { show_info_block, ErrorOptions, include_from_template } from "../modules/decadence";

function update_players(block_id: any, players: any) {
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

export class SchopenhauerGame extends ReconnectingWebsocketHandler {
    session_id: string = "";
    keyboard_input: Element;
    score: Element;

    testLetter(letter: string) {
        this.send({
            session_id: this.session_id,
            letter: letter
        });
    }

    uniCharCode(event: any) {
        var char = event.which || event.keyCode; // event.keyCode is used for IE8 and earlier
        this.testLetter(String.fromCharCode(char));
    }

    constructor(f: Element) {
        super();
        this.session_id = f.getAttribute("data-game");
        this.url = "/game/" + this.session_id;

        // capture all the elements
        this.keyboard_input = query(".keyboard-input")[0];
        this.score = document.getElementById("score");

        // callbacks
        this.keyboard_input.addEventListener("keypress", (evt: any) => {
            this.uniCharCode(evt);
        });
        this.keyboard_input.addEventListener("focusout", function (evt: any) {
            this.focus();
        });
        queryInElement(f, "a").map((e: Element) => {
            replaceLink(e, (url: string, element: Element) => {
                this.testLetter(element.innerHTML);
            })
        });
        this.connect();
    }

    onMessage(e: any) {
        var bread = JSON.parse(e.data);
        if (bread.redirect) {
            location.href = "/game/t/" + bread.tournament + "/";
        }

        if (bread.updates) {
            for (i = 0; i < bread.updates.length; i++) {
                var update = bread.updates[i];
                if (document.getElementById("game-" + update.session_id)) {
                    document.getElementById("game-mistakes-" + update.session_id).innerText = update.mistakes;
                    document.getElementById("game-progress-" + update.session_id).innerText = "(" + update.progress + ")";
                } else {
                    alert("NOT_IMPLEMENTED");
                }
            }
        }

        if (bread.session_id == this.session_id) {
            if (bread.letter) {
                document.getElementById("used_letters").innerHTML += bread.letter + ", ";
            }
            if (bread.used_chars) {
                document.getElementById("used_letters").innerHTML = "Wykorzystane literki: "
                for (var i = 0; i < bread.used_chars.length; i++) {
                    document.getElementById("used_letters").innerHTML += bread.used_chars[i] + ", ";
                }
            }
            if (bread.players)
                update_players("players-list", bread.players);

            if (!bread.player_list_only) {
                this.score.innerHTML = bread.score;
                document.getElementById("mistakes").innerText = bread.mistakes;
                document.getElementById("progress").innerText = bread.progress;

                if (bread.hangman_pic) {
                    var img_mistakes = bread.hangman_pic < 5 ? bread.hangman_pic + 1 : 6;
                    document.getElementById("pikczer").setAttribute("src", "/static/img/wis0" + (img_mistakes) + ".png");
                }
            }
        }
    }
}