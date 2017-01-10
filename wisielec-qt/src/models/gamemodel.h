#ifndef GAMEMODEL_H
#define GAMEMODEL_H

#include <QObject>
#include <QVariant>
#include <QStringList>

class GameModel : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString sessionId READ getSessionId WRITE setSessionId NOTIFY sessionIdChanged)
    //Q_PROPERTY(float score READ getScore WRITE setScore NOTIFY scoreChanged)
    //Q_PROPERTY(int position READ getPosition WRITE setPosition NOTIFY positionChanged)
    Q_PROPERTY(QVariant playerList READ getPlayerList NOTIFY playerListChanged)
    Q_PROPERTY(QString player READ getPlayer WRITE setPlayer NOTIFY playerChanged)
    Q_PROPERTY(QString modes READ getModes NOTIFY modesChanged)
public:
    explicit GameModel(QObject *parent = 0) : QObject(parent) {}
    void setSessionId(QString sessionId) { this->sessionId = sessionId; emit sessionIdChanged(); }
    void setPlayer(QString player) { this->player = player; emit playerChanged(); }
    //void setScore(float score) { this->score = score; emit scoreChanged(); }
    //void setPosition(int position) { this->position = position; emit positionChanged(); }

    const QString getSessionId() { return this->sessionId; }
    const QString getPlayer() { return this->player; }
    //const float getScore() { return this->score; }
    //const int getPosition() { return this->position; }

    const QVariant getPlayerList() { return QVariant::fromValue(this->playerList); }
    void setPlayerList(QStringList list) { this->playerList = list; emit playerListChanged(); }
    const QString getModes() { return this->modes; }
    void setModes(QString modes) { this->modes = modes; emit modesChanged(); }

signals:
    void sessionIdChanged();
    void playerListChanged();
    void playerChanged();

    //void scoreChanged();
    //void positionChanged();

    void modesChanged();

public slots:

private:
    QString sessionId;
    QStringList playerList;
    QString modes;
    QString player;
};

#endif // GAMEMODEL_H
