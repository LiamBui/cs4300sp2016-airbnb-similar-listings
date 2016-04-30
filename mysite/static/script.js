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
    var showChar = 210;  // How many characters are shown by default
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

function amenities(room_type, accommodates, bedrooms){
    if(room_type == 'Entire home/apt'){
        var room_type_icon = '/static/entirehome.png';
        var room_type_text = 'Entire Home/Apt';
    }
    else if(room_type == 'Private room'){
        var room_type_icon = '/static/private.png';
        var room_type_text = 'Private Room';
    }
    else{
        var room_type_icon = '/static/shared.png';
        var room_type_text = 'Shared Room';
    }
    var accom_icon = '/static/accommodates.png';
    var accom_text = 'Accomodates: ' + accommodates;
    var bedroom_icon = '/static/bedrooms.png';
    var bedroom_text = 'Bedrooms: ' + bedrooms;

    var html = '<div class = "quickinfo"><img src = "' + room_type_icon + '" class="icons"></img><p class="icon_labels">' + room_type_text + '</p></div><div class = "quickinfo"><img src = "' + accom_icon + '" class="icons"></img><p class="icon_labels">' + accom_text + '</p></div><div class = "quickinfo"><img src = "' + bedroom_icon + '" class="icons"></img><p class="icon_labels">' + bedroom_text + '</p></div>';
    //$('#listing_info').html(html);
    //console.log("poop");
    return html;
};













