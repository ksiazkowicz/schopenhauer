#ifndef ROUNDMODEL_H
#define ROUNDMODEL_H

#include <QObject>
#include <QVariant>
#include <QList>
#include "GameModel.h"

class RoundModel : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString status READ getStatus WRITE setStatus NOTIFY statusChanged)
    Q_PROPERTY(QString winner READ getWinner WRITE setWinner NOTIFY winnerChanged)
    Q_PROPERTY(QVariant games READ getGames NOTIFY gamesChanged)
    Q_PROPERTY(int roundId READ getRoundId NOTIFY roundIdChanged)
public:
    explicit RoundModel(QObject *parent = 0) : QObject(parent) {}
    void setStatus(QString status) { this->status = status; emit statusChanged(); }
    void setWinner(QString winner) { this->winner = winner; emit winnerChanged(); }
    void setRoundId(int pk) { this->roundId = pk; emit roundIdChanged(); }

    const QString getStatus() { return this->status; }
    const QVariant getGames() { return QVariant::fromValue(this->games); }
    const QString getWinner() { return this->winner; }
    const int getRoundId() { return this->roundId; }

    void setGame(QString player, QString sessionId) {
        GameModel *game = 0;
        for (int i=0; i < games.count(); i++) {
            GameModel *foundGame = (GameModel*)games.at(i);
            if (foundGame->getSessionId() == sessionId) {
                game = foundGame;
                break;
            }
        }

        if (game == 0) {
            game = new GameModel();
            game->setSessionId(sessionId);
            games.append(game);
        }
        game->setPlayer(player);
        emit gamesChanged();
    }

    Q_INVOKABLE QString getGameForPlayer(QString player) {
        for (int i=0; i < games.count(); i++) {
            GameModel* game = (GameModel*)games.at(i);
            if (game->getPlayer() == player)
                return game->getSessionId();
        }
        return "";
    }

    Q_INVOKABLE bool inProgress() { return this->status == "ROUND_IN_PROGRESS"; }

signals:
    void statusChanged();
    void gamesChanged();
    void winnerChanged();
    void roundIdChanged();

public slots:

private:
    QString winner;
    QString status;
    QList<QObject*> games;
    int roundId;
};

#endif // ROUNDMODEL_H
