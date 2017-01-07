#ifndef CHATMESSAGEMODEL_H
#define CHATMESSAGEMODEL_H

#include <QObject>

class ChatMessageModel : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString username READ getUsername WRITE setUsername NOTIFY usernameChanged)
    Q_PROPERTY(QString message READ getMessage WRITE setMessage NOTIFY messageChanged)
public:
    explicit ChatMessageModel(QObject *parent = 0) : QObject(parent) {
        this->reset();
    }

    void reset() {
        this->username = "AnonymousUser";
        this->message = "";
    }

    void setUsername(QString username) { this->username = username; emit usernameChanged(); }
    void setMessage(QString message) { this->message = message; emit messageChanged(); }

    const QString getUsername() { return this->username; }
    const QString getMessage() { return this->message; }

signals:
    void usernameChanged();
    void messageChanged();

public slots:

private:
    QString username;
    QString message;
};

#endif // CHATMESSAGEMODEL_H
