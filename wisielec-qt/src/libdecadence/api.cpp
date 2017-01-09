#include "api.h"


SchopenhauerApi::SchopenhauerApi(Settings *appSettings, QObject *parent) : QObject(parent)
{
    // initialize api things
    apiUrl = "127.0.0.1:8000";
    apiUrl = "schopenhauer.krojony.pl";
    sessionToken = "";

    // and auth things
    auth = new SchopenhauerCookies();
    manager = auth->getManager();
    connect(auth, &SchopenhauerCookies::sessionFound, this, &SchopenhauerApi::setSessionToken);
    connect(auth, &SchopenhauerCookies::authFailed, this, &SchopenhauerApi::handleFailure);
    connect(manager, &QNetworkAccessManager::finished, this, &SchopenhauerApi::parseReply);

    // get a csrftoken
    auth->sendGetRequest(QUrl(getUrl(Http, "/accounts/login/", true)));

    // user stuff
    me = new UserModel();
    viewedUser = new UserModel();

    tempUsername = "";

    // use app settings
    settings = appSettings;
    if (settings->authCredentialsPresent()) {
        // get data
        QString token = settings->getAuthToken();
        expectedUsername = settings->getUsername();

        // token present, attempt login
        auth->injectSessionCookie(token, getUrl(Http, "/", true));
        this->setSessionToken(token);
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
    // get content and parse it as JSON Object
    QString content = reply->readAll();
    QJsonDocument jsonResponse = QJsonDocument::fromJson(content.toUtf8());
    QJsonObject jsonObject = jsonResponse.object();

    // get url for figuring out what exactly have we got
    QString url = reply->url().toString();

    if (url.contains("/api/v1/game/create/")) {
        QString sessionId = jsonObject["session_id"].toString();
        emit gameCreated(sessionId);
    }

    if (url.contains("/api/v1/tournament") && url.contains("/invite")) {
        if (jsonObject.keys().contains("username") && jsonObject.keys().contains("session_id")) {
            this->getTournamentList();
        }
        return;
    }

    if (url.contains("/api/v1/tournament")) {
        // we're dealing with tournaments here
        if (jsonObject.keys().contains("tournaments"))
            emit foundTournaments(content);
        return;
    }

    if (url.contains("/api/v1/user") && url.contains("/achievements")) {
        // this request should contain achievements. first, let's check for which user are those though
        UserModel* user;
        // check if either me or viewedUser is defined and compare the username
        if (this->me)
            if (reply->url().toString().contains("/user/"+this->me->getUsername())) user = me;
        else if (this->viewedUser)
            if (reply->url().toString().contains("/user/"+this->viewedUser->getUsername())) user = viewedUser;


        // don't continue if no user was found
        if (user) {
            // reset achievement list
            user->clearAchievements();

            // iterate through all the received achievements
            QJsonArray achievements = jsonObject["achievements"].toArray();
            for (int i=0; i < achievements.size(); i++) {
                // parse json
                QJsonObject achJson = achievements.at(i).toObject();
                QString name = achJson["name"].toString();
                QString description = achJson["description"].toString();
                QString icon = achJson["icon"].toString();
                bool unlocked = achJson["unlocked"].toBool();
                // append to players achievement list
                user->appendAchievement(name, description, icon, unlocked);
            }
            // update progress variable
            user->setProgress(jsonObject["progress"].toInt());
        }
        // nothing to do here
        return;
    }

    if (url.contains("/api/v1/user")) {
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

            // nothing to do here
            return;
        }
    }

    if (url.contains("/api/v1/ranking")) {
        if (jsonObject.keys().contains("players")) {
            // assume it's the ranking list
            QJsonArray playersArray = jsonObject["players"].toArray();

            // don't proceed if there isn't actually any data though
            if (!playersArray.isEmpty()) {
                // clear the list
                bestPlayers.clear();
                // iterate through it and append all players
                for (int i=0; i < playersArray.size(); i++) {
                    QJsonObject playerJson = playersArray.at(i).toObject();
                    RankingModel *player = new RankingModel();
                    player->setUsername(playerJson["username"].toString());
                    player->setScore((float)(playerJson["score"].toDouble()));
                    player->setPosition(playerJson["position"].toInt());
                    bestPlayers.append(player);
                }
                emit rankingChanged();
            }
            emit rankingChanged();
        }
        // nothing to do here
        return;
    }


    qDebug() << url;
    qDebug() << content;
}

void SchopenhauerApi::getUserData() {
    manager->get(QNetworkRequest(QUrl(getUrl(Http, "/api/v1/user/", true))));
}

void SchopenhauerApi::getUserData(QString username) {
    tempUsername = username;
    manager->get(QNetworkRequest(QUrl(getUrl(Http, "/api/v1/user/"+username, true))));
}

void SchopenhauerApi::getUserAchievements() {
    this->getUserAchievements(me->getUsername());
}

void SchopenhauerApi::getUserAchievements(QString username) {
    manager->get(QNetworkRequest(QUrl(getUrl(Http, "/api/v1/user/"+username+"/achievements", true))));
}

void SchopenhauerApi::getTournamentList() {
    manager->get(QNetworkRequest(QUrl(getUrl(Http, "/api/v1/tournament/", true))));
}

void SchopenhauerApi::invitePlayerToTournament(QString tournament, QString username) {
    QUrlQuery postData;
    postData.addQueryItem("tournament_id", tournament);
    postData.addQueryItem("username", username);
    postData.addQueryItem("csrfmiddlewaretoken", auth->getCachedCsrftoken());
    // push request
    auth->sendPostRequest(QUrl(getUrl(Http,"/api/v1/tournament/invite/",true)),postData);
}

void SchopenhauerApi::createGame(QString modifiers) {
    QUrlQuery postData;
    postData.addQueryItem("modifiers", modifiers);
    postData.addQueryItem("csrfmiddlewaretoken", auth->getCachedCsrftoken());
    auth->sendPostRequest(QUrl(getUrl(Http,"/api/v1/game/create/",true)),postData);
}

void SchopenhauerApi::createTournament(QString modifiers, QString name) {
    QUrlQuery postData;
    postData.addQueryItem("modifiers", modifiers);
    postData.addQueryItem("name", name);
    postData.addQueryItem("csrfmiddlewaretoken", auth->getCachedCsrftoken());
    auth->sendPostRequest(QUrl(getUrl(Http,"/api/v1/tournament/create/",true)),postData);
}

void SchopenhauerApi::newRoundTournament(QString sessionId) {
    QUrlQuery postData;
    postData.addQueryItem("csrfmiddlewaretoken", auth->getCachedCsrftoken());
    auth->sendPostRequest(QUrl(getUrl(Http,"/api/v1/tournament/"+sessionId+"/new_round/",true)),postData);
}

void SchopenhauerApi::handleFailure(QString reason) {
    // clear credentials and let app know that we failed
    settings->clearAuthCredentials();
    emit authFailed(reason);
}
