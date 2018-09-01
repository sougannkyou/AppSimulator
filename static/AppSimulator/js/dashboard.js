const THEME = 'shine';//dark infographic macarons roma shine vintage

function ajaxError(err, msg) {
  // alert('[错误信息]' + msg + err);
}

const DEBUG_TIME = 1;


setInterval(function () {
  nowtime = new Date();
  // year = nowtime.getFullYear();
  // month = nowtime.getMonth() + 1;
  // date = nowtime.getDate();
  document.getElementById("systime").innerText = nowtime.toLocaleString();
}, 1000);

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
    if (element.src.indexOf('default.png') === -1) element.src = refresh_img_src(element.src);
  });

  $(".vm-capture").each(function (index, element) {
    if (element.src.indexOf('default.png') === -1) element.src = refresh_img_src(element.src);
  });
}, 5000);







