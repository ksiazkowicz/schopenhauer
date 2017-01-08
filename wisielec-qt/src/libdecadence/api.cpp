#include "api.h"

SchopenhauerApi::SchopenhauerApi(Settings *appSettings, QObject *parent) : QObject(parent)
{
    // initialize api things
    apiUrl = "127.0.0.1:8000";
    //apiUrl = "schopenhauer.krojony.pl";
    sessionToken = "";

    // and auth things
    auth = new SchopenhauerCookies();
    manager = auth->getManager();
    connect(auth, &SchopenhauerCookies::sessionFound, this, &SchopenhauerApi::setSessionToken);
    connect(auth, &SchopenhauerCookies::authFailed, this, &SchopenhauerApi::handleFailure);
    connect(manager, &QNetworkAccessManager::finished, this, &SchopenhauerApi::parseReply);

    // user stuff
    me = new UserModel();
    viewedUser = new UserModel();

    tempUsername = "";

    // use app settings
    settings = appSettings;
    if (settings->authCredentialsPresent()) {
        // token present, attempt login
        expectedUsername = settings->getUsername();
        this->setSessionToken(settings->getAuthToken());
    }
}


void SchopenhauerApi::setSessionToken(QString token) {
    // save credentials if not present
    if (!settings->authCredentialsPresent()) {
        settings->setAuthToken(token);
        settings->setUsername(expectedUsername);
    }

    // don't invalidate anything unless token is different
    if (token != this->sessionToken) {
        this->sessionToken = token;
        this->getUserData();
        this->getTournamentList();
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
    postData.addQueryItem("login", login);
    postData.addQueryItem("password", password);
    auth->login = postData;

    // to make sure we're authed, keep login for reference
    expectedUsername = login;

    // start login sequence
    auth->sendGetRequest(QUrl(getUrl(Http,"/accounts/login/?headless=1",true)));
}

void SchopenhauerApi::getRanking() {
    // call ranking API
    manager->get(QNetworkRequest(QUrl(getUrl(Http, "/api/v1/ranking/", true))));
}

void SchopenhauerApi::parseReply(QNetworkReply *reply) {
    QString content = reply->readAll();
    QJsonDocument jsonResponse = QJsonDocument::fromJson(content.toUtf8());
    QJsonObject jsonObject = jsonResponse.object();

    qDebug() << content;

    if (jsonObject.keys().contains("result")) {
        qDebug() << "REZULTNELO SIE UWAGA ------------";
        qDebug() << jsonObject["result"].toString();
        emit omgToDziala();
        this->getTournamentList();
        qDebug() << "no dzienki";
    }

    if (jsonObject.keys().contains("tournaments") && reply->url().toString().contains("/api/v1/tournament")) {
        emit foundTournaments(content);
    }

    if (jsonObject.keys().contains("username")) {
        UserModel* user;

        bool updatingMe = false;
        if (reply->url().toString().contains("/user/"+tempUsername) && !tempUsername.isEmpty()) {
            user = viewedUser;
            tempUsername = "";
        } else {
            user = me;
            updatingMe = true;
        }

        if (jsonObject["authenticated"].toBool()) {
            user->setUsername(jsonObject["username"].toString());
            user->setAvatar(jsonObject["avatar"].toString());
            user->setScore(jsonObject["score"].toDouble());
            user->setPosition(jsonObject["position"].toInt());
            user->setWonGames(jsonObject["won_games"].toInt());
            user->setLostGames(jsonObject["lost_games"].toInt());
            user->setWonTournaments(jsonObject["won_tournaments"].toInt());
            user->setLostTournaments(jsonObject["lost_tournaments"].toInt());
        } else {
            user->reset();
        }

        if (!expectedUsername.isEmpty()) {
            if (user->getUsername() == expectedUsername)
                emit authSuccess();
            else handleFailure("Token jest nieprawidłowy. Spróbuj zalogować się ponownie.");
            expectedUsername = "";
        }

        emit userChanged();
        emit viewedUserChanged();
    }

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

void SchopenhauerApi::getUserData() {
    manager->get(QNetworkRequest(QUrl(getUrl(Http, "/api/v1/user/", true))));
}

void SchopenhauerApi::getUserData(QString username) {
    tempUsername = username;
    manager->get(QNetworkRequest(QUrl(getUrl(Http, "/api/v1/user/"+username, true))));
}

void SchopenhauerApi::getTournamentList() {
    manager->get(QNetworkRequest(QUrl(getUrl(Http, "/api/v1/tournament/", true))));
}

void SchopenhauerApi::invitePlayerToTournament(QString tournament, QString username) {
    qDebug() << tournament << username;
    QUrlQuery postData;
    postData.addQueryItem("tournament_id", tournament);
    postData.addQueryItem("username", username);
    // push request

    auth->sendPostRequest(QUrl(getUrl(Http,"/api/v1/tournament/invite/",true)),postData);
}

void SchopenhauerApi::handleFailure(QString reason) {
    // clear credentials and let app know that we failed
    settings->clearAuthCredentials();
    emit authFailed(reason);
}
