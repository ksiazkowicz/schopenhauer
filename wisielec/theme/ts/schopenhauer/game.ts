import { replaceLink, query, queryInElement, ReconnectingWebsocketHandler } from "../modules/utils";
import { show_info_block, ErrorOptions, include_from_template } from "../modules/decadence";


export class SchopenhauerGame extends ReconnectingWebsocketHandler {
    letters: Array<Element>;
    session_id: string = "";
    keyboard_input: HTMLInputElement;
    mistakes: Element;

    used_letters: Array<string> = new Array<string>();
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
        this.mistakes = document.getElementById("mistakes");

        // callbacks
        this.keyboard_input.addEventListener("keypress", (evt: any) => {
            this.uniCharCode(evt);
        });
        if (screen.width <= 991) {
            this.keyboard_input.focus();
            this.keyboard_input.setAttribute("autofocus", "");
        }
        this.keyboard_input.addEventListener("focusout", (evt: any) => {
            if (screen.width > 991) {
                this.keyboard_input.focus();
                this.keyboard_input.setAttribute("autofocus", "");
            } else {
                this.keyboard_input.removeAttribute("autofocus");
            }
        });
        this.letters = queryInElement(f, "a");
        this.letters.map((e: Element) => {
            replaceLink(e, (url: string, element: Element) => {
                this.testLetter(element.innerHTML);
            })
        });
        this.connect();
    }

    updateLetters() {
        this.letters.map((e: Element) => {
            e.classList.toggle("disabled", this.used_letters.indexOf(e.innerHTML) != -1);
        })
    }

    onMessage(e: any) {
        var bread = JSON.parse(e.data);
        if (bread.redirect) {
            location.href = "/game/t/" + bread.tournament + "/";
        }

        if (bread.updates) {
            for (let update of bread.updates) {
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
                this.used_letters.push(bread.letter);
                this.updateLetters();
            }
            if (bread.used_chars) {
                this.used_letters = bread.used_chars.split('');
                this.updateLetters();
            }

            if (!bread.player_list_only) {
                if (this.score)
                    this.score.innerHTML = bread.score;
                if (this.mistakes)
                    this.mistakes.innerHTML = bread.mistakes;
                document.getElementById("progress").innerText = bread.progress;

                if (bread.hangman_pic) {
                    var img_mistakes = bread.hangman_pic < 5 ? bread.hangman_pic + 1 : 6;
                    document.getElementById("pikczer").setAttribute("src", "/static/img/hangman/0" + (img_mistakes) + ".png");
                }
            }
        }
    }
}