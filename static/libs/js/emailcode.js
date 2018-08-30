 var count = 60;//声明全局变量
 var codeboolean=false;
$(function(){
        $('#password').keyup(function () {
            var strongRegex = new RegExp("^(?=.{8,})(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[_]).*$", "g");
            var mediumRegex = new RegExp("^(?=.{7,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))).*$", "g");
            var enoughRegex = new RegExp("(?=.{6,}).*", "g");
            var weekRegex = /(^\d{6,}$)|(^[a-zA-Z]{6,}$)|(^[_]{6,}$)/;
            var re=/^(\w){6,20}$/;
            if (false == re.test($(this).val() )) {
                $('#level').removeClass('pw-weak');
                $('#level').removeClass('pw-medium');
                $('#level').removeClass('pw-strong');
                $('#level').addClass(' pw-defule');
            }
            else {
                if (strongRegex.test($(this).val())) {
                    $('#level').removeClass('pw-weak');
                    $('#level').removeClass('pw-medium');
                    $('#level').removeClass('pw-strong');
                    $('#level').addClass(' pw-strong');
                    //密码为八位及以上并且字母数字特殊字符三项都包括,强度最强
                }
                else if (mediumRegex.test($(this).val())) {
                    $('#level').removeClass('pw-weak');
                    $('#level').removeClass('pw-medium');
                    $('#level').removeClass('pw-strong');
                    $('#level').addClass(' pw-medium');
                    //密码为七位及以上并且字母、数字、特殊字符三项中有两项，强度是中等
                }
                else if (weekRegex.test($(this).val())) {
                    $('#level').removeClass('pw-weak');
                    $('#level').removeClass('pw-medium');
                    $('#level').removeClass('pw-strong');
                    $('#level').addClass('pw-weak');
                    //如果密码为6为及以下，就算字母、数字、特殊字符三项都包括，强度也是弱的
                }
             }
				return true;
			});
        creatCode();
        $("#login").click(function(){
            var logintime=new Date().format("yyyyMMddhhmmss")
            var starttime = $.cookie("registertime")
            var timegaps = timecha(logintime,starttime);
            if(timegaps>300){
                $("#yanzhema").css("color","red");
                $("#yanzhema").text("已过期")
                return
            }
            if(codeboolean && username_Boolean && nickname_Boolean && password_Boolean && repassword_Boolean && emaile_Boolean && phoneNum_Boolean && companyName_Boolean && filename_Boolean ){
                $("#myform").submit();
            }
         });
        $("#myform #username").blur(function(){
            $("#usernamecheck").show();
            $("#usernamespan").hide();
            var username=$(this).val();
            checkUsername(username);
        })
         $("#myform #username").focus(function(){
             var id=$(this).attr("id");
             foucsThing(id);
        })
        $("#myform #nickname").blur(function(){
            $("#nicknamecheck").show();
            $("#nicknamespan").hide();
            var nickname=$(this).val();
            checkNickname(nickname);
        })
        $("#myform #nickname").focus(function(){
            var id=$(this).attr("id");
             foucsThing(id);
        })
        $("#myform #password").blur(function(){
            $("#passwordcheck").show();
            $("#passwordspan").hide();
                checkPassword($(this).val())
         })
        $("#myform #password").focus(function(){
            var id=$(this).attr("id");
             foucsThing(id);
        })
        $("#myform #repassword").blur(function(){
            if($(this).val()!="") {
                if ($("#myform #password").val() == $(this).val()) {
                    $("#repasswordcheck").html("✔").css("color", "green");
                    repassword_Boolean = true;
                } else {
                    $("#repasswordcheck").html("两次输入不一致").css("color", "red");
//                    alert("Password is not the same!")
                    repassword_Boolean = false;
                }
            }
            if ($("#password").val()!="" && $(this).val()==""){
                $("#repasswordcheck").html("请再次输入密码").css("color", "red");
                    repassword_Boolean = false;
            }
         })
        $("#myform #phoneNum").blur(function(){
                $("#phoneNumcheck").show();
                $("#phoneNumspan").hide();
                checkPhoneNum($(this).val())
        })
         $("#myform #phoneNum").focus(function(){
            var id=$(this).attr("id");
             foucsThing(id);
        })
         $("#email").blur(function(){
              $("#emailcheck").show();
//              $("#emailspan").hide();
            checkEmail($(this).val());
         })
        $("#myform #email").focus(function(){
            var id=$(this).attr("id");
             foucsThing(id);
        })
        $("#companyName").blur(function(){
            if($(this).val()!=""){
                $("#companycheck").html("✔").css("color","green");
                companyName_Boolean=true;
            }else{
                $("#companycheck").html("公司名称不能为空").css("color","red");
                companyName_Boolean=false;
            };
        })
        $("#location").blur(function(){
            if($(this).val()!=""){
                $("#locationcheck").html("✔").css("color","green");
            }else{
                $("#locationcheck").html("");
            };
        })
        $("#inputRandom").blur(function(){
            $("#yanzhema").text("");
            var a=$(this).val();
            var b=$("#codes").val();
            if(a!="") {
                if (a != b) {
                    $("#yanzhema").css("color", "red");
                    $("#yanzhema").text("验证码错误");
                    codeboolean = false;
                } else {
                    $("#yanzhema").css("color", "green");
                    $("#yanzhema").text("✔");
                    codeboolean = true;
                }
            }else{
                codeboolean = false;
                $("#yanzhema").css("color", "red");
                $("#yanzhema").text("验证码不能为空");
            }
        })
         $("#myform #filename").change(function(){

             var filePath=$(this).val();
             var arr=filePath.split('\\');
             var fileName=arr[arr.length-1];
             $("#filenam").val(fileName);
             checkImg(filePath);
         })
         var starttime = $.cookie("registertime");//取上次点击按钮发送验证码的时间
         if(starttime){//判断是否在该浏览器点击过该按钮
            var curtime = new Date().format("yyyyMMddhhmmss");//得到当前时间
            var timegaps = timecha(curtime,starttime);//得到上次点击按钮和这次加载页面的时间差（秒）
            if(timegaps<60){
                count=60-timegaps;//改变count初始值
                buttclick();//调用按钮点击事件函数
            }
        }
    })
    function creatCode(){
        $.ajax({
            success: function (data) {
                $("#verify_code_img").attr("src", "data:image/gif;base64," + data.img);
                }
            })
    }
		//按钮点击事件
function buttclick(){
//        if(emaile_Boolean==true) {
            if (count == 60) {//只有计数等于60时才会调用ajax
                var email = $("#email").val();
                $.ajax({
                    url: '/sendEmail',
                    type: 'Post',//get
                    async: true,//false是否异步
                    data: {"email": email,"type":0},//json格式对象
                    timeout: 5000,//设置超时时间
                    dataType: 'json',//返回的数据格式类型json/xml/html/script/jsonp/text
                    success: function (data){

                        alert(data.msg);
                        $.cookie("registertime", new Date().format("yyyyMMddhhmmss"));
                        //把请求成功的时间设置为上次请求的时间
//                        $("#codes").val(data.code);
//                        console.log(textStatus);//在前端控制台打印请求的状态
                        console.log(data.msg);//在控制台打印当前的数据
                    }
//                    error: function (xhr, textStatus) {
////                        console.log(textStatus);//在前端控制台打印请求的状态
//                            alert(data.msg);
//                    },
//                    complete: function () {
//                        console.log('结束');
//                    }
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
//        }
//        else{
//            alert("邮箱格式不正确");
//        }
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