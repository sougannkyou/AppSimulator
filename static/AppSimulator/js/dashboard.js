const THEME = 'shine';//dark infographic macarons roma shine vintage

function ajaxError(err, msg) {
    // alert('[错误信息]' + msg + err);
}

const DEBUG_TIME = 1;
// ------------------ DeviceCrawlCntInfo  ------------------
setInterval(function () {
    $("#before").attr('src', src = "/static/AppSimulator/images/capture_before.png?t=" + Math.random());
    $("#current").attr('src', src = "/static/AppSimulator/images/capture.png?t=" + Math.random());
}, 1000);

setInterval(function () {
    $.ajax({
        url: '/AppSimulator/getDeviceCrawlCntAPI/',
        type: 'get',
        contentType: "application/json; charset=UTF-8",
        error: function (xhr, err) {
            ajaxError(err, 'DeviceInfo');
        },
        success: function (data, textStatus) {
            let ret = data.ret;
            mainVue.device1.cnt = ret.device1;
            mainVue.device2.cnt = ret.device2;
            mainVue.device3.cnt = ret.device3;
            mainVue.device4.cnt = ret.device4;
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
        error: function (xhr, err) {
            mainVue.msg = "Failure";
            console.error("[dashboard] getDevicesStatusAPI", err);
        },
        success: function (data, status) {
            let ret = data.ret;
            // console.log("getDevicesStatusAPI", ret);
            mainVue.device1.status = ret.device1;
            mainVue.device2.status = ret.device2;
            mainVue.device3.status = ret.device3;
            mainVue.device4.status = ret.device4;
            mainVue.msg = "OK";
        }
    };
    $.ajax(opt);
}, 30 * 1000 * DEBUG_TIME); // 单位秒

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







