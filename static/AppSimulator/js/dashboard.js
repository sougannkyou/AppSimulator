let THEME = 'shine';//dark infographic macarons roma shine vintage

function ajaxError(err, msg) {
    // alert('[错误信息]' + msg + err);
}

// ------------------ DeviceInfo  ------------------
window.setInterval(function () {
    $.ajax({
        url: '/AppSimulator/getDeviceInfoAPI/',
        type: 'get',
        contentType: "application/json; charset=UTF-8",
        error: function (xhr, err) {
            ajaxError(err, 'DeviceInfo');
        },
        success: function (data, textStatus) {
            let ret = data.ret;
            mainVue.device1_cnt = ret.device1;
            mainVue.device2_cnt = ret.device2;
            mainVue.device3_cnt = ret.device3;
            mainVue.device4_cnt = ret.device4;
            // $('#device1').text(ret.device1);
        }
    });
}, 5000)


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







