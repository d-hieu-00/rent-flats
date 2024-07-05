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
    if (isNull(cval) && isUndefined(cval) ) {
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
