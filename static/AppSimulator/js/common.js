const HOST = "";
const PAGE_SIZE = 20;

function callError(func, msg) {
    //alert('[error] ' + func + ": " + msg);
    console.error('[error]', func, msg);
}

function isNullOrEmpty(o) {
    return null === o || 'null' === o || '' === o || undefined === o || 'undefined' === o;
}

function send(opt) { // webSpider or eSpider网络版
    $.ajaxSetup({
        data: {csrfmiddlewaretoken: '{{ csrf_token }}'}
    });
    $.ajax(opt);
}