#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQuickWindow>
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

    QQuickWindow::setSceneGraphBackend(QSGRendererInterface::OpenGL);
    QQuickWindow app_window;

    QQmlApplicationEngine engine;
    engine.rootContext()->setContextProperty("gameClient", &schopenhauer);

    QString renderer_string = "Unknown";
    int graphics_api = app_window.rendererInterface()->graphicsApi();
    if (graphics_api == QSGRendererInterface::Direct3D12) {
        renderer_string = "Direct3D12";
    } else if (graphics_api == QSGRendererInterface::OpenGL) {
        renderer_string = "OpenGL";
    } else if (graphics_api == QSGRendererInterface::Software) {
        renderer_string = "Software";
    }

    engine.rootContext()->setContextProperty("renderer", renderer_string);
    engine.load(QUrl(QLatin1String("qrc:/main.qml")));

    return app.exec();
}
