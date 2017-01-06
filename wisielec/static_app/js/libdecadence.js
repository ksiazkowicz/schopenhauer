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
    // lol add it laters
    alert(error_level + ": " + string);
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
                show_info_block("error", "Decadence failed to render template '"+template+"' with error '"+xhr.status+"'. Except stuff to be broken", false);
            }
        }
    };
    // send a request
    xhr.send("csrfmiddlewaretoken="+readCookie("csrftoken")+"&data="+JSON.stringify(data));
}
