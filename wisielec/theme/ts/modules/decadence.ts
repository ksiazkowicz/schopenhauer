import { csrfPOST, query, queryInElement, popAttribute } from "./utils";

function connect_listener(element: Element) {
    let listener = window["UpdateListener"] || undefined;
    if (listener) {
        listener.init(element);
    }
}

export class ErrorOptions {
    auto_dismissible: boolean = true;
    dismiss_timeout: number = 4000;
    icon: string = "";
    has_button: boolean = false;
    button_text: string = "Close";
    button_href: string = "";
    template: string = "includes/decadence/alert_block.html";
    string: string = "";
    error_level: string = "";
    alert_id: any;
    avatar: string;

    constructor(options: object = {}) {
        for (let key of Object.keys(options))
            this[key] = options[key];
    }
}

export type ErrorLevel = "success" | "info" | "warning" | "danger";

export function show_info_banner(banner_id: string, auto_hide: boolean) {
    // hide all currently visible banners
    for (let e of query("#header-alerts .header-alert")) {
        e.classList.toggle("hidden", true);
    }

    // show banner by given ID
    for (let banner of query("#" + banner_id)) {
        banner.classList.toggle("hidden", false);

        // enable auto_hide
        if (auto_hide) {
            setTimeout(() => {
                banner.classList.toggle("hidden", true);
            }, 4000);
        }
    }
}

export function show_info_block(error_level: ErrorLevel, string: string, options: ErrorOptions) {
    /*
        Shows notification block at the top of the page.
     */
    options.string = string;
    options.error_level = error_level;
    options.alert_id = (new Date()).getTime();

    if (options.auto_dismissible) {
        // enable auto dismissing
        $(function () {
            setTimeout(function () {
                $("#alert-" + options.alert_id).alert('close');
            }, options.dismiss_timeout);
        });
    }

    include_from_template(query("#body-alerts")[0], options.template, options, "afterbegin", function () { });

    return options.alert_id
}

export function include_from_template(element: Element, template: string, data: any, mode: InsertPosition, callback: Function = function () { }) {
    /*
        Uses API to generate blocks from Django templates and includes them in the page.
        Takes css selector (like "#bread"), template file name ("includes/cancer.html") and context data.
        Also you can switch between different inclusion modes.
     */
    data.template = template;

    csrfPOST("/api/v1/decadence/template/", { "data": JSON.stringify(data) }).then((response) => {
        return response.text();
    }).then((text) => {
        element.insertAdjacentHTML(mode, text);
        connect_listener(element);
        callback();
    }).catch((ex) => {
        if (template != "includes/decadence/alert_block.html") {
            show_info_block("danger", "Error occured while rendering template '" + template + "'. Some things might not work properly. \n\n Details: '" + ex + "'.", new ErrorOptions);
        }
    });
}

export function batch_render(objects: Array<DecadenceObject>, callback: Function, container: string) {
    let data: object = {
        "template": "includes/decadence/batch.html",
        "batch": [],
        "container": "div"
    };

    for (let obj of objects) {
        data["batch"].push({
            "data": obj.data,
            "template": obj.template,
        });
    }

    if (container != undefined) {
        data["container"] = container;
    }

    csrfPOST("/decadence/template/", { "data": JSON.stringify(data) }).then((response) => {
        return response.text();
    }).then((text) => {
        // create new element
        let temp = document.createElement('div');
        temp.innerHTML = text;

        // iterate through all objects and render them
        for (let i = 0; i < objects.length; i++) {
            let new_element = <Element>temp.children[i];
            objects[i].__render(new_element.innerHTML);
        }
        callback();
    }).catch((ex) => {
        show_info_block("danger", "Error occured while rendering. Some things might not work properly. \n\n Details: '" + ex + "'.", new ErrorOptions);
    });
}

export class DecadenceObject {
    template: string;
    element: Element;
    data: object;
    last_render: number;
    rendered: boolean;
    fields: object = new Object();

    constructor(template: string, data: object) {
        if (template != "")
            this.template = template;
        this.data = data;
        this.rendered = false;
    }

    stripAttributes() {
        for (let field of Object.keys(this.fields)) {
            let attribute_name = "data-" + field.replace(/_/g, "-");
            if (this.element.hasAttribute(attribute_name)) {
                this.element.removeAttribute(attribute_name);
            } else {
                for (let e of queryInElement(this.element, "[" + attribute_name + "]")) {
                    e.removeAttribute(attribute_name);
                    break;
                }
            }
        }

    }

    importElement(element: Element) {
        /**
         * Takes element and generates data based on data attributes in Element and this.fields
         */
        this.element = element;
        for (let field of Object.keys(this.fields)) {
            // get data attribute and remove it because we don't need it in DOM anymore
            let attribute_name = "data-" + field.replace(/_/g, "-");
            let value = undefined;
            if (element.hasAttribute(attribute_name)) {
                value = popAttribute(element, attribute_name);
            } else {
                for (let e of queryInElement(element, "[" + attribute_name + "]")) {
                    value = popAttribute(e, attribute_name);
                    break;
                }
            }
            // if data attribute was not found, use default from this.fields
            this.data[field] = value || this.fields[field];
        }

        // well, we can assume it's rendered
        this.rendered = true;
        this.renderCallback();
    }

    insertElementInto(target_element: Element, mode: InsertPosition, element: string) {
        /**
         * Creates a temporary element, which we can then replace with our render result.
         */
        let hash = "decadence-temp-" + Date.now() + Math.random().toString(36).substr(2, 10);
        target_element.insertAdjacentHTML(mode, "<" + element + " id='" + hash + "'></" + element + ">");
        this.element = document.getElementById(hash);
        return this;
    }

    insert(element: Element, mode: InsertPosition) {
        /**
         * Shorthand for insertElementInto()
         */
        let element_type = "div";
        if (element.nodeName == "TBODY" || element.nodeName == "TABLE")
            element_type = "tr";
        return this.insertElementInto(element, mode, element_type);
    }

    update(fields: object) {
        /**
         * Updates fields in element with data provided by fields object.
         */
        if (this.element) {
            for (let field of Object.keys(fields)) {
                // Iterate through all fields, find a proper one by data-decadence attribute and update value
                for (let e of queryInElement(this.element, "[data-decadence='" + field + "']"))
                    e.innerHTML = fields[field];
                this.data[field] = fields[field];
            }
        }
        return this;
    }

    renderCallback() { }

    __render(text: string) {
        // create new element
        let temp: any;
        if (this.element.nodeName == "TR") {
            temp = document.createElement('table');
        } else {
            temp = document.createElement('div');
        }
        temp.innerHTML = text;
        let new_element = <Node>temp.children[0]; // for some reason first element is #text
        if (this.element.nodeName == "TR") {
            // DOM, what have I ever done to you?! :(
            new_element = <Node>temp.children[0].children[0];
        }

        // replace element with new element
        this.element.parentElement.replaceChild(<Node>new_element, this.element);
        this.element = <Element>new_element;
        this.rendered = true;

        // run callback
        connect_listener(this.element);
        this.renderCallback();
        this.stripAttributes();

        // dispatch "contentChanged" event
        let parent = this.element.parentElement;

        // check if parent is a table, we might need to get a few levels up
        if (parent.nodeName == "TBODY")
            parent = parent.parentElement;
        if (parent.nodeName == "TABLE")
            parent = parent.parentElement;

        parent.dispatchEvent(new Event("contentChanged"));
    }

    render() {
        /** 
         * Renders object using Decadence and AJAX. 
        */
        // make sure template is available in data
        this.data["template"] = this.template;

        // remember time when this function was called
        let render_time = Date.now();
        this.last_render = render_time;
        // fetch template from Decadence
        csrfPOST("/decadence/template/", { "data": JSON.stringify(this.data) }).then((response) => {
            return response.text();
        }).then((text) => {
            // avoid race condition
            if (this.last_render == render_time) {
                this.__render(text);
            }
        }).catch((ex) => {
            // show error
            show_info_block("danger", "Error occured while rendering template '" + this.template + "'. Some things might not work properly. \n\n Details: '" + ex + "'.", new ErrorOptions);
        });
    }
}