#ifndef TOURNAMENTMODEL_H
#define TOURNAMENTMODEL_H


#include <QObject>
#include <QVariant>
#include <QList>
#include <QStringList>
#include "ScoreboardModel.h"
#include "RoundModel.h"

class TournamentModel : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString sessionId READ getSessionId WRITE setSessionId NOTIFY sessionIdChanged)
    Q_PROPERTY(QString name READ getName WRITE setName NOTIFY nameChanged)
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
    void setModes(QString modes) { this->modes = modes; emit modesChanged(); }
    void setWinner(QString winner) { this->winner = winner; emit winnerChanged(); }

    const QString getSessionId() { return this->sessionId; }
    const QString getName() { return this->name; }
    const QString getModes() { return this->modes; }
    const bool getInProgress() { return this->inProgress; }

    const QVariant getScoreboard() { return QVariant::fromValue(this->scoreboard); }
    const QVariant getRounds() { return QVariant::fromValue(this->rounds); }
    const QString getWinner() { return this->winner; }

    void setPlayer(QString username, int score, bool isWinner, bool noScore) {
        // try to find the player on scoreboard first
        ScoreboardModel *player = 0;
        for (int i=0; i < scoreboard.count(); i++) {
            ScoreboardModel *fPlayer = (ScoreboardModel*)scoreboard.at(i);
            if (fPlayer->getUsername() == username) {
                player = fPlayer;
                break;
            }
        }

        // player not found, add it to list
        if (player == 0) {
            player = new ScoreboardModel();
            scoreboard.append(player);
            emit scoreboardChanged();
        }

        // update player
        player->setUsername(username);
        if (!noScore)
            player->setScore(score);
        player->setIsWinner(isWinner);
    }

    void updateRound(int pk, QString status, QString winner) {
        // make sure we're not duplicating those though
        RoundModel *round = 0;
        for (int i=0; i < rounds.count(); i++) {
            RoundModel *foundRound = (RoundModel*)rounds.at(i);
            if (foundRound->getRoundId() == pk) {
                round = foundRound;
                break;
            }
        }
        // create round if doesn't exist
        if (round == 0) {
            round = new RoundModel();
            round->setRoundId(pk);
            rounds.append(round);
        }

        // update data
        round->setWinner(winner);
        round->setStatus(status);

        emit roundsChanged();
    }

    void updateRoundGame(int pk, QString sessionId, QString player) {
        RoundModel *round = 0;
        for (int i=0; i < rounds.count(); i++) {
            round = (RoundModel*)rounds.at(i);
            if (round->getRoundId() == pk) {
                round->setGame(player, sessionId);
                return;
            }
        }
    }

    int getCurrentRound() { return rounds.count()+1; }

signals:
    void sessionIdChanged();
    void nameChanged();
    void inProgressChanged();
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
    QList<QObject*> scoreboard;
    QList<QObject*> rounds;
};


#endif // TOURNAMENTMODEL_H
