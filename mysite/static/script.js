var isPrototype = true;

 $(document).on('click', '.toggle-button', function() {
                $(this).toggleClass('toggle-button-selected'); 
                isPrototype = !isPrototype;
                if(isPrototype){
                    $('.version').text('Prototype')
                }
                else{
                    $('.version').text('Final')
                }
                console.log(isPrototype)
 });

$(document).ready(function(){
    if(orig_room_type == 'Entire home/apt'){
        $('#roomtype_icon').attr("src", '/static/entirehome.png');
        $('#orig-roomtype').text('Entire Home/Apt');
    }
    else if(orig_room_type == 'Private room'){
        $('#roomtype_icon').attr("src", '/static/private.png');
        $('#orig-roomtype').text('Private Room');
    }
    else{
        $('#roomtype_icon').attr("src", '/static/shared.png');
        $('#orig-roomtype').text('Shared Room');
    }
    $('#accom_icon').attr("src", '/static/accommodates.png');
    $('#orig-accom').text('Accommodates: ' + orig_accomm);
    $('#bedroom_icon').attr("src", '/static/bedrooms.png');
    $('#orig-bed').text('Bedrooms: ' + orig_beds);

     // Configure/customize these variables.
    var showChar = 100;  // How many characters are shown by default
    var ellipsestext = "...";
    var moretext = "&nbsp;[...]";
    var lesstext = "&nbsp;<<";

    $('.more').each(function() {
        var content = $(this).html();
 
        if(content.length > showChar) {
 
            var c = content.substr(0, showChar);
            var h = content.substr(showChar, content.length - showChar);
 
            var html = c + '<span class="morecontent"><span>' + h + '</span><a href="" class="morelink">' + moretext + '</a></span>';
 
            $(this).html(html);
        }

    console.log(output[0].summary);

});
 
$(".morelink").click(function(){
        if($(this).hasClass("less")) {
            $(this).removeClass("less");
            $(this).html(moretext);
        } else {
            $(this).addClass("less");
            $(this).html(lesstext);
        }
        $(this).parent().prev().toggle();
        $(this).prev().toggle();
        return false;
    });
});