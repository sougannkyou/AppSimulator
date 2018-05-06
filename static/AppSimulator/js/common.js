const HOST = "";
const PAGE_SIZE = 20;
const XPATH_ERROR = "错误:xpath表达式";

const NODES_OPTIONS = [
    {name: 'root', value: 'root'}
];

const DATA_DB = "redis://192.168.16.223/15/visual_data";

const TIME_FORMAT_OPTIONS = [
    {name: '不使用url作为时间过滤', value: {date_format: '', regex: ''}},
    {name: '使用: YYYY-mm-dd', value: {date_format: '%Y-%m-%d', regex: '\\d{4}-\\d{2}-\\d{2}'}},
    {name: '使用: YYYYmmdd', value: {date_format: '%Y%m%d', regex: '\\d{8}'}},
    {name: '使用: YY/mmdd', value: {date_format: '%Y/%m%d', regex: '\\d{2}\/\\d{4}'}},
    {name: '使用: YYYY-mm/dd', value: {date_format: '%Y-%m/%d', regex: '\\d{4}-\\d{2}\/\\d{2}'}}
];

const INFO_FLAG_OPTIONS = [
    {name: '新闻', value: '01'},
    {name: '论坛', value: '02'},
    {name: '博客', value: '03'},
    {name: '新浪微博', value: '0401'},
    {name: '腾讯微博', value: '0402'},
    {name: '平煤', value: '05'},
    {name: '微信', value: '06'},
    {name: '视频', value: '07'},
    {name: '长微博', value: '08'},
    {name: 'APP', value: '09'},
    {name: '评论', value: '10'},
    {name: '搜索', value: '99'}
];


function callError(func, msg) {
    //alert('[error] ' + func + ": " + msg);
    console.error('[error]',func, msg);
}

function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r !== null) {
        return decodeURI(r[2]);
    }
    return null;
}

function isNullOrEmpty(o) {
    return null === o || 'null' === o || '' === o || undefined === o || 'undefined' === o;
}

function isDiscuz() {
    //<meta name="generator" content="Discuz! X3.2" />
    //var Discuz = $("#html").contents().find('meta[name="generator"]').attr('content');
    var generator = document.getElementById("html").contentDocument.getElementsByTagName("meta")['generator'];
    //document.querySelector('meta[name="generator"]').getAttribute('content');
    return (!isNullOrEmpty(generator) && generator.getAttribute('content').indexOf("Discuz") !== -1);
}

function _getNavInfo(obj) {
    $.ajaxSetup({
        data: {csrfmiddlewaretoken: '{{ csrf_token }}'}
    });
    $.ajax({
        url: '/webSpider/getNavInfoAPI/',
        type: 'GET',
        data: {
            taskId: obj.taskId
        },
        dataType: "json",
        error: function (xhr, err) {
            callError("[xpath] _getNavInfoAPI GET", err);
        },
        success: function (data, status) {
            obj.hasDetail = data['hasDetail'];
            obj.navInfo.levels_cnt = data['levels_cnt'];
            obj.navInfo.levels = new Array(data['levels_cnt']);
            for (var i = 0; i < data['levels_cnt']; i++) {
                obj.navInfo.levels[i] = i;
            }
        }
    });
}

function navTo(target, taskId, level) { // ---- webSpider ----
    switch (target) {
        case "board":
            window.location.href = "/webSpider/board/";
            break;
        case "main":
            window.location.href = "/webSpider/main/";
            break;
        case "hubs":
            window.location.href = "/webSpider/hubs/?taskId=" + taskId + "&level=" + level;
            break;
        case "detail":
            window.location.href = "/webSpider/detail/?taskId=" + taskId;
            break;
        case "test":
            window.location.href = "/webSpider/spiderTest/?taskId=" + taskId;
            break;
        case "simulator":
            window.location.href = "/webSpider/simulator/";
            break;
        default:
            break;
    }
}

function send(opt) { // webSpider or eSpider网络版
    $.ajaxSetup({
        data: {csrfmiddlewaretoken: '{{ csrf_token }}'}
    });
    $.ajax(opt);
}