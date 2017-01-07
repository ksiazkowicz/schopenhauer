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


void SchopenhauerCookies::replyFinished(QNetworkReply *reply) {
    // if we're not on a login page, abort
    if (!reply->url().toString().contains("/accounts/login"))
        return;

    // if error occured, abort
    if (reply->error() != QNetworkReply::NoError){
        qWarning() << "ERROR:" << reply->errorString();
        qWarning() << reply->readAll();
        return;
    }

    // initialize variables
    QString csrftoken;
    QString session_id;
    // get cookie jar for url
    QList<QNetworkCookie> cookies = mManager->cookieJar()->cookiesForUrl(mUrl);
    for (int i=0; i<cookies.size(); i++) {
        // try to extract csrftoken and session_id from cookies
        if (cookies.at(i).name() == "csrftoken") csrftoken = cookies.at(i).value();
        if (cookies.at(i).name() == "sessionid") session_id = cookies.at(i).value();
    }

    // get response code
    int v = reply->attribute(QNetworkRequest::HttpStatusCodeAttribute).toInt();

    // if it's between 200 and 300, continue
    if (v >= 200 && v < 300) {
        // check if reply contains errors
        if (reply->readAll().contains("<ul class=\"errorlist nonfield\">")) {
            // assume something broke
            qDebug() << "Login failed";
            emit authFailed();
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
    }
}
