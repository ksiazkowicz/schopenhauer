#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQuickStyle>
#include <QtQml>
#include "src/SchopenhauerClient.h"

int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
    QGuiApplication app(argc, argv);

    // set universal style
    QQuickStyle::setStyle("Universal");

    // register QML types
    //qmlRegisterType<SchopenhauerClient>("schopenhauer", 1, 0, "SchClient");
    SchopenhauerClient schopenhauer;

    QQmlApplicationEngine engine;
    engine.rootContext()->setContextProperty("gameClient", &schopenhauer);
    engine.load(QUrl(QLatin1String("qrc:/main.qml")));

    return app.exec();
}
