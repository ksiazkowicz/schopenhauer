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

function generate_from_template(template, data) {
    /*
    Takes template and fills it with given data.
    Takes:
        - template - string, defined like this: <p>[[ bread ]] is kinda awesome</p>
        - data - js object, defined like this: { "bread": "Myself", }

    Returns a string with all tags replaced with strings from JSON object.
     */
    // get all keys from JS object
    var keys = Object.keys(data);
    // copy given template
    var new_template = template;

    // replace every occurrence of each [[ key ]] with object data
    for (var i=0; i<keys.length; i++) {
        // find all occurrences
        while (new_template.indexOf(keys[i]) != -1)
            // replace
            new_template = new_template.replace("[[ "+keys[i]+" ]]", data[keys[i]]);
    }

    return new_template;
}
