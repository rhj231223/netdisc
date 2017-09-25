/**
 * Created by renhuijun on 2017/9/25.
 */

'use strict';

$(function () {
    var delete_btn=$('.delete_btn');
    delete_btn.click(function(event){
        event.preventDefault();

        var self=$(this);
        var uuid=self.attr('data_id');
        var want_remove=$(this).attr('data_want_remove');


        rhjajax.post({
            url:'/cms/delete_file/',
            data:{
                uuid:uuid,
                want_remove:want_remove,
            },

            success:function(data){
                if(data['code']==200){
                    var msg='';
                    if(want_remove=='1'){
                        self.attr('data_want_remove','0');
                        self.removeClass('btn-danger');
                        self.addClass('btn-success');
                        self.text('取消删除');
                        msg='删除操作成功!'
                    }else{
                        self.attr('data_want_remove','1');
                        self.removeClass('btn-success');
                        self.addClass('btn-danger');
                        self.text('删除');
                        msg='取消删除操作成功!'
                    }
                    xtalert.alertSuccessToast(msg)

                }else{
                    xtalert.alertInfo(msg=data['message'])
                }
            }


        })

    })
});
