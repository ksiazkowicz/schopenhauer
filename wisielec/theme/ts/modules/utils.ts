import { show_info_block, show_info_banner, ErrorOptions } from "./decadence";
import bootbox = require("bootbox");

export function getURIParameters(uri: string) {
    if (uri.indexOf("?") != -1) {
        let query = uri.split("?")[1];
        let parameters = {};
        query.split("&").map((part: any) => {
            let item = part.split("=");
            parameters[item[0]] = decodeURIComponent(item[1]);
        })
        return parameters;
    }
    return {};
}

export function popAttribute(element: Element, name: string): string {
    let result: string = element.getAttribute(name);
    element.removeAttribute(name);
    return result;
}

export function encodeURIObject(body: object): string {
    let urlencoded_body: string = "";
    for (let key of Object.keys(body)) {
        if (urlencoded_body != "")
            urlencoded_body += "&";
        urlencoded_body += encodeURIComponent(key) + "=" + encodeURIComponent(body[key]);
    }
    return urlencoded_body;
}

export function csrfPOST(url: string, body: object): Promise<Response> {
    /**
     * Wrapper for fetch() that makes sure there is csrf token included in a request.
     */

    // add CSRF token to request body
    body["csrfmiddlewaretoken"] = read_cookie("csrftoken");

    // call fetch
    return fetch(url, {
        method: 'POST',
        headers: new Headers({ 'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest' }),
        body: encodeURIObject(body),
        credentials: 'same-origin',
    });
}

export function ajaxGET(url: string, body: object): Promise<Response> {
    /**
     * Wrapper for fetch() so I don't have to remember X-Requested-With
     */
    // use split because URL might already hold some parameters
    let request_url = url.split("?")[0];
    // apply given body to URL
    if (body) {
        request_url += "?" + encodeURIObject(body);
    }

    // run fetch()
    return fetch(request_url, {
        method: 'GET',
        headers: new Headers({ 'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest' }),
        credentials: 'same-origin',
    });
}


export function read_cookie(name: string) {
    let nameEQ = name + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1, c.length);
        }
        if (c.indexOf(nameEQ) === 0) {
            return c.substring(nameEQ.length, c.length);
        }
    }
    return null;
}

export function queryInElement(element: any, selector: string) {
    return [].slice.call(element.querySelectorAll(selector));
}

export function query(selector: string) {
    return queryInElement(document, selector);
}

export function replaceLink(element: Element, callback: Function) {
    let url = element.getAttribute("href");
    element.classList.add("restore-pointer");
    element.removeAttribute("href");
    element.addEventListener("click", function () {
        callback(url, element);
    });
}

export class ReconnectingWebsocketHandler {
    /**
     * Wrapper for WebSocket with common logic used by Feeds, Update API, Chat API etc.
     * 
     * Implements automatic reconnecting and a basic queue for messages.
     */
    ws: WebSocket;
    url: string;
    queue: Array<any> = new Array<any>();
    reconnect: boolean = true;
    supports_batch: boolean = false;

    is_reconnecting: boolean = false;


    constructor() {
        this.queue = new Array<string>();
    }

    isConnected() {
        return this.ws ? this.ws.readyState == WebSocket.OPEN : false;
    }

    onMessage(evt: any) { }

    onOpen() {
        if (this.is_reconnecting) {
            show_info_banner("header-connection-success", true);
        }
        this.is_reconnecting = true;

        if (this.supports_batch) {
            this.ws.send(JSON.stringify({ "batch": this.queue }));
            this.queue = new Array<any>();
        } else {
            while (this.queue.length > 0) {
                let msg = this.queue.pop();
                this.ws.send(JSON.stringify(msg));
            }
        }
    }
    onClose() {
        setTimeout(() => { this.connect(); }, 1000);
        show_info_banner("header-connection-error", false);
    }

    connect() {
        if (this.isConnected()) {
            this.ws.close();
        }

        let protocol = location.protocol == "https:" ? "wss://" : "ws://";
        this.ws = new WebSocket(protocol + window.location.host + this.url);
        this.ws.onopen = () => { this.onOpen(); };
        this.ws.onmessage = (evt: any) => { this.onMessage(evt); };
        this.ws.onclose = () => { this.onClose(); };
    }

    send(message: any) {
        if (this.isConnected()) {
            this.ws.send(JSON.stringify(message));
        } else {
            this.queue.push(message);
        }
    }
}