import { DecadenceObject } from './decadence';
declare module 'modules/utils' {
	export function read_cookie(name: string): string;
	export function query(selector: string): Array<Element>;
	export function queryInElement(element: any, selector: string): Array<Element>;
	export function replaceLink(element: Element, callback: Function): any;
	export function popAttribute(element: Element, name: string): string;
	export function csrfPOST(url: string, body: object): Promise<Response>;
	export function ajaxGET(url: string, body: object): Promise<Response>;
	export function encodeURIObject(body: object): string;

	export class ReconnectingWebsocketHandler {
		constructor(options: object);

		isConnected(): boolean;
		onMessage(evt: any): void;
		onOpen(): void;
		onClose(): void;
		connect(): void;
		send(message: string): void;
	}
}
declare module 'modules/decadence' {
	export class ErrorOptions {
		auto_dismissible: boolean;
		dismiss_timeout: number;
		icon: string;
		has_button: boolean;
		button_text: string;
		button_href: string;
		template: string;
		string: string;
		error_level: string;
		alert_id: any;
	}
	export type ErrorLevel = "success" | "info" | "warning" | "danger";
	export function show_info_banner(banner_id: string, auto_hide: boolean): void;
	export function show_info_block(error_level: ErrorLevel, string: string, options: ErrorOptions): any;
	export function include_from_template(element: Element, template: string, data: any, mode: InsertPosition, callback: Function): void;
	export function batch_render(objects: Array<DecadenceObject>, callback: Function): void;

	export class DecadenceObject {
		template: string;
		element: Element;
		data: any;
		last_render: number;

		constructor(template: string, data: any);
		update(fields: object): DecadenceObject;
		insert(element: Element, mode: InsertPosition): DecadenceObject;
		importElement(element: Element): void;
		stripAttributes(): void;
		renderCallback(): void;
		render(): void;
	}

}