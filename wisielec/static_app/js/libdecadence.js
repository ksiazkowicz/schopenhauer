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