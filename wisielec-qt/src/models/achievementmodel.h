#ifndef ACHIEVEMENTMODEL_H
#define ACHIEVEMENTMODEL_H


#include <QObject>

class AchievementModel : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString name READ getName WRITE setName NOTIFY nameChanged)
    Q_PROPERTY(QString description READ getDescription WRITE setDescription NOTIFY descriptionChanged)
    Q_PROPERTY(QString icon READ getIcon WRITE setIcon NOTIFY iconChanged)
    Q_PROPERTY(bool unlocked READ getUnlocked WRITE setUnlocked NOTIFY unlockedChanged)
public:
    explicit AchievementModel(QObject *parent = 0) : QObject(parent) {
        this->reset();
    }

    void reset() {
        this->name = "";
        this->description = "";
        this->icon = "";
        this->unlocked = false;
    }

    void setName(QString name) { this->name = name; emit nameChanged(); }
    void setDescription(QString description) { this->description = description; emit descriptionChanged(); }
    void setIcon(QString icon) { this->icon = icon; emit iconChanged(); }
    void setUnlocked(bool unlocked) { this->unlocked = unlocked; emit unlockedChanged(); }

    const QString getName() { return this->name; }
    const QString getDescription() { return this->description; }
    const QString getIcon() { return this->icon; }
    const bool getUnlocked() { return this->unlocked; }

signals:
    void nameChanged();
    void descriptionChanged();
    void iconChanged();
    void unlockedChanged();

private:
    QString name;
    QString description;
    QString icon;
    bool unlocked;
};

#endif // ACHIEVEMENTMODEL_H
