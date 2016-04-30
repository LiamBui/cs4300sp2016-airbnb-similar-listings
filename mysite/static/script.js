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
    $(window).bind('scroll', loadOnScroll);
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
 
$(document).on("click", ".morelink", function(){
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

var counter = 0;

function amenities(listing){
    if(listing.room_type == 'Entire home/apt'){
        var room_type_icon = '/static/entirehome.png';
        var room_type_text = 'Entire Home/Apt';
    }
    else if(listing.room_type == 'Private room'){
        var room_type_icon = '/static/private.png';
        var room_type_text = 'Private Room';
    }
    else{
        var room_type_icon = '/static/shared.png';
        var room_type_text = 'Shared Room';
    }
    var accom_icon = '/static/accommodates.png';
    var accom_text = 'Accomodates: ' + listing.accommodates;
    var bedroom_icon = '/static/bedrooms.png';
    var bedroom_text = 'Bedrooms: ' + listing.bedrooms;

    var dynamic_element = document.createElement("span");
    var attribute = document.createAttribute("id");
    var dynamic_class = "unique_id" + counter;
    attribute.value = dynamic_class;
    counter += 1;
    var showChar = 210;
    var ellipsestext = "...";
    var moretext = "&nbsp;[...]";
    var lesstext = "&nbsp;<<";
    var html = '<div class = "listing-container"><div class ="listing-score">Similarity Score: ' + listing.sim_score + '</div><div class = "listing-info"><div class="listing-name"><a href="' + listing.listing_url + '" target="_blank">' + listing.name + '</a></div><br><div class = "quickinfo"><img src = "' + room_type_icon + '" class="icons"></img><p class="icon_labels">' + room_type_text + '</p></div><div class = "quickinfo"><img src = "' + accom_icon + '" class="icons"></img><p class="icon_labels">' + accom_text + '</p></div><div class = "quickinfo"><img src = "' + bedroom_icon + '" class="icons"></img><p class="icon_labels">' + bedroom_text + '</p></div><div class="quickinfo">' + listing.price + ' per Night</div></div><div class="listing-img-container"><img src="' + listing.thumbnail_url + '" /></div><div class="listing-text"><div class = "listing-description">Description: <br><span class="more">' + listing.description.substr(0, showChar) + '<span class="morecontent"><span>' + listing.description.substr(showChar, listing.description.length - showChar) + '</span><a href="" class="morelink">' + moretext + '</a></span></span></div><div class = "listing-summary">Summary: <br><span class="more">' + listing.summary.substr(0, showChar) + '<span class="morecontent"><span>' + listing.summary.substr(showChar, listing.summary.length - showChar) + '</span><a href="" class="morelink">' + moretext + '</a></span></span></div></div><br></div>';
    dynamic_element.innerHTML = html;
    $(dynamic_element).attr("style", ".morecontent {display: inline;} .morecontent span {display: none;} .morelink {display: inline-block; font-family: serif; font-size: 1em !important;} br {display: block !important}");
    return dynamic_element;
};

var pageNum = 1;
var hasNextPage = true;
var loadOnScroll = function() {
    if ($(window).scrollTop() > $(document).height() - ($(window).height()*1.5)){
        $(window).unbind();
        loadItems();
    }
};

var loadItems = function() {
    if (hasNextPage == false) {
        return false;
    }
    pageNum += 1;
    $.ajax({
        data: {page_number: pageNum},
        dataType: 'json',
        success: function(output) {
            hasNextPage = true;
            for (listing in output) {
                $(amenities(output[listing])).appendTo(".results-container");
            }
        },
        error: function(output) {
            hasNextPage = false;
        },
        complete: function(output, textStatus){
            setTimeout(loadItems, 2000);
            $(window).bind('scroll', loadOnScroll);
        }
    });
};


