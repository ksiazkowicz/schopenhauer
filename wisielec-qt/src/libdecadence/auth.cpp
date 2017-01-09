#include "auth.h"
#include <QDebug>
#include <QNetworkCookie>

SchopenhauerCookies::SchopenhauerCookies(QObject *parent) : QObject(parent)
{
    mManager = new QNetworkAccessManager(this);
    mManager->setCookieJar(new QNetworkCookieJar(this));
    connect(mManager, SIGNAL(finished(QNetworkReply*)), SLOT(replyFinished(QNetworkReply*)));
}

void SchopenhauerCookies::sendPostRequest(const QUrl &url, const QUrlQuery &data){
    mUrl = url;
    login = data;
    QNetworkRequest r(mUrl);
    r.setHeader(QNetworkRequest::ContentTypeHeader,
                       "application/x-www-form-urlencoded");
    mManager->post(r, data.toString(QUrl::FullyEncoded).toUtf8());
}

void SchopenhauerCookies::sendGetRequest(const QUrl &url) {
    mUrl = url;
    test = mUrl;
    QNetworkRequest r(mUrl);
    mManager->get(r);

    status = Busy;
    emit statusChanged();
}

QString SchopenhauerCookies::getCachedCsrftoken() {
    return csrftoken;
}

void SchopenhauerCookies::injectSessionCookie(QString token, QString apiUrl) {
    // create an empty list of cookies
    QList<QNetworkCookie> cookies;
    // forge session cookie
    QNetworkCookie session_cookie("sessionid", token.toLatin1());
    cookies.append(session_cookie);
    // update cookie jar
    mManager->cookieJar()->setCookiesFromUrl(cookies, apiUrl);
}

void SchopenhauerCookies::replyFinished(QNetworkReply *reply) {
    // if error occured, abort
    if (reply->error() != QNetworkReply::NoError){
        qWarning() << "ERROR:" << reply->errorString();
        qWarning() << reply->readAll();
        return;
    }

    // initialize variables
    QString session_id;
    // get cookie jar for url
    QList<QNetworkCookie> cookies = mManager->cookieJar()->cookiesForUrl(mUrl);
    for (int i=0; i<cookies.size(); i++) {
        // try to extract csrftoken and session_id from cookies
        if (cookies.at(i).name() == "csrftoken") csrftoken = cookies.at(i).value();
        if (cookies.at(i).name() == "sessionid") session_id = cookies.at(i).value();
    }

    // ignore if it's not login page though
    if (!reply->url().toString().contains("/accounts/login"))
        return;

    // get response code
    int v = reply->attribute(QNetworkRequest::HttpStatusCodeAttribute).toInt();

    // if it's between 200 and 300, continue
    if (v >= 200 && v < 300) {
        // check if reply contains errors
        if (reply->readAll().contains("<ul class=\"errorlist nonfield\">")) {
            // assume something broke
            qDebug() << "Login failed";
            emit authFailed("Logowanie nie powiodło się. Sprawdź login i hasło.");
            status = Idle;
            emit statusChanged();
        } else {
            // we got the login form and csrf token, log in
            login.addQueryItem("csrfmiddlewaretoken", csrftoken);
            mManager->post(QNetworkRequest(mUrl), login.toString(QUrl::FullyEncoded).toUtf8());
        }
    } else if (v >= 300 && v < 400) {
        // we got a redirect, assume we logged in
        qDebug() << "Session found";
        emit sessionFound(session_id);
        status = Idle;
        emit statusChanged();
    } else if (v > 400) {
        emit authFailed("Błąd serwera. Spróbuj ponownie później.");
    }
}
