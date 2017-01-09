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

    void injectSessionCookie(QString token, QString apiUrl);

    QUrlQuery login;

    enum Status {
        Idle = 0,
        Busy
    };
    Status status = Idle;

    QString getCachedCsrftoken();

signals:
    void sessionFound(QString session_id);
    void error(QString errorString);
    void statusChanged();
    void authFailed(QString reason);

private slots:
    void replyFinished(QNetworkReply *reply);

private:
    QNetworkAccessManager *mManager;
    QUrl mUrl;
    QUrl rUrl;
    QUrl test;

    QString csrftoken = "";

};

#endif // SCHOPENHAUERCOOKIES_H
