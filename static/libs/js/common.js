$(document).ready(function(){
	$('#extranav li').click(function() {
		console.log("nav clicked...");
	    $(this).addClass('active').siblings().removeClass('active');
	})
})
// $('#extranav li').click(function() {
// 	console.log("nav clicked...");
//     $(this).addClass('active').siblings().removeClass('active');
// })
function checkTime(i)     
{     
    if (i<10){  
        i="0" + i;  
    }     
      return i;  
}   
function ticktime(){
	var curdate = new Date();
	var curtime = curdate.getFullYear() + "-" + checkTime(curdate.getMonth() + 1) + "-" +
				  checkTime(curdate.getDate()) + " " + checkTime(curdate.getHours()) + ":" + curdate.getMinutes() +
				  ":" + checkTime(curdate.getSeconds());
	console.log(curdate, curtime);
	document.getElementById("currentdate").innerHTML = curtime;

}
$(document).ready(function(){
	ticktime();
	setInterval(function(){
		ticktime();
		}, 1000)
})