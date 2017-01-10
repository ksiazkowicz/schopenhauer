#ifndef TOURNAMENTMODEL_H
#define TOURNAMENTMODEL_H


#include <QObject>
#include <QVariant>
#include <QList>
#include <QStringList>
#include "scoreboardmodel.h"

class TournamentModel : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString sessionId READ getSessionId WRITE setSessionId NOTIFY sessionIdChanged)
    Q_PROPERTY(QString name READ getName WRITE setName NOTIFY nameChanged)
    Q_PROPERTY(QVariant playerList READ getPlayerList NOTIFY playerListChanged)
    Q_PROPERTY(QString modes READ getModes WRITE setModes NOTIFY modesChanged)
    Q_PROPERTY(bool inProgress READ getInProgress WRITE setInProgress NOTIFY inProgressChanged)
    Q_PROPERTY(QString winner READ getWinner WRITE setWinner NOTIFY winnerChanged)

    Q_PROPERTY(QVariant scoreboard READ getScoreboard NOTIFY scoreboardChanged)
    Q_PROPERTY(QVariant rounds READ getRounds NOTIFY roundsChanged)

    Q_PROPERTY(int currentRound READ getCurrentRound NOTIFY currentRoundChanged)
public:
    explicit TournamentModel(QObject *parent = 0) : QObject(parent) {}
    void setSessionId(QString sessionId) { this->sessionId = sessionId; emit sessionIdChanged(); }
    void setName(QString name) { this->name = name; emit nameChanged(); }
    void setInProgress(bool inProgress) { this->inProgress = inProgress; emit inProgressChanged(); }
    void setPlayerList(QStringList list) { this->playerList = list; emit playerListChanged(); }
    void setModes(QString modes) { this->modes = modes; emit modesChanged(); }
    void setWinner(QString winner) { this->winner = winner; emit winnerChanged(); }

    const QString getSessionId() { return this->sessionId; }
    const QString getName() { return this->name; }
    const QString getModes() { return this->modes; }
    const bool getInProgress() { return this->inProgress; }
    const QVariant getPlayerList() { return QVariant::fromValue(this->playerList); }

    const QVariant getScoreboard() { return QVariant::fromValue(this->scoreboard); }
    const QVariant getRounds() { return QVariant::fromValue(this->rounds); }
    const QString getWinner() { return this->winner; }

    void setPlayerScore(QString username, int score, bool isWinner) {
        // try to find the player on scoreboard first
        for (int i=0; i < scoreboard.count(); i++) {
            ScoreboardModel *player = (ScoreboardModel*)scoreboard.at(i);
            if (player->getUsername() == username) {
                player->setIsWinner(isWinner);
                player->setScore(score);
                emit scoreboardChanged();
                return;
            }
        }
        // player not found, add it to list
        ScoreboardModel *player = new ScoreboardModel();
        player->setUsername(username);
        player->setScore(score);
        player->setIsWinner(isWinner);
        scoreboard.append(player);
        emit scoreboardChanged();
    }

    void updateRounds(QString content) {
        emit currentRoundChanged();
    }

    int getCurrentRound() { return 3; }

signals:
    void sessionIdChanged();
    void nameChanged();
    void inProgressChanged();
    void playerListChanged();
    void modesChanged();
    void scoreboardChanged();
    void roundsChanged();
    void winnerChanged();

    void currentRoundChanged();

public slots:

private:
    QString sessionId;
    QString name;
    QString modes;
    QString winner;
    bool inProgress;
    QStringList playerList;
    QList<QObject*> scoreboard;
    QList<QObject*> rounds;
};


#endif // TOURNAMENTMODEL_H
