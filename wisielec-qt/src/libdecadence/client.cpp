#include "client.h"

SchopenhauerClient::SchopenhauerClient(SchopenhauerApi *api, QObject *parent) : QObject(parent)
{
    // initialize API
    this->api = api;
    connect(api, &SchopenhauerApi::updatedSessionData, this, &SchopenhauerClient::invalidateSockets);
    connect(api, &SchopenhauerApi::foundTournaments, this, &SchopenhauerClient::parseTournaments);

    // connect sockets to signals and slots
    connect(&socket, &QWebSocket::textMessageReceived,
            this, &SchopenhauerClient::onContentReceived);
    connect(&lobby_socket, &QWebSocket::textMessageReceived,
            this, &SchopenhauerClient::onLobbyContentReceived);
    connect(&lobby_socket, &QWebSocket::stateChanged, this, &SchopenhauerClient::onStateChanged);
    connect(&socket, &QWebSocket::stateChanged, this, &SchopenhauerClient::onStateChanged);

    // connect to lobby
    //this->refresh_lobby();
}

void SchopenhauerClient::onStateChanged(QAbstractSocket::SocketState state) {
    qDebug() << "socket jest na" << state;
    QWebSocket* socket = (QWebSocket*)QObject::sender();
    if (socket->error() != QAbstractSocket::UnknownSocketError)
        qDebug() << socket->errorString();
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
    socket.close();
    socket.open(QUrl(api->getUrl(SchopenhauerApi::Websocket,"/game/" + this->session_id +"/")));
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

    if (jsonObject["session_id"].toString() != "") {
        if (this->session_id == "") {
            if (jsonObject["new"].toBool())
                this->session_id = jsonObject["session_id"].toString();
        }

        if (jsonObject["session_id"].toString() == session_id) {
            progress = jsonObject["progress"].toString();
            score = jsonObject["score"].toInt();
            QString letter = jsonObject["letter"].toString();
            mistakes = jsonObject["mistakes"].toInt();
            used_chars.append(letter);
            emit progress_changed();
            emit score_changed();
            emit mistakes_changed();
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
                QString game = running_games.at(i).toString();
                GameModel *gameObj = new GameModel();
                gameObj->setSessionId(game);
                games.insert(game, gameObj);
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
}

void SchopenhauerClient::parseTournaments(QString reply) {
    // parse reply as JSON document
    QJsonDocument jsonResponse = QJsonDocument::fromJson(reply.toUtf8());
    QJsonObject jsonObject = jsonResponse.object();

    // reset tournament map
    tournaments.clear();

    // iterate through all tournaments in array
    QJsonArray array = jsonObject["tournaments"].toArray();
    for (int i=0; i<array.size(); i++) {
        // get json for specific position
        QJsonObject json = array.at(i).toObject();

        // create new tournament object
        TournamentModel* tournament = new TournamentModel();

        // move session id to another string, cause we're going to use it as key later
        QString sessionId = json["session_id"].toString();

        // add values from JSON to our model
        tournament->setName(json["name"].toString());
        tournament->setSessionId(sessionId);
        tournament->setInProgress(json["in_progress"].toBool());

        // parse players array
        QJsonArray players = json["players"].toArray();
        QStringList playerList;
        for (int i=0; i < players.size(); i++) {
            playerList.append(players.at(i).toString());
        }

        // set players list
        tournament->setPlayerList(playerList);
        qDebug() << playerList;

        // add to our map and push out a signal
        tournaments.insert(sessionId, tournament);
        emit tournamentsChanged();
    }
}
