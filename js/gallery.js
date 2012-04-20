$(function() {
$(".scrollable").scrollable();

$(".items img").click(function() {
    if ($(this).hasClass("active")) { return; }

    var url = $(this).attr("src").replace("_s", "");
    var id = $(this).attr("id").split("_")[0];
    
    var wrap = $("#image_wrap_" + id).fadeTo("medium", 0.5);

    var img = new Image();

    img.onload = function() {
        wrap.fadeTo("fast", 1);
        wrap.find("img").attr("src", url);
    };

    img.src = url;

//    $(".items img").removeClass("active");
    $(this.parentNode.parentNode).find("img").removeClass("active");     
    $(this).addClass("active");
});

$(".items img").each(function() {
    if ($(this).attr("id").split("_")[1] == "1") $(this).click();
});
});
