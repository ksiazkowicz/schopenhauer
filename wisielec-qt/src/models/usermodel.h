#ifndef USERMODEL_H
#define USERMODEL_H

#include <QObject>
#include <QDebug>
#include <QVariant>
#include "AchievementModel.h"

class UserModel : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString username READ getUsername WRITE setUsername NOTIFY usernameChanged)
    Q_PROPERTY(QString avatar READ getAvatar WRITE setAvatar NOTIFY avatarChanged)
    Q_PROPERTY(float score READ getScore WRITE setScore NOTIFY scoreChanged)
    Q_PROPERTY(int position READ getPosition WRITE setPosition NOTIFY positionChanged)

    Q_PROPERTY(int wonGames READ getWonGames WRITE setWonGames NOTIFY wonGamesChanged)
    Q_PROPERTY(int lostGames READ getLostGames WRITE setLostGames NOTIFY lostGamesChanged)
    Q_PROPERTY(int wonTournaments READ getWonTournaments WRITE setWonTournaments NOTIFY wonTournamentsChanged)
    Q_PROPERTY(int lostTournaments READ getLostTournaments WRITE setLostTournaments NOTIFY lostTournamentsChanged)

    Q_PROPERTY(int progress READ getProgress WRITE setProgress NOTIFY progressChanged)
    Q_PROPERTY(QVariant achievements READ getAchievements NOTIFY achievementsChanged)
public:
    explicit UserModel(QObject *parent = 0) : QObject(parent) {
        this->reset();
    }
    UserModel(UserModel *model) {
        this->username = model->username;
        this->avatar = model->avatar;
        this->position = model->position;
        this->score = model->score;
        this->wonGames = model->wonGames;
        this->lostGames = model->lostGames;
        this->wonTournaments = model->wonTournaments;
        this->lostTournaments = model->lostTournaments;
    }

    void reset() {
        this->username = "AnonymousUser";
        this->avatar = "qrc:/img/avatar.jpg";
        this->position = 0;
        this->score = 0;
        this->wonGames = 0;
        this->lostGames = 0;
        this->wonTournaments = 0;
        this->lostTournaments = 0;
    }

    void setUsername(QString username) { this->username = username; emit usernameChanged(); }
    void setAvatar(QString avatar) { this->avatar = avatar; emit avatarChanged(); }
    void setScore(float score) { this->score = score; emit scoreChanged(); }
    void setPosition(int position) { this->position = position; emit positionChanged(); }

    const QString getUsername() { return this->username; }
    const QString getAvatar() { return this->avatar; }
    const float getScore() { return this->score; }
    const int getPosition() { return this->position; }

    const int getWonGames() { return this->wonGames; }
    const int getLostGames() { return this->lostGames; }
    const int getWonTournaments() { return this->wonTournaments; }
    const int getLostTournaments() { return this->lostTournaments; }

    const int getProgress() { return this->progress; }
    QVariant getAchievements() { return QVariant::fromValue(this->achievements); }

    void setWonGames(int a) { this->wonGames = a; emit wonGamesChanged(); }
    void setLostGames(int a) { this->lostGames = a; emit lostGamesChanged(); }
    void setWonTournaments(int a) { this->wonTournaments = a; emit wonTournamentsChanged(); }
    void setLostTournaments(int a) { this->lostTournaments = a; emit lostTournamentsChanged(); }

    void setProgress(int a) { this->progress = a; emit progressChanged(); }

    void clearAchievements() { achievements.clear(); }
    void appendAchievement(QString name, QString description, QString icon, bool unlocked) {
        AchievementModel *achievement = new AchievementModel();
        achievement->setName(name);
        achievement->setDescription(description);
        achievement->setIcon(icon);
        achievement->setUnlocked(unlocked);
        this->achievements.append(achievement);
    }

signals:
    void usernameChanged();
    void scoreChanged();
    void positionChanged();
    void avatarChanged();

    void wonGamesChanged();
    void lostGamesChanged();
    void wonTournamentsChanged();
    void lostTournamentsChanged();

    void progressChanged();
    void achievementsChanged();

public slots:

private:
    QString username;
    QString avatar;
    float score;
    int position;

    int wonGames;
    int lostGames;
    int wonTournaments;
    int lostTournaments;

    int progress;
    QList<QObject*> achievements;
};

#endif // USERMODEL_H
