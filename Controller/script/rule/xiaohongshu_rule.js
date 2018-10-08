// const request = require("C:\\Users\\zhxg\\AppData\\Roaming\\npm\\node_modules\\request\\index.js");
const request = require("request");
//const URL="http://172.16.253.147:8000/apiadmin/android/interception/";
//const URL="http://192.168.16.223:8000/apiadmin/android/interception/";
const URL = "http://ispider.istarshine.com/apiadmin/android/interception/";
const SET_NAME = "xiaohongshu_meilinkai";


function save_data(data) {
  request.post(URL, {form: {"content": JSON.stringify(data), "task_id": SET_NAME}}, function (error, response, body) {
    if (!error && response.statusCode == 200) {
      console.log(body) // 请求成功的处理逻辑
    }
  });
};


module.exports = {
  * beforeSendResponse(requestDetail, responseDetail) {
    return new Promise((resolve, reject) => {
      const newResponse = responseDetail.response;
      let statusCode = newResponse.statusCode;

      if (statusCode === 200 || statusCode === 206 || statusCode === 301 || statusCode === 302) {
        let detailUrl = requestDetail.url;
        if (detailUrl.indexOf("www.xiaohongshu.com/api/sns/v9/note") != -1) {
          let body = JSON.parse(new Buffer(newResponse.body, 'base64').toString())
          let title = body.data.share_info.content;
          let ctimestamp = body.data.post_time * 1000 - 3600 * 8 * 1000;
          let ctime = new Date(ctimestamp).toLocaleString();
          let gtimestamp = new Date().getTime() - 3600 * 8 * 1000;
          let gtime = new Date(gtimestamp).toLocaleString();
          let url = body.data.share_info.link;
          let source = body.data.user.nickname;
          let content = body.data.desc;

          let data = {
            'title': title,
            'ctime': ctime,
            'gtime': gtime,
            'source': source,
            'retweeted_source': '',
            'channel': '',
            'channel_url': '',
            'siteName': '小红书',
            'data_db': '',
            'url': url,
            'content': content,
          }
          save_data(data);
        }
      }
      // -----------------------------------------------------------------------------------
      resolve({response: newResponse});
      // -----------------------------------------------------------------------------------
    });
  }
};