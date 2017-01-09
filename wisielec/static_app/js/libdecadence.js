var default_options = {"auto_dismissible": true, "dismiss_timeout": 4000};

function update_players(block_id, players) {
    var players_list = document.getElementById(block_id);
    if (players != "") {
        var new_players = "";
        for (var i=0; i<players.length; i++) {
            var player = players[i];
            new_players += "<a href='/profiles/view/" + player + "/'>" + player + "</a>";
            if (i != players.length - 1)
                new_players += ", ";
            players_list.innerHTML = new_players;
        }
    } else
        players_list.innerHTML = "nie żyją!";
}

function show_info_block(error_level, string, options) {
    /*
        Shows notification block at the top of the page.
     */
    // get date for alert ID
    var d = new Date();

    // prepare request
    var data = {
        "error_level": error_level, "string": string, "alert_id": d.getTime()
    };
    var template = "includes/decadence/alert_block.html";

    // check if options are defined
    if (options) {
        if (options.auto_dismissible) {
            // enable auto dismissing
            $(function() {
                setTimeout(function () {
                    $("#alert-"+data.alert_id).alert('close');
                }, options.dismiss_timeout);
            });
        }
        if (options.has_button) {
            data.has_button = true;
            data.button_text = options.button_text;
            data.button_href = options.button_href;
        }
        if (options.icon) {
            data.icon = options.icon;
        }
        if (options.custom_template) {
            // override template with provided in options
            template = options.custom_template
        }
        if (options.extra_data) {
            // if extra data is provided, replace data in data array
            var extra_keys = Object.keys(options.extra_data);
            for (var i=0; i<extra_keys.length; i++) {
                data[extra_keys[i]] = options.extra_data[extra_keys[i]];
            }
        }
    }

    // add block
    include_from_template("#body-alerts", template, data, "afterBegin");

    // we might want to have that one
    return data.alert_id
}

function fake_tournament_invite() {
    var options = {
        "has_button": true,
        "button_text": "Dołącz!",
        "button_href": "/game/t/test",
        "icon": "fa fa-trophy",
        "extra_data": { "tournament_name": "Fejkowe zaproszenie do turnieju", "username": "MrocznaPleśńŚmierci" },
        "custom_template": "includes/decadence/alerts/tournament_invite.html"
    };
    show_info_block("info", "", options)
}

function include_from_template(selector, template, data, mode) {
    /*
        Uses API to generate blocks from Django templates and includes them in the page.
        Takes css selector (like "#bread"), template file name ("includes/cancer.html") and context data.
        Also you can switch between different inclusion modes.

        wow, this is probably insecure as fuck
     */
    // create Ajax request
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/v1/decadence/template/', true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    data.template = template;

    // connect signal that gets fired up after request is finished
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // get block by css selector
                var block = document.querySelector(selector);

                // insert HTML
                block.insertAdjacentHTML(mode, xhr.responseText)
            } else {
                // stuff broke, show error
                show_info_block("danger", "Decadence failed to render template '"+template+"' with error '"+xhr.status+"'. Except stuff to be broken",
                default_options);
            }
        }
    };
    // send a request
    xhr.send("csrfmiddlewaretoken="+readCookie("csrftoken")+"&data="+JSON.stringify(data));
}

function create_game(modifiers, phrase) {
    /*
        Uses ajax to create a game with given parameters.
     */
    // create Ajax request
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/v1/game/create/', true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var data = "csrfmiddlewaretoken="+readCookie("csrftoken")+"&modifiers="+encodeURIComponent(modifiers);
    if (phrase)
        data += "&phrase="+encodeURIComponent(phrase);

    // connect signal that gets fired up after request is finished
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.session_id)
                    location.href = "/game/g/"+response.session_id;
            } else {
                // stuff broke, show error
                show_info_block("danger", "Stworzenie gry nie powiodło się, spróbuj ponownie.", default_options);
            }
        }
    };
    // send a request
    xhr.send(data);
}

function create_tournament(modifiers, name) {
    /*
        Uses ajax to create a game with given parameters.
     */
    // create Ajax request
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/v1/tournament/create/', true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    // connect signal that gets fired up after request is finished
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.session_id)
                    location.href = "/game/t/"+response.session_id;
            } else {
                // stuff broke, show error
                show_info_block("danger", "Stworzenie turnieju nie powiodło się, spróbuj ponownie.", default_options);
            }
        }
    };
    // send a request
    xhr.send("csrfmiddlewaretoken="+readCookie("csrftoken")+"&name="+encodeURIComponent(name)+"&modifiers="+encodeURIComponent(modifiers));
}

function new_round_tournament(session_id) {
    /*
        Uses ajax to create a new round.
     */
    // create Ajax request
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/v1/tournament/'+session_id+'/new_round/', true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    // connect signal that gets fired up after request is finished
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                show_info_block("success", "Utworzono nową rundę.", default_options);
            } else {
                // stuff broke, show error
                show_info_block("danger", "Dodanie użytkownika '" + username +"' do turnieju nie powiodło się.", default_options);
            }
        }
    };
    // send a request
    xhr.send("csrfmiddlewaretoken="+readCookie("csrftoken"));
}

function invite_to_tournament(session_id, username) {
    /*
        Uses ajax to invite user with specified username to tournament.
     */
    // create Ajax request
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/v1/tournament/'+session_id+'/invite/', true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    // connect signal that gets fired up after request is finished
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.session_id)
                    location.href = "/game/t/"+response.session_id;
                show_info_block("success", "Wysłano zaproszenie do użytkownika '" + username +"'.", default_options);
            } else {
                // stuff broke, show error
                show_info_block("danger", "Dodanie użytkownika '" + username +"' do turnieju nie powiodło się.", default_options);
            }
        }
    };

    // send a request
    xhr.send("csrfmiddlewaretoken="+readCookie("csrftoken")+"&username="+encodeURIComponent(username));
}