import QtQuick 2.0
import QtWebView 1.1
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.1

Page {
    WebView {
        id: webview
        url: "about:blank"
        anchors.fill: parent
        onUrlChanged: {
            var urlString = url.toString();

            if (!urlString.match("accounts\/signup")) {
                // back on lobby page, quit
                stack.pop()
            }
        }
        Component.onCompleted: url = "http://" + api.getApiServer() + "/accounts/signup?headless=1"
    }
}
