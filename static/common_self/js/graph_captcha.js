/**
 * Created by renhuijun on 2017/9/23.
 */

'use strict';

$(function () {
    $('#btn_style').click(function(event){
        event.preventDefault();
        var captcha_img=$('#captcha_img');
        var old_src=captcha_img.attr('src');
        var new_src=xtparam.setParam(old_src,'xxx',Math.random())
        captcha_img.attr('src',new_src);
    })
});
