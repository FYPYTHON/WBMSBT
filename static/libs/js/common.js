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