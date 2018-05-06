Vue.component('navigator', {
    props: {
        main_show: {type: Boolean, required: false, default: true},
        task_id: {type: Number, required: true},
        current_level: {type: Number, required: false, default: -1},
        levels: {type: Array, required: true, default: []},
        has_detail: {type: Boolean, required: true, default: false}
    },
    template: '<a v-show="main_show" v-on:click="navTo(\'main\',-1)" class="btn btn-xs btn-warning btn-nav" title="入口管理">' +
        '<i class="fa fa-sitemap"></i>' +
    '</a>' +
    '<a v-for="level in levels" v-on:click="navTo(\'hubs\',level)" title="[[ level+1 ]]级列表页"' +
    ' v-bind:class="[ current_level===level ? \'btn btn-xs btn-primary btn-nav nav-mark\' : \'btn btn-xs btn-primary btn-nav\']">' +
        '<i class="fa fa-list"></i>' +
    '</a>' +
    '<a v-show="has_detail" v-on:click="navTo(\'detail\',-1)" class="btn btn-xs btn-success btn-nav" title="详情页">' +
        '<i class="fa fa-file-text-o"></i>' +
    '</a>',
    methods: {
        navTo: function (action, level) {
            switch (action) {
                case "main":
                    window.location.href = "/webSpider/main/";
                    break;
                case "hubs":
                    window.location.href = "/webSpider/hubs/?taskId=" + this.task_id + "&level=" + level;
                    break;
                case "detail":
                    window.location.href = "/webSpider/detail/?taskId=" + this.task_id;
                    break;
                default:
                    break;
            }
        }
    }
});

Vue.component('paginator', {
    props: ['current', 'total', 'goto'],
    template:
    '<div class="box-footer with-border style="border-color: #1b6d85;height:62px">' +
        '<ul class="pagination pagination-bg" style="margin-top:5px">' +
            '<li v-bind:class="current != 1 ? \'active\' : \'disabled\'">' +
                '<a v-on:click="gotoPage(\'first\')"> 首页</a>' +
            '</li>' +
            '<li v-bind:class="1 < current ? \'active\' : \'disabled\'">' +
                '<a v-on:click="gotoPage(\'prev\')"> 上一页</a>' +
            '</li>' +
            '<li class="disabled">' +
                '<span>第 [[ current ]] 页</span><span> 共 [[ total ]] 页</span>' +
            '</li>' +
            '<li v-bind:class="current < total ? \'active\' : \'disabled\'">' +
                '<a v-on:click="gotoPage(\'next\')"> 下一页</a>' +
            '</li>' +
            '<li v-bind:class="current != total ? \'active\' : \'disabled\'">' +
                '<a v-on:click="gotoPage(\'last\')"> 末页</a>' +
            '</li>' +
            '<li>' +
            '<div class="col-md-1">' +
                '<div class="form-group">' +
                    '<div class="input-group">' +
                        '<input v-model="goto" type="text" placeholder="  跳转页" value="[[goto]]" style="height:30px;width:60px">' +
                        '<div class="input-group-addon">' +
                            '<a v-on:click="gotoPage(\'goto\')">' +
                                '<i class="glyphicon glyphicon-play"></i>' +
                            '</a>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
            '</div>' +
            '</li>' +
        '</ul>' +
    '</div>',
    methods: {
        gotoPage: function (action) {
            console.log("action ", action, typeof(action));
            switch (action) {
                case "first":
                    this.current = 1;
                    break;
                case "last":
                    this.current = this.total;
                    break;
                case "next":
                    if (this.current < this.total) {
                        this.current++;
                    }
                    break;
                case "prev":
                    if (this.current > 1) {
                        this.current--;
                    }
                    break;
                default: // "goto"
                    this.current = this.goto;
            }
            this.goto = this.current;
        }
    }
});

