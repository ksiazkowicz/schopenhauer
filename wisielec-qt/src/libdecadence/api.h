#ifndef SCHOPENHAUERAPI_H
#define SCHOPENHAUERAPI_H

#include <QObject>
#include <QUrlQuery>
#include <QJsonArray>
#include <QJsonObject>
#include <QJsonDocument>
#include "src/models/RankingModel.h"
#include "src/models/UserModel.h"
#include "auth.h"
#include "src/settings.h"

class SchopenhauerApi : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QVariant rankingModel READ getRankingModel NOTIFY rankingChanged)
    Q_PROPERTY(UserModel *user READ getUser NOTIFY userChanged)
    Q_PROPERTY(UserModel *viewedUser READ getViewedUser NOTIFY viewedUserChanged)

public:
    enum Protocol {
        Websocket = 0,
        Http,
        Https,
    };

    explicit SchopenhauerApi(Settings *appSettings, QObject *parent = 0);

    QString getUrl(Protocol proto, QString path);
    QString getUrl(Protocol proto, QString path, bool ignoreSessionToken);

    Q_INVOKABLE QString getApiServer() { return this->apiUrl; }

    Q_INVOKABLE void getRanking();
    Q_INVOKABLE void getUserData();
    Q_INVOKABLE void getUserData(QString username);
    Q_INVOKABLE void getUserAchievements();
    Q_INVOKABLE void getUserAchievements(QString username);

    Q_INVOKABLE void getTournamentList();
    //Q_INVOKABLE void getTournament(QString tournament);
    Q_INVOKABLE void invitePlayerToTournament(QString tournament, QString username);

    Q_INVOKABLE void attemptLogin(QString login, QString password);


    QVariant getRankingModel() { return QVariant::fromValue(bestPlayers); }
    UserModel *getUser() { return me; }
    UserModel *getViewedUser() { return viewedUser; }

signals:
    void updatedSessionData();
    void rankingChanged();
    void userChanged();
    void viewedUserChanged();
    void foundTournaments(QString reply);

    void omgToDziala();

    void authSuccess();
    void authFailed(QString reason);

public slots:
    void setSessionToken(QString token);
    void parseReply(QNetworkReply *reply);
    void handleFailure(QString reason);

private:
    QString apiUrl;
    QString sessionToken;

    SchopenhauerCookies *auth;
    QNetworkAccessManager *manager;

    QString tempUsername;

    QList<QObject*> bestPlayers;
    UserModel *me;
    UserModel *viewedUser;

    Settings *settings;
    QString expectedUsername = "";
};

#endif // SCHOPENHAUERAPI_H
