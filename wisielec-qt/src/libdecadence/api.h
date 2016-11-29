#ifndef SCHOPENHAUERAPI_H
#define SCHOPENHAUERAPI_H

#include <QObject>
#include <QUrlQuery>
#include <QJsonArray>
#include <QJsonObject>
#include <QJsonDocument>
#include "src/models/RankingModel.h"
#include "auth.h"

class SchopenhauerApi : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QVariant rankingModel READ getRankingModel NOTIFY rankingChanged)

public:
    enum Protocol {
        Websocket = 0,
        Http,
        Https,
    };

    explicit SchopenhauerApi(QObject *parent = 0);

    QString getUrl(Protocol proto, QString path);
    QString getUrl(Protocol proto, QString path, bool ignoreSessionToken);

    Q_INVOKABLE void getRanking();

    Q_INVOKABLE void attemptLogin(QString login, QString password);


    QVariant getRankingModel() { return QVariant::fromValue(bestPlayers); }

signals:
    void updatedSessionData();
    void rankingChanged();

public slots:
    void setSessionToken(QString token);
    void parseReply(QNetworkReply *reply);

private:
    QString apiUrl;
    QString sessionToken;

    SchopenhauerCookies *auth;
    QNetworkAccessManager *manager;

    QList<QObject*> bestPlayers;
};

#endif // SCHOPENHAUERAPI_H
