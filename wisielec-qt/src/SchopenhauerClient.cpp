#include "src/SchopenhauerClient.h"

SchopenhauerClient::SchopenhauerClient(QObject *parent) : QObject(parent)
{
    connect(&socket, &QWebSocket::connected, this, &SchopenhauerClient::onConnected);
    connect(&socket, &QWebSocket::disconnected, this, &SchopenhauerClient::onDisconnected);
    socket.open(QUrl("ws://127.0.0.1:8000/game/"));
    lobby_socket.open(QUrl("ws://127.0.0.1:8000/lobby/"));

    session_id = "2ec39b80911911e6a00f68f728f88948";
    games.append("artur szopenhauer krulem rzycia");
}

void SchopenhauerClient::onConnected()
{
    qDebug() << "WebSocket connected";
    connect(&socket, &QWebSocket::textMessageReceived,
            this, &SchopenhauerClient::onContentReceived);
    connect(&lobby_socket, &QWebSocket::textMessageReceived,
            this, &SchopenhauerClient::onLobbyContentReceived);

    this->join_game(this->session_id);
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

    QJsonObject request;
    request["session_id"] = this->session_id;
    request["action"] = "join";

    QJsonDocument doc(request);
    lobby_socket.sendTextMessage(doc.toJson(QJsonDocument::Compact));
}

void SchopenhauerClient::new_game() {
    this->session_id = "";
    QJsonObject request;
    request["session_id"] = "";
    request["action"] = "new";

    QJsonDocument doc(request);
    lobby_socket.sendTextMessage(doc.toJson(QJsonDocument::Compact));
}

void SchopenhauerClient::onDisconnected()
{
    qDebug() << "WebSocket disconnected";
}

void SchopenhauerClient::onContentReceived(QString message)
{
    qDebug() << "Message received:" << message;

    QJsonDocument jsonResponse = QJsonDocument::fromJson(message.toUtf8());
    QJsonObject jsonObject = jsonResponse.object();

    qDebug() << (jsonObject["session_id"].toString() == session_id);
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

    qDebug() << (jsonObject["session_id"].toString() == session_id);
    qDebug() << jsonObject.keys();

    if (jsonObject.keys().contains("running_games")) {
        QJsonArray running_games = jsonObject["running_games"].toArray();
        qDebug() << running_games;

        if (!running_games.isEmpty()) {
            for (int i=0; i < running_games.size(); i++) {
                QString game = running_games.at(i).toString();
                if (!games.contains(game)) {
                    games.append(game);
                }
            }
            qDebug() << games;
            emit games_changed();
        }
    }

    if (jsonObject["session_id"].toString() == session_id) {
        progress = jsonObject["progress"].toString();
        score = jsonObject["score"].toInt();
        mistakes = jsonObject["mistakes"].toInt();
        qDebug() << jsonObject["used_chars"].toArray();
        emit progress_changed();
        emit score_changed();
        emit mistakes_changed();
    }
}
