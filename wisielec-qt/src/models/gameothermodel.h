#ifndef GAMEOTHERMODEL_H
#define GAMEOTHERMODEL_H

#include <QObject>

class GameOtherModel : public QObject
{
    Q_OBJECT
    Q_PROPERTY(int mistakes READ getMistakes WRITE setMistakes NOTIFY mistakesChanged)
    Q_PROPERTY(QString player READ getPlayer WRITE setPlayer NOTIFY playerChanged)
    Q_PROPERTY(QString progress READ getProgress NOTIFY progressChanged)
public:
    explicit GameOtherModel(QObject *parent = 0) : QObject(parent) {}
    void setPlayer(QString player) { this->player = player; emit playerChanged(); }
    void setMistakes(int mistakes) { this->mistakes = mistakes; emit mistakesChanged(); }
    void setProgress(QString progress) { this->progress = progress; emit progressChanged(); }

    const QString getPlayer() { return this->player; }
    const QString getProgress() { return this->progress; }
    const int getMistakes() { return this->mistakes; }

signals:
    void progressChanged();
    void playerChanged();
    void mistakesChanged();

public slots:

private:
    QString progress;
    QString player;
    int mistakes;
};


#endif // GAMEOTHERMODEL_H
