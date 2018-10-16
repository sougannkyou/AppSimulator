// const redis = require("redis");
const redis = require("C:\\Users\\zhxg\\AppData\\Roaming\\npm\\node_modules\\redis\\index.js");
// const client = redis.createClient(6379, '192.168.17.109', {});
const client = redis.createClient(6379, '172.16.2.109', {});
const set_name = "xiaohongshu_meilinkai";
//const set_name = "xiaohongshu_meilinkai_1";

// redis 链接错误
client.on("error", function (error) {
  console.log(error);
});

function save_data(data) {
  console.log(data);
  client.select(15, function (error) {
    if (error) {
      console.log(error);
    } else {
      //client.sadd("xiaohongshu_meilinkai-" + new Date().toLocaleDateString(), JSON.stringify({
      console.log(1111111111111);
      client.sadd([set_name, data], function (err, reply) {
        console.log(33333333333);
        console.log(reply);
        console.log(44444444444);

      });
      console.log(2222222222222);
    }
  });
}

function save_data_all(data) {
  console.log(data);
  client.select(14, function (error) {
    if (error) {
      console.log(error);
    } else {
      client.sadd([set_name, data], function (err, reply) {
        console.log(reply);
      });
    }
  });
}

module.exports = {
  * beforeSendResponse(requestDetail, responseDetail) {
    return new Promise((resolve, reject) => {
      const newResponse = responseDetail.response;
      let statusCode = newResponse.statusCode;

      if (statusCode === 200 || statusCode === 206 || statusCode === 301 || statusCode === 302) {
        let detailUrl = requestDetail.url;
        if (detailUrl.indexOf("www.xiaohongshu.com/api/sns/v9/note") !== -1) {
          let body = JSON.parse(new Buffer(newResponse.body, 'base64').toString())
          save_data_all(body);
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
            'siteName': '小红书',
            'data_db': '',
            'url': url,
            'content': content,
          }
          save_data(JSON.stringify(data));
        }
      }
      // -----------------------------------------------------------------------------------
      resolve({response: newResponse});
      // -----------------------------------------------------------------------------------
    });
  }
};