import QtQuick 2.0
import QtWebView 1.1
import QtQuick.Controls 2.0

Page {
    WebView {
        id: webview
        url: "http://krojony.pl/"
        anchors.fill: parent
        /*onNavigationRequested: {
            // detect URL scheme prefix, most likely an external link
            var schemaRE = /^\w+:/;
            if (schemaRE.test(request.url)) {
                request.action = WebView.AcceptRequest;
            } else {
                request.action = WebView.IgnoreRequest;
                // delegate request.url here
            }
        }*/
        onLoadingChanged: {
            if (loading == false)
                webview.runJavaScript("readCookie('csrftoken')", function(result) { console.log(result); gameClient.attempt_login(result) });
        }
        onUrlChanged: {
            //webview.runJavaScript("readCookie('csrftoken')", function(result) { console.log(result); });
            if (url == "http://schopenhauer.krojony.pl/game/lobby") {
                url = "about:blank"
                webview.visible = false
                webview.runJavaScript("readCookie('csrftoken')", function(result) { console.log(result); });
            }
            console.log(url)
        }
        Component.onCompleted: url = "http://127.0.0.1:8000/profiles/login"
    }
}
