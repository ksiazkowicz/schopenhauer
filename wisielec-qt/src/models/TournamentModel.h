#ifndef TOURNAMENTMODEL_H
#define TOURNAMENTMODEL_H


#include <QObject>
#include <QVariant>
#include <QStringList>

class TournamentModel : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString sessionId READ getSessionId WRITE setSessionId NOTIFY sessionIdChanged)
    Q_PROPERTY(QString name READ getName WRITE setName NOTIFY nameChanged)
    Q_PROPERTY(QVariant playerList READ getPlayerList NOTIFY playerListChanged)
    Q_PROPERTY(bool inProgress READ getInProgress WRITE setInProgress NOTIFY inProgressChanged)
public:
    explicit TournamentModel(QObject *parent = 0) : QObject(parent) {}
    void setSessionId(QString sessionId) { this->sessionId = sessionId; emit sessionIdChanged(); }
    void setName(QString name) { this->name = name; emit nameChanged(); }
    void setInProgress(bool inProgress) { this->inProgress = inProgress; emit inProgressChanged(); }
    void setPlayerList(QStringList list) { this->playerList = list; emit playerListChanged(); }

    const QString getSessionId() { return this->sessionId; }
    const QString getName() { return this->name; }
    const bool getInProgress() { return this->inProgress; }
    const QVariant getPlayerList() { return QVariant::fromValue(this->playerList); }

signals:
    void sessionIdChanged();
    void nameChanged();
    void inProgressChanged();
    void playerListChanged();

public slots:

private:
    QString sessionId;
    QString name;
    bool inProgress;
    QStringList playerList;
};


#endif // TOURNAMENTMODEL_H
