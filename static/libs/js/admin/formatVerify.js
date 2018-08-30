var count = 60;//声明全局变量

$(function(){
    var starttime = $.cookie("registertime");//取上次点击按钮发送验证码的时间
         if(starttime){//判断是否在该浏览器点击过该按钮
            var curtime = new Date().format("yyyyMMddhhmmss");//得到当前时间
            var timegaps = timecha(curtime,starttime);//得到上次点击按钮和这次加载页面的时间差（秒）
            if(timegaps<60){
                count=60-timegaps;//改变count初始值
                buttclick();//调用按钮点击事件函数
            }
        }
    }
}
function buttclick(){
    var checkresult=0;
    if (count == 60 && checkresult==0) {//只有计数等于60时才会调用ajax
        var email = $("#email").val();
        $.ajax({
            url: '/sendEmail/stmp',
            type: 'Post',//get
            async: true,//false是否异步
            data: {"email": email,"type":0},//json格式对象
            timeout: 5000,//设置超时时间
            dataType: 'json',//返回的数据格式类型json/xml/html/script/jsonp/text
            success: function (data){
                alert(data.msg);
                $.cookie("registertime", new Date().format("yyyyMMddhhmmss"));
                //把请求成功的时间设置为上次请求的时间
//                $("#codes").val(data.code);
                console.log(data.msg);//在控制台打印当前的数据
            }
        });
    }
    var obj = $("#getcode");//设置按钮上面的字
    if (count == 0) {
        obj.attr("disabled", false);
        obj.html("获取验证码");
        count = 60;
        return;
    } else {
        obj.attr("disabled", true);
        obj.html("重新发送(" + count + "s" + ")");
        count--;
    }
    setTimeout(function () {
        buttclick()
    }, 1000)//每一秒钟调用自己一次
}

//计算出时间差的秒数
function timecha(objO,objT){
    var str1=objO.substr(0,10);
    var str2=objT.substr(0,10);
    if(str1!=str2){
        return 70;
    }else{
        var str3=objO.substr(10,2);
        var str4=objT.substr(10,2);
        var str5=objO.substr(12,2);
        var str6=objT.substr(12,2);
        var str7=parseInt(str3)*60+parseInt(str5);
        var str8=parseInt(str4)*60+parseInt(str6);
        return str7-str8;
    }
}
//提供一个得到当前系统时间的字符串
Date.prototype.format = function (fmt) { //author: meizz
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" +                o[k]).length)));
    return fmt;
}