/**
 * Created by renhuijun on 2017/9/25.
 */

'use strict';

$(function () {
    var submit_btn=$('#submit_btn');
    submit_btn.click(function(event){
        event.preventDefault();

        // var uuid=$(this).attr('data_id');
        var name=$('input[name=name]').val();
        var permission_id=$('select[name=permission_id]').val();

        rhjajax.post({
            url:window.location.href,
            data:{
                name:name,
                permission_id:permission_id,
            },
            success:function(data){
                if(data['code']==200){
                    xtalert.alertSuccessToast('文件保存成功!')
                    setTimeout(function(){
                        window.location.reload()
                    },1200)
                }else{
                    xtalert.alertInfo(data['message'])
                }
            }
        })
    });
});
