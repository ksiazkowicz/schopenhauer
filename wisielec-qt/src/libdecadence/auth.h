#ifndef SCHOPENHAUERCOOKIES_H
#define SCHOPENHAUERCOOKIES_H

#include <QObject>
#include <QNetworkAccessManager>
#include <QUrlQuery>
#include <QUrl>
#include <QNetworkCookieJar>
#include <QNetworkRequest>
#include <QNetworkReply>

class SchopenhauerCookies : public QObject
{
    Q_OBJECT

public:
    explicit SchopenhauerCookies(QObject *parent = 0);

    void sendPostRequest(const QUrl &url, const QUrlQuery &data);

    void sendGetRequest(const QUrl &url);
    QNetworkAccessManager* getManager() { return mManager; }

    QUrlQuery login;

signals:
    void sessionFound(QString session_id);
    void error(QString errorString);

private slots:
    void replyFinished(QNetworkReply *reply);

private:
    QNetworkAccessManager *mManager;
    QUrl mUrl;
    QUrl rUrl;
    QUrl test;
};

#endif // SCHOPENHAUERCOOKIES_H
