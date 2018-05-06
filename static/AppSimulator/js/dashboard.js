var THEME = 'shine';//dark infographic macarons roma shine vintage

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

// ------------------ 域名总数 ------------------
function newDomainOpt(THEME, opt) {
    $.ajax({
        url: '/AppSimulator/drawNewDomainAPI/',
        type: 'POST',
        data: {opt: opt},
        dataType: "json",
        error: function (xhr, err) {
            ajaxError(err, '域名总数');
        },
        success: function (data, textStatus) {
            $('#newDomain').remove();
            $('#newDomainParent').html('<div id="newDomain" style="width:100%;height:270px;"></div>');

            let obj = document.getElementById('newDomain');
            let myChart = echarts.init(obj, THEME);
            let option = {
                color: ['#39BCD1'],
                title: {
                    text: ''
                },
                tooltip: {
                    trigger: 'axis'
                },
                toolbox: {
                    feature: {
                        dataView: {show: false, readOnly: false},
                        magicType: {show: false, type: ['line']},
                        restore: {show: false},
                        saveAsImage: {show: false}
                    }
                },
                legend: {
                    // data: ['日增数','总数']
                    data: ['总数']
                },
                dataZoom: [
                    {
                        type: 'slider',
                        start: 1,
                        end: 100
                    },
                    {
                        type: 'inside',
                        start: 1,
                        end: 100
                    }
                ],
                xAxis: {
                    data: data['timeList'],
                    axisLabel: {
                        interval: data['interval'],
                        rotate: 60,
                        textStyle: {
                            //color: "blue",
                            fontSize: 6
                        }
                    }
                },
                yAxis: [
                    // {
                    //     type: 'value',
                    //     name: '日增数',
                    //     axisLabel: {
                    //         formatter: '{value}'
                    //     }
                    // },
                    {
                        type: 'value',
                        name: '总数',
                        axisLabel: {
                            formatter: '{value}'
                        }
                    }
                ],
                series: [
                    // {
                    //     name: '日增数',
                    //     barWidth: 10,
                    //     type: 'bar',
                    //     data: data['domainDaysCnt']
                    // },
                    {
                        name: '总数',
                        type: 'line',
                        data: data['domainTotalCnt']
                    }
                ]
            };
            myChart.setOption(option);
        }
    });
}

function reDrawNewDoamin(opt) {
    var THEME = '';
    newDomainOpt(THEME, opt);
}
// newDomainOpt(THEME, 'week');


// ------------------ 新站发现(日增量) ------------------
function newDomainOptDays(THEME, opt) {
    $.ajax({
        url: '/AppSimulator/drawNewDomainAPI/',
        type: 'POST',
        data: {opt: opt},
        dataType: "json",
        error: function (xhr, err) {
            ajaxError(err, '新站发现(日增量)');
        },
        success: function (data, textStatus) {
            $('#entranceCntByDays').remove();
            $('#newEntranceCntByDays').html('<div id="entranceCntByDays" style="width:100%;height:270px;"></div>');

            var obj = document.getElementById('newDomainDays');
            var myChart = echarts.init(obj, THEME);
            var option = {
                color: ['#39BCD1'],
                title: {
                    text: ''
                },
                tooltip: {
                    trigger: 'axis'
                },
                toolbox: {
                    feature: {
                        dataView: {show: false, readOnly: false},
                        magicType: {show: false, type: ['line']},
                        restore: {show: false},
                        saveAsImage: {show: false}
                    }
                },
                legend: {
                    data: ['日增数']
                },
                dataZoom: [
                    {
                        type: 'slider',
                        start: 1,
                        end: 100
                    },
                    {
                        type: 'inside',
                        start: 1,
                        end: 100
                    }
                ],
                xAxis: {
                    data: data['timeList'],
                    axisLabel: {
                        interval: data['interval'],
                        rotate: 60,
                        textStyle: {
                            //color: "blue",
                            fontSize: 6
                        }
                    }
                },
                yAxis: [
                    {
                        type: 'value',
                        name: '日增数',
                        axisLabel: {
                            formatter: '{value}'
                        }
                    },
                    // {
                    //     type: 'value',
                    //     name: '总数',
                    //     axisLabel: {
                    //         formatter: '{value}'
                    //     }
                    // }
                ],
                series: [
                    {
                        name: '日增数',
                        barWidth: 10,
                        type: 'bar',
                        data: data['domainDaysCnt']
                    },
                    // {
                    //     name: '总数',
                    //     type: 'line',
                    //     yAxisIndex: 1,
                    //     data: data['domainTotalCnt']
                    // }
                ]
            };
            myChart.setOption(option);
        }
    });
}

function reDrawNewDoaminDays(opt) {
    var THEME = '';
    newDomainOptDays(THEME, opt);
}
// newDomainOptDays(THEME, 'week');

// ------------------ 入口采集量排名 ------------------
function entranceRankFunc(THEME) {
    $.ajax({
        url: '/AppSimulator/drawHubPageRankAPI/',
        type: 'get',
        contentType: "application/json; charset=UTF-8",
        error: function (xhr, err) {
            ajaxError(err, '入口采集量排名');
        },
        success: function (data, textStatus) {

            var myChart = echarts.init(document.getElementById('entrance_rank'), THEME);
            var urlList = data["hubPageUrl"];
            var crawledNumList = data["hubPageCrawledNum"];
            var option = {
                    color: ['#348017'],
                    title: {
                        text: ''
                    },
                    tooltip: {
                        trigger: 'item',
                        formatter: function (params) {
                            var x = params.name;
                            var i = parseInt(x.substring(3, x.length));

                            return crawledNumList[i - 1] + '<br/>' + urlList[i - 1];
                        }
                    },
                    legend: {
                        data: ['已采集详情页数']
                    },
                    xAxis: {
                        //data: data["hubPageUrl"]
                        data: ['No.1', 'No.2', 'No.3', 'No.4', 'No.5', 'No.6', 'No.7', 'No.8', 'No.9', 'No.10']
                    },
                    yAxis: {},
                    series: [{
                        name: '已采集详情页数',
                        stack: '总量',
                        barWidth: 10,
                        type: 'bar',
                        data: data["hubPageCrawledNum"]
                    }]
                }
                ;
            myChart.setOption(option);
        }
    });
}
// entranceRankFunc(THEME);

// ------------------ redis_monitor ------------------
function redisMonitorFunc(THEME) {
    var myChart = echarts.init(document.getElementById("redis_monitor"), THEME);

    var base = 1;
    var hour = [];

    var data = [0];
    var now = base;

    function addData(shift) {
        hour.push(now);
        data.push(Math.random() * 60);

        if (shift) {
            hour.shift();
            data.shift();
        }
        if (now > 23) {
            now = 1;
        } else {
            now = now + 1;
        }
    }

    for (var i = 1; i < 24; i++) {
        addData();
    }

    var option = {
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: hour
        },
        yAxis: {
            boundaryGap: [0, '50%'],
            type: 'value',
            max: 100
        },
        series: [
            {
                name: 'redis',
                type: 'line',
                smooth: true,
                symbol: 'none',
                stack: 'a',
                areaStyle: {
                    normal: {}
                },
                data: data
            }
        ]
    };

    setInterval(function () {
        addData(true);
        myChart.setOption({
            xAxis: {
                data: hour
            },
            series: [{
                name: 'redis',
                data: data
            }]
        });
    }, 1800);

    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
}
redisMonitorFunc(THEME);


// ------------------ runStatus  ------------------
function runStatus(THEME) {
    $.ajax({
        url: '/AppSimulator/drawDomainSearchCategoryAPI/',
        type: 'get',
        contentType: "application/json; charset=UTF-8",
        error: function (xhr, err) {
            ajaxError(err, '运行状态');
        },
        success: function (data, textStatus) {
            var myChart = echarts.init(document.getElementById("runStatus"), THEME);
            var option = {
                tooltip: {
                    trigger: 'item',
                    formatter: "{a} <br/>{b}: {c} ({d}%)"
                },
                legend: {
                    orient: 'vertical',
                    x: 'left',
                    data: ['启用', '停用']
                },
                series: [
                    {
                        name: '运行状态',
                        type: 'pie',
                        radius: ['50%', '90%'],
                        avoidLabelOverlap: false,
                        label: {
                            normal: {
                                show: false,
                                position: 'center'
                            },
                            emphasis: {
                                show: true,
                                textStyle: {
                                    fontSize: '30',
                                    fontWeight: 'bold'
                                }
                            }
                        },
                        labelLine: {
                            normal: {
                                show: false
                            }
                        },
                        data: [
                            {value: data['manual_added'], name: '启用'},
                            {value: data['cross_domain_link'], name: '停用'},
                        ]
                    }
                ]
            };
            myChart.setOption(option);
        }
    });
}
// runStatus(THEME);





