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
}


void SchopenhauerCookies::replyFinished(QNetworkReply *reply) {
    if (!reply->url().toString().contains("/profiles/login"))
        return;

    if (reply->error() != QNetworkReply::NoError){
        qWarning() << "ERROR:" << reply->errorString();
        qWarning() << reply->readAll();
        return;
    }

    //Cookies//
    QString csrftoken;
    QString session_id;
    QList<QNetworkCookie>  cookies = mManager->cookieJar()->cookiesForUrl(mUrl);
    //qDebug() << "COOKIES for" << mUrl.host(); // << cookies;
    for (int i=0; i<cookies.size(); i++) {
        //qDebug() << cookies.at(i).name() << cookies.at(i).value();
        if (cookies.at(i).name() == "csrftoken") csrftoken = cookies.at(i).value();
        if (cookies.at(i).name() == "sessionid") session_id = cookies.at(i).value();
    }
    //End Cookies//
    int v = reply->attribute(QNetworkRequest::HttpStatusCodeAttribute).toInt();
    if (v >= 200 && v < 300) {
        login.addQueryItem("csrfmiddlewaretoken", csrftoken);
        mManager->post(QNetworkRequest(mUrl), login.toString(QUrl::FullyEncoded).toUtf8());
    } else if (v >= 300 && v < 400) {
        qDebug() << "Session found";
        emit sessionFound(session_id);
    }
}
