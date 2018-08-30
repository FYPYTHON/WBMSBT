var username_Boolean = false;
var nickname_Boolean = false;
var password_Boolean = false;
var repassword_Boolean = false;
var varconfirm_Boolean = false;
var emaile_Boolean = false;
var phoneNum_Boolean = true;
var companyName_Boolean = false;
var filename_Boolean = false;
function checkPassword(str){
    if(str!=""){
         var re=/^(\w){6,20}$/;
         if(re.test(str)){
             $("#passwordcheck").html("✔").css("color","green");
            password_Boolean=true;
         }else{
            $("#passwordcheck").html("格式错误,密码必须为6~20位数字字母下划线的组合").css("color","red");
//            alert("Invalid format of password!");
            password_Boolean=false;
         }
    }else {
        $("#passwordcheck").html("密码不能为空").css("color","red");
//            alert("Password is empty!");
            password_Boolean=false;
    }
}
function checkUsername(str) {
    var username = str;
    var re = /^[a-zA-z]\w{4,15}$/;
    if (username != "") {
        if (re.test(username)) {
            $.ajax({
                type: "Post",
                url: "/admin/checkUserIsExist",
                dataType: "json",
                data: {"loginName": username},
                success: function (data) {
                    if (data.msg == "登录名已被注册") {
                        $("#usernamecheck").html("登录名已被注册").css("color", "red");
                        username_Boolean = false;
                    } else {
                        $("#usernamecheck").html("✔").css("color", "green");
                        username_Boolean = true;
                    }
                }
            })
        } else {
            $("#usernamecheck").html("请输入6-16位,字母、数字,以字母开头").css("color", "red");
            username_Boolean = false;
        }
    } else {
        $("#usernamecheck").html("登录名不能为空").css("color", "red");
        username_Boolean = false;
    }
}
function  checkNickname(str) {
    var nickname=str;
    var re =/^[\u4e00-\u9fa5·]{2,8}$/;
    if(nickname!=""){
        if(re.test(nickname)){
            $("#nicknamecheck").html("✔").css("color","green");
            nickname_Boolean=true;
        }else{
            $("#nicknamecheck").html("格式错误").css("color","red");
             nickname_Boolean=false;
        }
    }else{
        $("#nicknamecheck").html("姓名不能为空").css("color","red");
         nickname_Boolean=false;
    }
}
function checkPhoneNum(str){
    var re=/^1[3|4|5|7|8][0-9]{9}$/;
    if(str!=""){
         if(re.test(str)){
            $("#phoneNumcheck").html("✔").css("color","green");
            phoneNum_Boolean=true;
         }else{
           $("#phoneNumcheck").html("格式错误").css("color","red");
           phoneNum_Boolean=false;
        }
    }else{
        phoneNum_Boolean=true;
    }
}
function checkEmail(str){
    var re= /^[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+/ ;
     if(str!="") {
         if (re.test(str)) {
             $("#emailcheck").html("✔").css("color","green");
             emaile_Boolean=true;
         } else {
//             $("#emailcheck").html("格式错误").css("color","red");
             emaile_Boolean=false;
         }
     }else {
//         $("#emailcheck").html("邮箱不能为空").css("color","red");
         emaile_Boolean=false;
     }
}
function checkImg(str){
     var filename=str;
     if(filename!="") {
         var extStart = filename.lastIndexOf(".");
         var ext = filename.substring(extStart, filename.length).toUpperCase();
         if (ext != ".BMP" && ext != ".PNG" && ext != ".GIF" && ext != ".JPG" && ext != ".JPEG") {
             $("#filenamecheck").html("图片限于bmp,png,gif,jpeg,jpg格式").css("color", "red");
             filename_Boolean = false;
         }else {
              $("#filenamecheck").html("✔").css("color","green");
              filename_Boolean=true;
         }
     }else {
         $("#filenamecheck").html("文件不能为空").css("color","red");
            filename_Boolean=false;
     }
 }
 function foucsThing(str) {
     A=str+"check";
     B=str+"span";
     $("#"+A).hide();
     $("#"+B).show();
}
$("#login").click(function(){

    var span=eval(span1ss)+eval(sapns2)+eval(spans3)+eval(spans5)+eval(spans6)+eval(spans7);
    if(span==6 ){
        $("#myform").submit();
    }
 });

$("#myform input").blur(function(){
    var s=$(this).attr("id");
    alert(s);
})