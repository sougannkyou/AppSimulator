const THEME = 'shine';//dark infographic macarons roma shine vintage

function ajaxError(err, msg) {
    // alert('[错误信息]' + msg + err);
}

const DEBUG_TIME = 1;

function showTime() {
    nowtime = new Date();
    year = nowtime.getFullYear();
    month = nowtime.getMonth() + 1;
    date = nowtime.getDate();
    document.getElementById("systime").innerText = year + "年" + month + "月" + date + " " + nowtime.toLocaleTimeString();
}

setInterval("showTime()", 1000);

// ------------------ DeviceCrawlCntInfo  ------------------
function refresh_img_src(img_src) {
    let i = img_src.indexOf('?t=');
    if (i > 0) {
        return img_src.substr(0, i) + '?t=' + Math.random();
    } else {
        return img_src + '?t=' + Math.random();
    }
}

setInterval(function () {
    $(".emulator-capture").each(function (index, element) {
        // console.log(element.src);
        element.src = refresh_img_src(element.src);
    });

    $(".vm-capture").each(function (index, element) {
        // console.log(element.src);
        element.src = refresh_img_src(element.src);
    });
    // $("#current").attr('src', src = "/static/AppSimulator/images/capture.png?t=" + Math.random());
}, 1000);

setInterval(function () {
    $.ajax({
        url: '/AppSimulator/getDeviceCrawlCntAPI/',
        type: 'get',
        contentType: "application/json; charset=UTF-8",
        data: {
            app_name: mainVue.app_name,
        },
        error: function (xhr, err) {
            ajaxError(err, 'DeviceInfo');
        },
        success: function (data, textStatus) {
            let ret = data.ret;
            mainVue.devices.dedup_cnt = ret.dedup_cnt;
            mainVue.devices.cnt = ret.cnt;
        }
    });
}, 10 * 1000 * DEBUG_TIME);

setInterval(function getProxyServerInfoAPI() {
    if (mainVue.deviceId === '') {
        alert("请选择设备。");
        return false;
    }
    let opt = {
        url: '/AppSimulator/getProxyServerInfoAPI/',
        type: 'GET',
        data: {
            deviceId: mainVue.deviceId,
        },
        dataType: "json",
        error: function (xhr, err) {
            mainVue.msg = "Failure";
            console.error("[dashboard] setDeviceGPSAPI", err);
        },
        success: function (data, status) {
            mainVue.proxyServerInfo.hd_percent = data['hd_info']['percent'];
            mainVue.proxyServerInfo.memory_rate = ((data['mem_info']['total'] - data['mem_info']['free']) * 100 / data['mem_info']['total']).toFixed(1);
            mainVue.proxyServerInfo.cpu_percent = data['cpu_info']['percent'];
            mainVue.msg = "OK";
        }
    };
    $.ajax(opt);
}, 10 * 1000 * DEBUG_TIME);

setInterval(function getDevicesStatusAPI() {
    let opt = {
        url: '/AppSimulator/getDevicesStatusAPI/',
        type: 'GET',
        data: {scope_times: 30, interval_times: 10}, // 单位秒
        dataType: "json",
        data: {
            deviceId: mainVue.deviceId,
            app_name: mainVue.app_name,
        },
        error: function (xhr, err) {
            mainVue.msg = "Failure";
            console.error("[dashboard] getDevicesStatusAPI", err);
        },
        success: function (data, status) {
            console.log("getDevicesStatusAPI", mainVue.devices.statusList.length, data.ret);
            for (let i = 0; i < 100; i++) {
                mainVue.devices.statusList.shift();
            }
            for (let i = 0; i < data.ret.length; i++) {
                mainVue.devices.statusList.push(data.ret[i]);
            }
            mainVue.msg = "OK";
        }
    };
    $.ajax(opt);
}, 10 * 1000 * DEBUG_TIME); // 单位秒

function getDeviceCaptureAPI() {
    $.ajax({
        url: '/AppSimulator/getDeviceCaptureAPI/',
        type: 'get',
        contentType: "application/json; charset=UTF-8",
        error: function (xhr, err) {
            ajaxError(err, 'getDeviceCaptureAPI');
        },
        success: function (data, textStatus) {
        }
    });
}

getDeviceCaptureAPI();

// (function memoryMonitor() {
//     let myChart = echarts.init(document.getElementById("memory_monitor"), THEME);
//
//     let base = 1;
//     let hour = [];
//
//     let data = [0];
//     let now = base;
//
//     function addData(shift) {
//         hour.push(now);
//         data.push(100 - 50);
//
//         if (shift) {
//             hour.shift();
//             data.shift();
//         }
//         if (now > 29) {
//             now = 1;
//         } else {
//             now = now + 1;
//         }
//     }
//
//     for (let i = 1; i < 30; i++) {
//         addData();
//     }
//
//     let option = {
//         xAxis: {
//             type: 'category',
//             boundaryGap: false,
//             data: hour
//         },
//         yAxis: {
//             boundaryGap: [0, '50%'],
//             type: 'value',
//             max: 100
//         },
//         series: [
//             {
//                 name: 'memory',
//                 type: 'line',
//                 smooth: true,
//                 symbol: 'none',
//                 stack: 'a',
//                 areaStyle: {
//                     normal: {}
//                 },
//                 color: ['#1cffac'],
//                 data: data,
//                 markLine: {
//                     data: [
//                         // 纵轴，默认
//                         {type: 'max', name: '最大值', itemStyle: {normal: {color: '#dc143c'}}},
//                     ]
//                 }
//             }
//         ]
//     };
//
//     setInterval(function () {
//         addData(true);
//         myChart.setOption({
//             xAxis: {
//                 data: hour
//             },
//             series: [{
//                 name: 'memory',
//                 data: data
//             }]
//         });
//     }, 2000);
//
//     if (option && typeof option === "object") {
//         myChart.setOption(option, true);
//     }
// })();

//
// (function getResultSample() {
//     $.ajax({
//         url: '/AppSimulator/getResultSampleAPI/',
//         type: 'get',
//         contentType: "application/json; charset=UTF-8",
//         error: function (xhr, err) {
//             ajaxError(err, 'DeviceInfo');
//         },
//         success: function (data, textStatus) {
//             let ret = data.ret;
//             $('#result_sample_1').text(ret.device1);
//             $('#result_sample_2').text(ret.device2);
//             $('#result_sample_3').text(ret.device3);
//             $('#result_sample_4').text(ret.device4);
//         }
//     });
// })();







