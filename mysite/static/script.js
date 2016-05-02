var isPrototype = true;

$(document).on('click', '.toggle-button', function() {
                $(this).toggleClass('toggle-button-selected'); 
                cur_loc = window.location.href;
                if(cur_loc == "https://similairbnb.herokuapp.com/pt/")
                    isPrototype = false;
                else
                    isPrototype = true;

                isPrototype = !isPrototype;
                if(isPrototype){
                    $('.version').text('Prototype')
                    window.location = "https://airbnb-similar-listings.herokuapp.com/pt/";
                }
                else{
                    $('.version').text('Final')
                    window.location = "https://similairbnb.herokuapp.com/pt/";
                }
                console.log(isPrototype)
 });