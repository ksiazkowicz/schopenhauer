#ifndef SCHOPENHAUERAPI_H
#define SCHOPENHAUERAPI_H

#include <QObject>
#include <QUrlQuery>
#include "auth.h"

class SchopenhauerApi : public QObject
{
    Q_OBJECT

public:
    enum Protocol {
        Websocket = 0,
        Http,
        Https,
    };

    explicit SchopenhauerApi(QObject *parent = 0);

    QString getUrl(Protocol proto, QString path);
    QString getUrl(Protocol proto, QString path, bool ignoreSessionToken);

    void attemptLogin(QString login, QString password);

signals:
    void updatedSessionData();

public slots:
    void setSessionToken(QString token);

private:
    QString apiUrl;
    QString sessionToken;

    SchopenhauerCookies *auth;
};

#endif // SCHOPENHAUERAPI_H
