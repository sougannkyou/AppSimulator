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


    // 获取密码等元素所在表单
    var div_form = $('#change_password');

    // 获取两个密码输入框
    var new_password = $('#id_password1');
    var new_password_again = $('#id_password2');

    // 获取保存按钮
    var save_button = $('#change_password_save');

    // 获取提交按钮
    var submit_button = $('button[name="_submit"]');

    // 获取是否为管理员修改密码
    var change_admin = $('#change-user-admin');

    // 增加生成密码按钮
    if (change_admin.text().length > 0) {
        var password_create_button = create_element('span', new_password);
        password_create_button.text('生成密码');
        password_create_button.addClass('btn-primary btn-sm');
    } else {
        password_create_button = change_admin;
    }
    // 生成8位混合密码
    password_create_button.click(function (event) {
        event.preventDefault();
        event.stopPropagation();
        var password_value = password(8);
        // console.log(password_value);
        new_password.val(password_value);
        new_password_again.val(password_value);
        if(change_admin.text() == '#1'){
            var mes = '您设置的密码为：' + password_value + '请保存！';
            // alert(mes);
            $('#alert-modal-content').text(mes);
            $('#alert-message-window').modal();
        };
        password_test(new_password);

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
        password_strength.addClass(password_class);
        password_strength.text(text);
    }

    // 以下为验证密码强度
    function password_test(password_input) {
        var verystrongRegex = new RegExp("^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*\\W).*$", 'g');
        var strongRegex = new RegExp("^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$", 'g');
        var mediumRegex = new RegExp("^(?=.{6,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))).*$");
        var enoughRegex = new RegExp("(?=.{6,}).*");
        if (password_input.val().length > 0) {
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
                password_strength_test('error', '弱,必须为6位以上字母加数字');
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
            password_same.addClass('error');
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

    // 点击密码输入周围空白区域时，也可以进行验证
    div_form.click(function () {
        password_test(new_password);
        password_same_func()
    });


    // 提交时的验证
    var submitnum = 0;

    function submit_test(event) {
        var required_num = 1;
        $('.required').each(function () {
            if ($(this).val().length == 0) {
                required_num = 0
            }
        });
        // if (password_strength.attr('class') == 'error') {
        if ('create_element_class error' == password_strength.attr('class')) {
            event.preventDefault();
            alert('您设置的新密码有误，请注意密码必须6位以上字母加数字！')
        } else if (password_same.attr('class') == 'create_element_class error') {
            event.preventDefault();
            alert('您设置的密码不一致，请重新设置！')
        } else if (required_num == 0) {
            event.preventDefault();
            alert('必填项必须全部填写')
        } else {
            submitnum = 1
        }
    };


    save_button.click(function (event) {
        submitnum = 0;
        submit_test(event);
        if (submitnum == 1) {
            submit_button.click()
        }
    });
    if (submitnum == 0) {
        $(document).unload(function () {
            event.stopPropagation()
        })
    }
});