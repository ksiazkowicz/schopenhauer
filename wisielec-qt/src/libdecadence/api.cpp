#include "api.h"

SchopenhauerApi::SchopenhauerApi(QObject *parent) : QObject(parent)
{
    // initialize api things
    apiUrl = "127.0.0.1:8000";
    sessionToken = "";

    // and auth things
    auth = new SchopenhauerCookies();
    manager = auth->getManager();
    connect(auth, &SchopenhauerCookies::sessionFound, this, &SchopenhauerApi::setSessionToken);
    connect(manager, &QNetworkAccessManager::finished, this, &SchopenhauerApi::parseReply);

    this->getRanking();
}


void SchopenhauerApi::setSessionToken(QString token) {
    // don't invalidate anything unless token is different
    if (token != this->sessionToken) {
        this->sessionToken = token;
        emit updatedSessionData();
    }
}

QString SchopenhauerApi::getUrl(Protocol proto, QString path) {
    // we don't ignore token by default
    return this->getUrl(proto, path, false);
}

QString SchopenhauerApi::getUrl(Protocol proto, QString path, bool ignoreSessionToken) {
    /*
     * Returns API url with session key for specified protocol and path
    */
    QString baseUrl;
    // choose right protocol first
    switch (proto) {
    case Websocket: baseUrl = "ws://"; break;
    case Http: baseUrl = "http://"; break;
    case Https: baseUrl = "https://"; break;
    default: baseUrl = "http://";
    }

    // append defined api url
    baseUrl += apiUrl;

    // append path
    baseUrl += path;

    // check if session token is present
    if (!sessionToken.isEmpty() && !ignoreSessionToken) {
        return baseUrl + "?session_key=" + sessionToken;
    } else {
        // nope, so just go ahead
        return baseUrl;
    }
}

void SchopenhauerApi::attemptLogin(QString login, QString password) {
    qDebug() << "attempting login as" << login;
    // prepare form data
    QUrlQuery postData;
    postData.addQueryItem("username", login);
    postData.addQueryItem("password", password);
    auth->login = postData;
    // start login sequence
    auth->sendGetRequest(QUrl(getUrl(Http,"/profiles/login",true)));
}

void SchopenhauerApi::getRanking() {
    // call ranking API
    qDebug() << getUrl(Http, "/api/v1/ranking", true);
    manager->get(QNetworkRequest(QUrl(getUrl(Http, "/api/v1/ranking", true))));
}

void SchopenhauerApi::parseReply(QNetworkReply *reply) {
    QString content = reply->readAll();
    QJsonDocument jsonResponse = QJsonDocument::fromJson(content.toUtf8());
    QJsonObject jsonObject = jsonResponse.object();

    if (jsonObject.keys().contains("players")) {
        QJsonArray playersArray = jsonObject["players"].toArray();

        if (!playersArray.isEmpty()) {
            bestPlayers.clear();
            for (int i=0; i < playersArray.size(); i++) {
                QJsonObject playerJson = playersArray.at(i).toObject();
                RankingModel *player = new RankingModel();
                player->setUsername(playerJson["username"].toString());
                player->setScore((float)(playerJson["score"].toDouble()));
                player->setPosition(playerJson["position"].toInt());
                bestPlayers.append(player);
                qDebug() << playerJson["username"] << playerJson["score"] << playerJson["position"];
            }
            emit rankingChanged();
        }
        emit rankingChanged();
    }
}
