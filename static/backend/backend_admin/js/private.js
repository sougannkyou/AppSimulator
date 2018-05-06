/**
 * Created by Administrator on 2017/2/16.
 */
$(document).ready(function () {
    // 生成并添加网页元素
    function create_element(tag_name, element_location, text) {
        text = text ? text : '';
        var element = $(document.createElement(tag_name));
        element.addClass('create_element_class');
        element.text(text);
        element_location.after(element);
        return element
    }

    // 增加必填提示
    var required_text = $('<span style="color: red; font-family: 楷体;;font-size:large">*</span>');
    $('.required').before(required_text);

    // 正确时的class
    var success_class = 'create_element_class success fa fa-check';
    // 错误时的class
    var error_class = 'create_element_class error fa fa-close';

    // 获取用户名输入框
    var username = $('#id_username');
    // 生成用户名验证提示
    var username_test = create_element('span', username);

    // 如果是修改用户页面，获取用户名输入框
    var change_username = $('#change_username_id');

    // 以下为用户名验证
    // 用户名规则检验
    var right_name = new RegExp("^[\\w.@+-]+$");

    function username_verify() {
        if (username.val().length == 0) {
            username_test.attr('class', 'create_element_class error');
            username_test.text('用户名不能为空');
        } else if (false == right_name.test(username.val())) {
            username_test.attr('class', error_class);
            username_test.text('');
        } else {
            // username_test.attr('class', 'create_element_class success');
            duplicate_username()
        }
    };

    // 用户名是否重复ajax检验
    // var duplicate_user_text = create_element('span', username_test);

    function duplicate_username() {
        // ajax提示区域
        $.post({
            data: {'username_duplicate': username.val(), 'username': change_username.text()},
            // url: {% url 'backend_admin:duplicate_username'%},
            url: '/duplicate_username',
            success: function (data, statusText, xmlHttpRequest) {
                console.log(data);
                if (data == '1') {
                    username_test.attr('class', 'create_element_class error');
                    username_test.text('用户名已存在')
                } else if(data == '2'){
                    username_test.attr('class', success_class);
                    username_test.text('')
                }else {
                    username_test.attr('class', success_class);
                    username_test.text('');
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                username_test.attr('class', 'create_element_class error');
                username_test.text('获取用户名出现错误');
                console.log(textStatus)
            },
            dataType: 'text'
        });

    };

    username.keyup(function () {
        username_verify()
    });
    username.blur(function () {
        username_verify();
    });

    // 获取电子邮箱输入框
    var email = $('#id_email_required');
    // 生成邮箱验证提示
    var email_test = create_element('span', email);

    // 以下为邮箱验证
    var right_email = new RegExp(/\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}/);

    // 邮箱格式验证
    function email_verify_func() {
        if (email.val().length == 0) {
            email_test.attr('class', 'create_element_class error');
            email_test.text('邮箱不能为空');
        } else if (false == right_email.test(email.val())) {
            email_test.attr('class', error_class);
            email_test.text('');
        } else {
            duplicate_email()
        }
    };
    // 邮箱重复性验证
    // var duplicate_email_text = create_element('span', email_test);

    function duplicate_email() {
        // ajax提示区域
        $.post({
            data: {'email_duplicate': email.val(), 'username': change_username.text()},
            url: '/duplicate_email',
            success: function (data, statusText, xmlHttpRequest) {
                if (data == '1') {
                    email_test.attr('class', 'create_element_class error');
                    email_test.text('邮箱已存在')
                } else if(data == '2'){
                    email_test.attr('class', success_class);
                    email_test.text('')
                }else {
                    email_test.attr('class', success_class);
                    email_test.text('');
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                email_test.text('获取邮箱出现错误');
            },
            dataType: 'text'
        });
    }

    email.keyup(function () {
        email_verify_func();
    });
    email.blur(function () {
        email_verify_func();
    });

    // 获取姓名生成按输入框
    var nickname = $('#id_nickname');

    // 获取保存按钮
    var save_button = $('input[name="_save"]');


    // 姓名验证提示生成
    var nickname_test_span = create_element('span', nickname);
    // 姓名验证
    function nickname_test(nickname_input, nickname_test_text) {
        if (nickname_input.val().length == 0) {
            nickname_test_text.attr('class', 'error create_element_class');
            nickname_test_text.text('姓名不能为空')
        } else {
            nickname_test_text.attr('class', success_class);
            nickname_test_text.text('')
        }
    }

    nickname.keyup(function () {
        nickname_test(nickname, nickname_test_span)
    });
    nickname.blur(function () {
        nickname_test(nickname, nickname_test_span)
    });

    // 提交时的验证
    var submitnum = 0;

    function submit_test() {
        var required_num = 1;
        $('.required').each(function () {
            if ($(this).val().length == 0) {
                required_num = 0
            }
        });
        // if (password_strength.attr('class') == 'error') {
        if (username_test.attr('class').match('error')) {
            event.preventDefault();
            alert('用户名有误，请重新设置！')
        } else if (email_test.attr('class').match('error')) {
            event.preventDefault();
            alert('邮箱输入有误，请重新设置！')
        } else if (required_num == 0) {
            event.preventDefault();
            alert('必填项必须全部填写')
        } else {
            submitnum = 1
        }
    };

    $('#create_user_button').click(function () {
        submitnum = 0;
        submit_test();
        if (submitnum == 0) {
            $('#create_user_submit').trigger()
        }
    });
    if (submitnum == 0) {
        $(document).unload(function () {
            event.stopPropagation()
        })
    }
    save_button.trigger(function () {
        alert($('.required').val().length);
        submit_test()
    });

});