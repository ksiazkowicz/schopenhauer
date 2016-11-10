#include "src/SchopenhauerClient.h"


SchopenhauerClient::SchopenhauerClient(QObject *parent) : QObject(parent)
{
    api_url = "0.tcp.ngrok.io:12928";
    connect(&socket, &QWebSocket::connected, this, &SchopenhauerClient::onConnected);
    connect(&socket, &QWebSocket::disconnected, this, &SchopenhauerClient::onDisconnected);
    connect(&socket, &QWebSocket::textMessageReceived,
            this, &SchopenhauerClient::onContentReceived);
    connect(&lobby_socket, &QWebSocket::textMessageReceived,
            this, &SchopenhauerClient::onLobbyContentReceived);
    connect(&lobby_socket, &QWebSocket::connected, this, &SchopenhauerClient::onConnected);
    connect(&lobby_socket, &QWebSocket::disconnected, this, &SchopenhauerClient::onDisconnected);
    connect(&lobby_socket, &QWebSocket::stateChanged, this, &SchopenhauerClient::onStateChanged);
    lobby_socket.open(QUrl("ws://"+api_url+"/lobby/"));

    session_id = "";
}

void SchopenhauerClient::onConnected()
{
    qDebug() << "WebSocket connected";
}

void SchopenhauerClient::onStateChanged(QAbstractSocket::SocketState state) {
    qDebug() << "socket jest na" << state;
    QWebSocket* socket = (QWebSocket*)QObject::sender();
    qDebug() << socket->errorString();
}

void SchopenhauerClient::refresh_lobby() {
    lobby_socket.close(); lobby_socket.open(QUrl("ws://"+api_url+"/lobby/"));
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
    socket.open(QUrl("ws://"+api_url+"/game/" + this->session_id));
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

    if (jsonObject.keys().contains("new")) {
        bool dupy = jsonObject["new"].toBool();
        if (dupy) {
            QString game = jsonObject["session_id"].toString();
            if (!games.contains(game)) {
                games.append(game);
            }
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
