let THEME = 'shine';//dark infographic macarons roma shine vintage

function ajaxError(err, msg) {
    // alert('[错误信息]' + msg + err);
}

// ------------------ DeviceInfo  ------------------
(function getDeviceInfo() {
    $.ajax({
        url: '/AppSimulator/getDeviceInfoAPI/',
        type: 'get',
        contentType: "application/json; charset=UTF-8",
        error: function (xhr, err) {
            ajaxError(err, 'DeviceInfo');
        },
        success: function (data, textStatus) {
            let ret = data.ret;
            $('#device1').text(ret.device1);
            $('#device2').text(ret.device2);
            $('#device3').text(ret.device3);
            $('#device4').text(ret.device4);
        }
    });
})();
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







