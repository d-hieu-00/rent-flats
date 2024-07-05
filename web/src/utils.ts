import { ref } from 'vue';

export function isNull(inVar: any) {
    return inVar === null;
};

export function isUndefined(inVar: any) {
    return inVar === undefined;
};

export function setCookie(cookieName: string, cookieValue: string, expireDays?: number) {
    var exdate = new Date();
    if (expireDays === null || expireDays === undefined) {
        document.cookie = cookieName + "=" + cookieValue;
    } else {
        exdate.setDate(exdate.getDate() + expireDays);
        document.cookie = cookieName + "=" + cookieValue + (";expires=" + exdate.toUTCString());
    }
}

export function getCookie(name: string) : string | undefined {
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
    if (arr = document.cookie.match(reg)) {
        return arr[2];
    } else {
        return undefined;
    }
}

export function delCookie(name: string) {
    const cval = getCookie(name);
    if (!isNull(cval) && !isUndefined(cval) ) {
        let exp = new Date();
        exp.setTime(exp.getTime() - 1);
        document.cookie = name + "=" + cval + ";expires=" + exp.toUTCString();
    }
}

export function isRespError(data: object | any) : boolean {
    if (data["error"]) {
        return true;
    }
    if (data["err"]) {
        return true;
    }
    return false;
}

export function fetchRespError(data: object | any) : string {
    if (data["error"]) {
        return data["error"];
    }
    if (data["err"]) {
        return data["err"];
    }
    return "";
}

const eventBus = ref(new Map());

const emitEvent = (eventName: string, payload?: any) => {
    if (eventBus.value.has(eventName)) {
        eventBus.value.get(eventName).forEach((callback: (_: any) => any) => callback(payload));
    }
};

const onEvent = (eventName: string, callback: any) => {
    if (!eventBus.value.has(eventName)) {
        eventBus.value.set(eventName, []);
    }
    eventBus.value.get(eventName).push(callback);
};

const offEvent = (eventName: string, callback: any) => {
    if (eventBus.value.has(eventName)) {
        const callbacks = eventBus.value.get(eventName);
        const index = callbacks.indexOf(callback);
        if (index > -1) {
            callbacks.splice(index, 1);
        }
    }
};

export { emitEvent, onEvent, offEvent };
