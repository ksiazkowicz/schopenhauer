#ifndef SCHOPENHAUERCLIENT_H
#define SCHOPENHAUERCLIENT_H

#include <QObject>
#include <QWebSocket>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QMap>
#include "auth.h"
#include "api.h"
#include "src/models/gamemodel.h"
#include "src/models/TournamentModel.h"
#include "src/models/ChatMessageModel.h"

class SchopenhauerClient : public QObject
{
    Q_OBJECT
    Q_PROPERTY(int score READ get_score NOTIFY score_changed)
    Q_PROPERTY(int mistakes READ get_mistakes NOTIFY mistakes_changed)
    Q_PROPERTY(QString progress READ get_progress NOTIFY progress_changed)
    Q_PROPERTY(QStringList used_chars READ get_used_chars NOTIFY used_chars_changed)
    Q_PROPERTY(QString session_id READ get_session_id WRITE set_session_id NOTIFY session_id_changed)
    Q_PROPERTY(QVariant games READ get_games NOTIFY games_changed)
    Q_PROPERTY(QVariant tournaments READ getTournaments NOTIFY tournamentsChanged)
    Q_PROPERTY(QVariant lobbyPlayers READ getLobbyPlayers NOTIFY lobbyPlayersChanged)
    Q_PROPERTY(QVariant chatMessages READ getChatMessages NOTIFY chatMessagesChanged)
    Q_PROPERTY(QString channelName READ getChannelName NOTIFY channelNameChanged)
    Q_PROPERTY(QString tournamentId READ getTournamentId NOTIFY tournamentIdChanged)
    Q_PROPERTY(TournamentModel* currentTournament READ getCurrentTournament NOTIFY tournamentIdChanged)

public:
    explicit SchopenhauerClient(SchopenhauerApi *api, QObject *parent = 0);

    int get_score() { return score; }
    int get_mistakes() { return mistakes; }
    QVariant get_games() { return QVariant::fromValue(games.values()); }
    QString get_progress() { return progress; }
    QString get_session_id() { return session_id; }
    void set_session_id(QString _new) { session_id = _new; emit session_id_changed(); }
    QStringList get_used_chars() { return used_chars; }

    Q_INVOKABLE void guess_letter(QString letter);
    Q_INVOKABLE void join_game(QString session_id);
    Q_INVOKABLE void new_game();
    Q_INVOKABLE void refresh_lobby();

    QVariant getLobbyPlayers() { return QVariant::fromValue(this->lobbyPlayers); }
    QVariant getTournaments() { return QVariant::fromValue(this->tournaments.values()); }
    QVariant getChatMessages() { return QVariant::fromValue(this->chatMessages); }

    QString getChannelName();

    Q_INVOKABLE void sendChatMessage(QString message_text);
    Q_INVOKABLE void switchChatChannel(QString channel);

    Q_INVOKABLE void joinTournament(QString sessionId);
    Q_INVOKABLE QString currentTournamentName();
    Q_INVOKABLE QString currentTournamentModes();
    Q_INVOKABLE QString getTournamentId() { return currentTournamentId; }
    Q_INVOKABLE TournamentModel* getCurrentTournament();

signals:
    void score_changed();
    void progress_changed();
    void games_changed();
    void mistakes_changed();
    void used_chars_changed();
    void session_id_changed();

    void lobbyPlayersChanged();
    void tournamentsChanged();
    void chatMessagesChanged();
    void channelNameChanged();

    void gameFound(QString sessionId);
    void roundEnded();

    void tournamentInfoFound();
    void tournamentIdChanged();

public slots:
    void onContentReceived(QString message);
    void onLobbyContentReceived(QString message);
    void onChatContentReceived(QString message);
    void onTournamentContentReceived(QString message);
    void onStateChanged(QAbstractSocket::SocketState state);

    void invalidateSockets();

    void parseTournaments(QString content);
    void parseRounds(QString content);
    void parseScoreboard(QString reply);

    void endTournament(QString sessionId, QString winner, int roundCount);

private:
    QWebSocket socket;
    QWebSocket lobby_socket;
    QWebSocket chat_socket;
    QWebSocket tournament_socket;

    int score = 0;
    int mistakes = 0;
    QString progress = "____";
    QStringList used_chars;
    QStringList lobbyPlayers;

    QMap<QString,QObject*> games;
    QMap<QString,QObject*> tournaments;

    QList<QObject*> chatMessages;
    QString currentChatRoom = "lobby";

    GameModel* currentGame;

    SchopenhauerApi *api;
    QString session_id;

    QString currentTournamentId;
};

#endif // SCHOPENHAUERCLIENT_H
