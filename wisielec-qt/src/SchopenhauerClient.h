#ifndef SCHOPENHAUERCLIENT_H
#define SCHOPENHAUERCLIENT_H

#include <QObject>
#include <QWebSocket>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>

class SchopenhauerClient : public QObject
{
    Q_OBJECT

    Q_PROPERTY(int score READ get_score NOTIFY score_changed)
    Q_PROPERTY(int mistakes READ get_mistakes NOTIFY mistakes_changed)
    Q_PROPERTY(QString progress READ get_progress NOTIFY progress_changed)
    Q_PROPERTY(QStringList used_chars READ get_used_chars NOTIFY used_chars_changed)
    Q_PROPERTY(QString session_id READ get_session_id WRITE set_session_id NOTIFY session_id_changed)
    Q_PROPERTY(QVariant games READ get_games NOTIFY games_changed)

public:
    explicit SchopenhauerClient(QObject *parent = 0);

    int get_score() { return score; }
    int get_mistakes() { return mistakes; }
    QVariant get_games() { return QVariant::fromValue(games); }
    QString get_progress() { return progress; }
    QString get_session_id() { return session_id; }
    void set_session_id(QString _new) { session_id = _new; emit session_id_changed(); }
    QStringList get_used_chars() { return used_chars; }

    Q_INVOKABLE void guess_letter(QString letter);
    Q_INVOKABLE void join_game(QString session_id);
    Q_INVOKABLE void new_game();


signals:
    void score_changed();
    void progress_changed();
    void games_changed();
    void mistakes_changed();
    void used_chars_changed();
    void session_id_changed();

public slots:
    void onConnected();
    void onDisconnected();
    void onContentReceived(QString message);
    void onLobbyContentReceived(QString message);

private:
    QWebSocket socket;
    QWebSocket lobby_socket;
    QString session_id;
    int score = 0;
    int mistakes = 0;
    QString progress = "____";
    QStringList used_chars;
    QStringList games;
};

#endif // SCHOPENHAUERCLIENT_H
