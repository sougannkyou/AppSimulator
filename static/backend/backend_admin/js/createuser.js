function password(length, special) {
    var iteration = 0;
    var password = "";
    var randomNumber;
    if (special == undefined) {
        var special = false;
    }
    while (iteration < length) {
        randomNumber = (Math.floor((Math.random() * 100)) % 94) + 33;
        if (!special) {
            if ((randomNumber >= 33) && (randomNumber <= 47)) {
                continue;
            }
            if ((randomNumber >= 58) && (randomNumber <= 64)) {
                continue;
            }
            if ((randomNumber >= 91) && (randomNumber <= 96)) {
                continue;
            }
            if ((randomNumber >= 123) && (randomNumber <= 126)) {
                continue;
            }
        }
        iteration++;
        password += String.fromCharCode(randomNumber);
    }
    return password;
}

$(document).ready(function () {
    // 移除‘保存并编辑’button

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


    // 获取两个密码输入框
    var new_password = $('#id_password1');
    var new_password_again = $('#id_password2');

    // 获取姓名生成按输入框
    var nickname = $('#id_nickname');

    // 获取保存按钮
    var save_button = $('input[name="_save"]');

    // 增加生成密码按钮
    var password_create_button = create_element('span', new_password);
    password_create_button.text('生成密码');
    password_create_button.addClass('btn-primary btn-sm');
    // 生成8位混合密码

    password_create_button.click(function (event) {
        console.log(email_test.attr('class'));
        console.log(typeof(email_test.attr('class')));
        var password_value = password(8);
        // console.log(password_value);
        event.preventDefault();
        event.stopPropagation();
        new_password.val(password_value);
        new_password_again.val(password_value)
    });

    // 以下为密码强度和一致性验证
    // 增加密码强度验证提示区域
    var password_strength = create_element('span', password_create_button);
    password_strength.text('');

    // 增加密码强度验证提示区域
    var password_same = create_element('span', new_password_again);
    password_same.text('');

    function password_strength_test(password_class, text) {
        password_strength.attr('class', 'create_element_class');
        password_strength.addClass('create_element_class');
        password_strength.addClass(password_class);
        password_strength.text(text);
    }

    // 以下为验证密码强度
    function password_test(password_input) {
        var verystrongRegex = new RegExp("^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*\\W).*$", 'g');
        var strongRegex = new RegExp("^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$", 'g');
        var mediumRegex = new RegExp("^(?=.{6,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))).*$");
        var enoughRegex = new RegExp("(?=.{6,}).*");
        if (password_input.val().length > 0){
            if (false == enoughRegex.test(password_input.val())) {
                password_strength_test('error', '请确认您的密码长度在6到16位之间');
            }
            else if (verystrongRegex.test(password_input.val())) {
                password_strength_test('success', '很强');
                //密码为八位及以上并且字母数字特殊字符三项都包括,强度最强
            } else if (strongRegex.test(password_input.val())) {
                password_strength_test('success', '强');
                //密码为八位及以上并且字母数字特殊字符三项都包括,强度最强
            }
            else if (mediumRegex.test(password_input.val())) {
                password_strength_test('common', '一般');
                //密码为七位及以上并且字母、数字、特殊字符三项中有两项，强度是中等
            }
            else {
                password_strength_test('error', '弱');
                //如果密码为6位及以下，就算字母、数字、特殊字符三项都包括，强度也是弱的
            }
            return true;
        }
    };

    // 验证密码强度
    new_password.keyup(function () {
        password_test(new_password)
    });
    new_password.blur(function () {
        password_test(new_password)
    });

    // 以下为验证密码一致性

    function password_same_func() {
        if (new_password.val().length != 0 && new_password_again.val().length != 0 && new_password_again.val() != new_password.val()) {
           password_same.attr('class', 'error create_element_class');
            password_same.text('您输入的密码不一致')
        } else if (new_password.val().length != 0 && new_password_again.val().length == 0) {
            password_same.attr('class', 'error create_element_class');
            password_same.text('请再次输入您的密码')
        } else {
            password_same.attr('class', 'create_element_class');
            password_same.text('')
        }
    };
    new_password_again.keyup(function () {
        password_same_func()
    });
    new_password_again.blur(function () {
        password_same_func()
    });

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

    // 点击密码输入周围空白区域时，也可以进行验证
    $('#create_user_form').click(function () {
        password_test(new_password);
        password_same_func()
    });

    // 权限选择
    $('input[name="permissions"]').click(function () {
        var permissions_checkboxes = $(this).closest('.box-permission').find('input[name="checkbox_permission"]');
        if ($(this).prop('checked') == true) {
            $(this).attr("checked", true);
            permissions_checkboxes.each(function () {
                $(this).prop("checked", "checked");
            })
        } else {
            $(this).attr("checked", false);
            permissions_checkboxes.each(function () {
                $(this).removeAttr('checked')
            })
        }
    });

    $('input[name="checkbox_permission"]').click(function () {
        var permissions_checkboxes = $(this).closest('.box-permission').find('input[name="checkbox_permission"]');
        var permission_span = $(this).closest('.box-permission').find('input[name="permissions"]');
        if ($(this).prop('checked') == true && permission_span.prop('checked') == false) {
            permission_span.prop("checked", "checked");
        } else {
            var checked_num = 0;
            permissions_checkboxes.each(function () {
                if ($(this).prop('checked') == true) {
                    checked_num = 1
                }
            });
            if (checked_num == 0) {
                permission_span.removeAttr('checked')
            }
        }
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
        if (password_strength.attr('class').match('error')) {
            event.preventDefault();
            alert('您设置的新密码有误，请注意密码必须6位以上字母加数字！')
        } else if (password_same.attr('class').match('error')) {
            event.preventDefault();
            alert('您设置的密码不一致，请重新设置！')
        } else if (username_test.attr('class').match('error')) {
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

    // 角色权限hover之后出现具体权限
    $('.user-groups').hover(function () {
        $(this).children('.docBubble').removeClass('no-display');
    }, function () {
        $(this).children('.docBubble').addClass('no-display');
    });


});