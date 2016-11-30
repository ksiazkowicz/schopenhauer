#ifndef RANKINGMODEL_H
#define RANKINGMODEL_H

#include <QObject>

class RankingModel : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString username READ getUsername WRITE setUsername NOTIFY usernameChanged)
    Q_PROPERTY(float score READ getScore WRITE setScore NOTIFY scoreChanged)
    Q_PROPERTY(int position READ getPosition WRITE setPosition NOTIFY positionChanged)
public:
    explicit RankingModel(QObject *parent = 0) : QObject(parent) {}
    void setUsername(QString username) { this->username = username; emit usernameChanged(); }
    void setScore(float score) { this->score = score; emit scoreChanged(); }
    void setPosition(int position) { this->position = position; emit positionChanged(); }

    const QString getUsername() { return this->username; }
    const float getScore() { return this->score; }
    const int getPosition() { return this->position; }

signals:
    void usernameChanged();
    void scoreChanged();
    void positionChanged();

public slots:

private:
    QString username;
    float score;
    int position;
};

#endif // RANKINGMODEL_H
