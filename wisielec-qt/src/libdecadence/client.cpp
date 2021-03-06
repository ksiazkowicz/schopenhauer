#include "client.h"

SchopenhauerClient::SchopenhauerClient(SchopenhauerApi *api, QObject *parent) : QObject(parent)
{
    // initialize API
    this->api = api;
    connect(api, &SchopenhauerApi::updatedSessionData, this, &SchopenhauerClient::invalidateSockets);
    connect(api, &SchopenhauerApi::foundTournaments, this, &SchopenhauerClient::parseTournaments);
    connect(api, &SchopenhauerApi::tournamentEnded, this, &SchopenhauerClient::endTournament);
    connect(api, &SchopenhauerApi::tournamentRoundsFound, this, &SchopenhauerClient::parseRounds);
    connect(api, &SchopenhauerApi::tournamentScoresFound, this, &SchopenhauerClient::parseScoreboard);
    connect(api, &SchopenhauerApi::gameInfoFound, this, &SchopenhauerClient::updateGameInfo);

    // connect sockets to signals and slots
    connect(&socket, &QWebSocket::textMessageReceived,
            this, &SchopenhauerClient::onContentReceived);
    connect(&lobby_socket, &QWebSocket::textMessageReceived,
            this, &SchopenhauerClient::onLobbyContentReceived);
    connect(&lobby_socket, &QWebSocket::stateChanged, this, &SchopenhauerClient::onStateChanged);
    connect(&socket, &QWebSocket::stateChanged, this, &SchopenhauerClient::onStateChanged);

    // enable chat
    currentChatRoom = "";
    connect(&chat_socket, &QWebSocket::textMessageReceived, this, &SchopenhauerClient::onChatContentReceived);
    connect(&chat_socket, &QWebSocket::stateChanged, this, &SchopenhauerClient::onStateChanged);

    // enable tournaments
    currentTournamentId = "";
    connect(&tournament_socket, &QWebSocket::textMessageReceived, this, &SchopenhauerClient::onTournamentContentReceived);
    connect(&tournament_socket, &QWebSocket::stateChanged, this, &SchopenhauerClient::onStateChanged);

    // connect to lobby
    //this->refresh_lobby();
}

void SchopenhauerClient::onStateChanged(QAbstractSocket::SocketState state) {
    //qDebug() << "socket jest na" << state;
    /*QWebSocket* socket = (QWebSocket*)QObject::sender();
    if (socket->error() != QAbstractSocket::UnknownSocketError)
        qDebug() << socket->errorString();*/
}

void SchopenhauerClient::refresh_lobby() {
    /*
     *  Reconnect to lobby.
     *
     */
    lobby_socket.close();
    lobby_socket.open(QUrl(api->getUrl(SchopenhauerApi::Websocket, "/lobby/")));
}


void SchopenhauerClient::guess_letter(QString letter) {
    QJsonObject request;
    request["session_id"] = this->session_id;
    request["letter"] = letter;

    QJsonDocument doc(request);
    socket.sendTextMessage(doc.toJson(QJsonDocument::Compact));
}

void SchopenhauerClient::join_game(QString _new_id) {
    this->session_id = _new_id;
    this->otherGames.clear();
    api->getGameInfo(_new_id);
    qDebug() << this->session_id;
    socket.close();
    socket.open(QUrl(api->getUrl(SchopenhauerApi::Websocket,"/game/" + this->session_id)));
}

void SchopenhauerClient::new_game() {
    this->session_id = "";
    QJsonObject request;
    request["session_id"] = "";
    request["action"] = "new";

    QJsonDocument doc(request);
    lobby_socket.sendTextMessage(doc.toJson(QJsonDocument::Compact));
}

void SchopenhauerClient::onContentReceived(QString message)
{
    qDebug() << "Message received:" << message;

    QJsonDocument jsonResponse = QJsonDocument::fromJson(message.toUtf8());
    QJsonObject jsonObject = jsonResponse.object();

    qDebug() << jsonObject.keys();

    if (jsonObject["tournament"].toString() == currentTournamentId && !currentTournamentId.isEmpty()) {
        if (jsonObject["redirect"].toBool())
            emit roundEnded();
    }

    if (jsonObject["session_id"].toString() != "") {
        if (this->session_id == "") {
            if (jsonObject["new"].toBool())
                this->session_id = jsonObject["session_id"].toString();
        }

        if (jsonObject["session_id"].toString() == session_id) {
            if (jsonObject.keys().contains("progress")) {
                progress = jsonObject["progress"].toString();
                score = jsonObject["score"].toInt();
                QString letter = jsonObject["letter"].toString();
                mistakes = jsonObject["mistakes"].toInt();
                hangmanPic = jsonObject["hangman_pic"].toInt();
                used_chars.append(letter);
                QString progress_string = jsonObject["progress_string"].toString();
                this->setOtherGame(api->getUser()->getUsername(), progress_string, mistakes);
                emit progress_changed();
                emit score_changed();
                emit mistakes_changed();
                emit hangmanChanged();

                QString state = jsonObject["state"].toString();
                if (state == "WIN")
                    emit gameEnded(true);
                else if (state == "FAIL")
                    emit gameEnded(false);
            }
        }
    }
    if (jsonObject.keys().contains("updates")) {
        QJsonArray updates = jsonObject["updates"].toArray();
        for (int i=0; i<updates.count(); i++) {
            QJsonObject update = updates.at(i).toObject();
            QString username = update["player"].toString();
            QString progress = update["progress"].toString();
            int mistakes = update["mistakes"].toInt();
            this->setOtherGame(username, progress, mistakes);
        }
    }
}

void SchopenhauerClient::onLobbyContentReceived(QString message)
{
    qDebug() << "Message received:" << message;

    QJsonDocument jsonResponse = QJsonDocument::fromJson(message.toUtf8());
    QJsonObject jsonObject = jsonResponse.object();

    qDebug() << jsonObject.keys();

    if (jsonObject.keys().contains("players")) {
        QJsonArray players = jsonObject["players"].toArray();
        QStringList playerList;
        for (int i=0; i < players.size(); i++) {
            playerList.append(players.at(i).toString());
        }
        if (jsonObject.keys().contains("session_id")) {
            QString sessionId = jsonObject["session_id"].toString();
            GameModel *game = (GameModel*)games.value(sessionId);
            if (game)
                game->setPlayerList(playerList);
        } else {
            this->lobbyPlayers = playerList;
            emit lobbyPlayersChanged();
        }
    }

    if (jsonObject.keys().contains("running_games")) {
        QJsonArray running_games = jsonObject["running_games"].toArray();

        if (!running_games.isEmpty()) {
            games.clear();
            for (int i=0; i < running_games.size(); i++) {
                QJsonObject game = running_games.at(i).toObject();
                QString game_id = game["session_id"].toString();
                QString progress = game["progress"].toString();
                GameModel *gameObj = new GameModel();
                gameObj->setSessionId(game_id);
                gameObj->setProgress(progress);
                games.insert(game_id, gameObj);
            }
            emit games_changed();
        }
    }

    if (jsonObject.keys().contains("new")) {
        bool dupy = jsonObject["new"].toBool();
        if (dupy) {
            QString game = jsonObject["session_id"].toString();
            GameModel *gameObj = new GameModel();
            gameObj->setSessionId(game);
            games.insert(game, gameObj);
            emit games_changed();
        }
    }

    if (jsonObject["session_id"].toString() == session_id) {
        progress = jsonObject["progress"].toString();
        score = jsonObject["score"].toInt();
        mistakes = jsonObject["mistakes"].toInt();
        emit progress_changed();
        emit score_changed();
        emit mistakes_changed();
    }
}

void SchopenhauerClient::invalidateSockets() {
    qDebug() << "Invalidating sockets";
    this->refresh_lobby();
    this->switchChatChannel(currentChatRoom);
    this->leaveTournament();
}

void SchopenhauerClient::parseTournaments(QString reply) {
    // parse reply as JSON document
    QJsonDocument jsonResponse = QJsonDocument::fromJson(reply.toUtf8());
    QJsonObject jsonObject = jsonResponse.object();

    // iterate through all tournaments in array
    QJsonArray array = jsonObject["tournaments"].toArray();
    for (int i=0; i<array.size(); i++) {
        // get json for specific position
        QJsonObject json = array.at(i).toObject();

        // move session id to another string, cause we're going to use it as key later
        QString sessionId = json["session_id"].toString();

        TournamentModel* tournament = 0;
        // check if already exists and create new one if doesn't
        if (tournaments.keys().contains(sessionId)) {
            tournament = (TournamentModel*)tournaments.value(sessionId);
        } else {
            tournament = new TournamentModel();
            tournaments.insert(sessionId, tournament);
        }

        // add values from JSON to our model
        tournament->setName(json["name"].toString());
        tournament->setSessionId(sessionId);
        tournament->setInProgress(json["in_progress"].toBool());
        tournament->setModes(json["modes"].toString());

        // parse players array
        QJsonArray players = json["players"].toArray();
        for (int i=0; i < players.size(); i++) {
            tournament->setPlayer(players.at(i).toString(), 0, false, true);
        }

        // push signal
        emit tournamentsChanged();

        // update tournament view
        if (sessionId == currentTournamentId)
            emit tournamentInfoFound();
    }
}

void SchopenhauerClient::sendChatMessage(QString message_text) {
    chat_socket.sendTextMessage(message_text);
}

void SchopenhauerClient::onChatContentReceived(QString message) {
    // parse content as JSON
    QJsonDocument jsonResponse = QJsonDocument::fromJson(message.toUtf8());
    QJsonObject jsonObject = jsonResponse.object();

    // create chat message object if request is valid
    if (jsonObject.keys().contains("author") && jsonObject.keys().contains("message")) {
        ChatMessageModel* chatMessage = new ChatMessageModel();
        chatMessage->setUsername(jsonObject["author"].toString());
        chatMessage->setMessage(jsonObject["message"].toString());

        chatMessages.append(chatMessage);
        emit chatMessagesChanged();
    }
}

void SchopenhauerClient::switchChatChannel(QString channel) {
    // ignore if we're in that channel unless our socket is dead
    if (currentChatRoom != channel || chat_socket.state() != QAbstractSocket::ConnectedState) {
        // clear current message queue
        chatMessages.clear();
        emit chatMessagesChanged();

        // change current channel name
        currentChatRoom = channel;
        emit channelNameChanged();

        // reconnect
        chat_socket.close();
        chat_socket.open(QUrl(api->getUrl(SchopenhauerApi::Websocket, "/chat/"+channel)));
    }
}

QString SchopenhauerClient::getChannelName() {
    // returns verbose name of chat context
    if (currentChatRoom == "lobby") {
        return "Lobby";
    } else if (currentChatRoom.startsWith("tournament-")) {
        return "Turniej";
    } else {
        // lol stub
        return currentChatRoom;
    }
}

void SchopenhauerClient::joinTournament(QString sessionId) {
    // ask API for some things
    api->getTournamentList();
    api->getTournamentRounds(sessionId);
    api->getTournamentScoreboard(sessionId);

    // swtich channel to tournament chat
    this->switchChatChannel("tournament-" + sessionId);

    // update session id
    currentTournamentId = sessionId;

    // connect to tournament lobby
    tournament_socket.open(QUrl(api->getUrl(SchopenhauerApi::Websocket, "/tournament/"+sessionId)));
}

void SchopenhauerClient::leaveTournament() {
    // return to lobby
    this->switchChatChannel("lobby");

    currentTournamentId = "";
    tournament_socket.close();
}

QString SchopenhauerClient::currentTournamentName() {
    if (tournaments.keys().contains(currentTournamentId)) {
        return ((TournamentModel*)(tournaments.value(currentTournamentId)))->getName();
    } else return "Ładowanie...";
}

QString SchopenhauerClient::currentTournamentModes() {
    if (tournaments.keys().contains(currentTournamentId)) {
        return ((TournamentModel*)(tournaments.value(currentTournamentId)))->getModes();
    } else return "Ładowanie...";
}

void SchopenhauerClient::onTournamentContentReceived(QString message) {
    // parse content as JSON
    QJsonDocument jsonResponse = QJsonDocument::fromJson(message.toUtf8());
    QJsonObject jsonObject = jsonResponse.object();

    // if redirect, join the game
    if (jsonObject.keys().contains("redirect")) {
        // check if it's meant for us
        QString username = api->getUser()->getUsername();
        if (jsonObject["player"].toString() == username) {
            // yeah, let's push it
            QString sessionId = jsonObject["game"].toString();
            emit gameFound(sessionId);
        }
    }
}

void SchopenhauerClient::endTournament(QString sessionId, QString winner, int roundCount) {
    // check if tournament is on our list
    if (tournaments.keys().contains(sessionId)) {
        // sure, let's begin doing weird things
        TournamentModel *tournament = ((TournamentModel*)(tournaments.value(sessionId)));
        tournament->setInProgress(false);
        tournament->setWinner(winner);
    }
}

TournamentModel* SchopenhauerClient::getCurrentTournament() {
    if (tournaments.keys().contains(currentTournamentId)) {
        return (TournamentModel*)(tournaments.value(currentTournamentId));
    } else return 0;
}

void SchopenhauerClient::parseScoreboard(QString reply) {
    // parse reply as JSON document
    QJsonDocument jsonResponse = QJsonDocument::fromJson(reply.toUtf8());
    QJsonObject jsonObject = jsonResponse.object();

    QString sessionId = jsonObject["session_id"].toString();

    // check if tournament exists
    if (tournaments.keys().contains(sessionId)) {
        TournamentModel *tournament = ((TournamentModel*)(tournaments.value(sessionId)));

        // save winner username for reference
        QString winner = jsonObject["winner"].toString();

        // parse the list of players
        QJsonArray players = jsonObject["players"].toArray();
        for (int i=0; i < players.size(); i++) {
            // get player json
            QJsonObject player = players.at(i).toObject();
            QString username = player["username"].toString();
            int score = player["score"].toInt();

            // update scoreboard
            tournament->setPlayer(username, score, winner == username, false);
        }
    }
}


void SchopenhauerClient::parseRounds(QString reply) {
    // parse reply as JSON document
    QJsonDocument jsonResponse = QJsonDocument::fromJson(reply.toUtf8());
    QJsonObject jsonObject = jsonResponse.object();

    QString sessionId = jsonObject["session_id"].toString();

    // check if tournament exists
    if (tournaments.keys().contains(sessionId)) {
        TournamentModel *tournament = ((TournamentModel*)(tournaments.value(sessionId)));

        // parse the list of rounds
        QJsonArray rounds = jsonObject["rounds"].toArray();
        for (int i=0; i < rounds.size(); i++) {
            // get round json
            QJsonObject round = rounds.at(i).toObject();
            QString status = round["status"].toString();
            QString winner = round["winner"].toString();
            int pk = round["id"].toInt();
            // update round
            tournament->updateRound(pk, status, winner);

            // iterate through all games and add them too
            QJsonArray games = round["games"].toArray();
            for (int i=0; i < games.size(); i++) {
                QJsonObject game = games.at(i).toObject();
                QString sessionId = game["session_id"].toString();
                QString player = game["player"].toString();
                // update game
                tournament->updateRoundGame(pk, sessionId, player);
            }
        }
    }
}

void SchopenhauerClient::updateGameInfo(QString reply) {
    // parse reply as JSON document
    QJsonDocument jsonResponse = QJsonDocument::fromJson(reply.toUtf8());
    QJsonObject jsonObject = jsonResponse.object();

    QString sessionId = jsonObject["session_id"].toString();

    if (sessionId == this->session_id) {
        this->progress = jsonObject["progress"].toString();
        this->score = jsonObject["score"].toInt();
        this->mistakes = jsonObject["mistakes"].toInt();
        this->hangmanPic = this->mistakes;
        QString progress_string = jsonObject["progress_string"].toString();
        this->setOtherGame(api->getUser()->getUsername(), progress_string, mistakes);
        emit score_changed();
        emit progress_changed();
        emit score_changed();
        emit hangmanChanged();
        if (jsonObject.keys().contains("other_games")) {
            QJsonArray arrayOfGames = jsonObject["other_games"].toArray();
            for (int i=0; i<arrayOfGames.count(); i++) {
                QJsonObject game = arrayOfGames.at(i).toObject();
                QString username = game["username"].toString();
                QString progress = game["progress"].toString();
                int mistakes = game["mistakes"].toInt();
                this->setOtherGame(username, progress, mistakes);
            }
        }
    }
}
