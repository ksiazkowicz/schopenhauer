#include "src/SchopenhauerClient.h"

SchopenhauerClient::SchopenhauerClient(QObject *parent) : QObject(parent)
{
    connect(&socket, &QWebSocket::connected, this, &SchopenhauerClient::onConnected);
    connect(&socket, &QWebSocket::disconnected, this, &SchopenhauerClient::onDisconnected);
    socket.open(QUrl("ws://127.0.0.1:8000/guess/"));
    lobby_socket.open(QUrl("ws://127.0.0.1:8000/lobby/"));

    session_id = "2ec39b80911911e6a00f68f728f88948";
}

void SchopenhauerClient::onConnected()
{
    qDebug() << "WebSocket connected";
    connect(&socket, &QWebSocket::textMessageReceived,
            this, &SchopenhauerClient::onContentReceived);
    connect(&lobby_socket, &QWebSocket::textMessageReceived,
            this, &SchopenhauerClient::onLobbyContentReceived);

    this->guess_letter("a");
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

void SchopenhauerClient::onLobbyContentReceived(QString message)
{
    qDebug() << "Message received:" << message;

    QJsonDocument jsonResponse = QJsonDocument::fromJson(message.toUtf8());
    QJsonObject jsonObject = jsonResponse.object();

    qDebug() << (jsonObject["session_id"].toString() == session_id);
    qDebug() << jsonObject.keys();

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
