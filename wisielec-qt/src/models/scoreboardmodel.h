#ifndef SCOREBOARDMODEL_H
#define SCOREBOARDMODEL_H

#include <QObject>

class ScoreboardModel : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString username READ getUsername WRITE setUsername NOTIFY usernameChanged)
    Q_PROPERTY(float score READ getScore WRITE setScore NOTIFY scoreChanged)
    Q_PROPERTY(bool isWinner READ getIsWinner WRITE setIsWinner NOTIFY isWinnerChanged)

public:
    explicit ScoreboardModel(QObject *parent = 0) : QObject(parent) {
        this->reset();
    }
    void reset() {
        this->username = "AnonymousUser";
        this->score = 0;
        this->isWinner = false;
    }

    void setUsername(QString username) { this->username = username; emit usernameChanged(); }
    void setScore(float score) { this->score = score; emit scoreChanged(); }
    void setIsWinner(bool isWinner) { this->isWinner = isWinner; emit isWinnerChanged(); }

    const QString getUsername() { return this->username; }
    const float getScore() { return this->score; }
    const bool getIsWinner() { return this->isWinner; }

signals:
    void usernameChanged();
    void scoreChanged();
    void isWinnerChanged();

public slots:

private:
    QString username;
    float score;
    bool isWinner;
};

#endif // SCOREBOARDMODEL_H
