//----------------------------------------------------------------------------
Vue.filter("formatTime", function (nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString().replace(/:\d{1,2}$/, ' ');
});

Vue.filter("hasInfo", function (s) {
    if (typeof(s) === "undefined" || (typeof(s) === "string" && s === "")) {
        return "无";
    } else {
        return "有";
    }
});

function isNullOrEmpty(o) {
    return null === o || 'null' === o || '' === o || undefined === o || 'undefined' === o;
}

Vue.filter("count", function (arr) {
    if (!isNullOrEmpty(arr)) {
        return arr.length;
    } else {
        return 0;
    }
});
