#include "api.h"

SchopenhauerApi::SchopenhauerApi(QObject *parent) : QObject(parent)
{
    // initialize api things
    apiUrl = "127.0.0.1:8000";
    sessionToken = "";

    // and auth things
    auth = new SchopenhauerCookies();
    connect(auth, &SchopenhauerCookies::sessionFound, this, &SchopenhauerApi::setSessionToken);
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
