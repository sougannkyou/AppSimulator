// function password(length, special) {
//     var iteration = 0;
//     var password = "";
//     var randomNumber;
//     if (special == undefined) {
//         var special = false;
//     }
//     while (iteration < length) {
//         randomNumber = (Math.floor((Math.random() * 100)) % 94) + 33;
//         if (!special) {
//             if ((randomNumber >= 33) && (randomNumber <= 47)) {
//                 continue;
//             }
//             if ((randomNumber >= 58) && (randomNumber <= 64)) {
//                 continue;
//             }
//             if ((randomNumber >= 91) && (randomNumber <= 96)) {
//                 continue;
//             }
//             if ((randomNumber >= 123) && (randomNumber <= 126)) {
//                 continue;
//             }
//         }
//         iteration++;
//         password += String.fromCharCode(randomNumber);
//     }
//     return password;
// }


$(document).ready(function () {
    // 获取option值
    var permissions = $('#id_permissions');
    var display_array = ['内容类型', '会话', '权限', 'permission groups'];
    $('#add_id_permissions').remove();
    permissions.children().each(function () {
        var new_text = $(this).text().split('\|');
        if ($.inArray($.trim(new_text[1]), display_array) > -1) {
            $(this).remove();
        } else {
            $(this).text($.trim(new_text[2]));
        }
    });


    // // 移除‘保存并编辑’button
    // $('input[name="_continue"]').remove();
    //
    // // 生成并添加网页元素
    // function create_element(tag_name, element_location, text) {
    //     text = text ? text : '';
    //     var element = $(document.createElement(tag_name));
    //     element.addClass('create_element_class');
    //     element.text(text);
    //     element_location.after(element);
    //     return element
    // }
    //
    // // 增加必填提示
    // var required_text = create_element('span', $('.required'), '必填');
    //
    // // 获取两个密码输入框
    // var new_password = $('#id_password1');
    // var new_password_again = $('#id_password2');
    //
    // // 获取保存按钮，保存并增加另一个按钮
    // var add_another_button = $('input[name="_addanother"]');
    // var save_button = $('input[name="_save"]');
    //
    // // 增加必填提示
    // // var required_text = create_element('span', $('.required'));
    //
    // // 增加生成密码按钮
    // var password_create_button = create_element('button', new_password);
    // password_create_button.text('生成密码');
    // // 生成8位混合密码
    // var password_value = password(8);
    // password_create_button.click(function (e) {
    //     event.preventDefault();
    //     event.stopPropagation();
    //     new_password.val(password_value);
    //     new_password_again.val(password_value)
    // });
    //
    // // 以下为密码强度和一致性验证
    // // 增加密码强度验证提示区域
    // var password_strength = create_element('span', password_create_button);
    // password_strength.text('密码强度');
    //
    // // 增加密码强度验证提示区域
    // var password_same = create_element('span', new_password_again);
    // password_same.text('密码一致性');
    //
    // function password_strength_test(password_class, text) {
    //     password_strength.attr('class', 'create_element_class');
    //     password_strength.addClass(password_class);
    //     password_strength.text(text);
    // }
    //
    // // 以下为验证密码强度
    // function password_test(password_input) {
    //     var strongRegex = new RegExp("^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*\\W).*$");
    //     var mediumRegex = new RegExp("^(?=.{6,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))).*$");
    //     var enoughRegex = new RegExp("(?=.{6,}).*");
    //     if (false == enoughRegex.test(password_input.val())) {
    //         password_strength_test('error', '请确认您的密码长度在6到16位之间');
    //     }
    //     else if (mediumRegex.test(password_input.val())) {
    //         password_strength_test('common', '一般');
    //         //密码为七位及以上并且字母、数字、特殊字符三项中有两项，强度是中等
    //     }
    //     else if (strongRegex.test(password_input.val())) {
    //         password_strength_test('strong', '强');
    //         //密码为八位及以上并且字母数字特殊字符三项都包括,强度最强
    //     }
    //     else {
    //         password_strength_test('error', '弱');
    //         //如果密码为6位及以下，就算字母、数字、特殊字符三项都包括，强度也是弱的
    //     }
    //     return true;
    // };
    //
    // // 验证密码强度
    // new_password.keyup(function () {
    //     password_test(new_password)
    // });
    // new_password.blur(function () {
    //     password_test(new_password)
    // });
    //
    // // 以下为验证密码一致性
    //
    // function password_same_func() {
    //     if (new_password.val().length != 0 && new_password_again.val().length != 0 && new_password_again.val() != new_password.val()) {
    //         password_same.addClass('error');
    //         password_same.text('您输入的密码不一致')
    //     } else {
    //         password_same.attr('class', 'create_element_class');
    //         password_same.text('')
    //     }
    // };
    // new_password_again.keyup(function () {
    //     password_same_func()
    // });
    // new_password_again.blur(function () {
    //     password_same_func()
    // });
    //
    // // 点击密码输入周围空白区域时，也可以进行验证
    // $('fieldset[class="module aligned wide"]').click(function () {
    //     password_test(new_password);
    //     password_same_func()
    // });
    //
    // // 提交时的验证
    // function submit_test() {
    //     if (password_strength.attr('class') == 'error') {
    //         event.preventDefault();
    //         alert('您设置的新密码有误，请注意密码必须6位以上字母加数字！')
    //     } else if (password_same.attr('class') == 'error') {
    //         event.preventDefault();
    //         alert('您设置的密码不一致，请重新设置！')
    //     }
    // };
    //
    // save_button.click(function () {
    //     submit_test()
    // });
    // add_another_button.click(function () {
    //     submit_test()
    // })
});