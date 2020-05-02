function recommendPlaces(city, state,offset) {
    var recommend_places_url = "https://fsq.internmate.tech/foursquare";
    var htmlContent = '<ul class="widget w-friend-pages-added notification-list friend-requests">{places_holder}</ul>';
    var places = [];
    $.ajax({
        url:recommend_places_url,
        dataType:'json',
        type:'post',
        contentType: 'application/json',
        data: JSON.stringify({"city":city,"state":state,"offset":offset}),
        processData:false,
        success: function(data, textStatus, jQxhr){
            dataParsed = JSON.parse(JSON.stringify(data))
            $.each(dataParsed, function(i, item) {
                var parse = JSON.parse(JSON.stringify(item));
                placesString = `<li class="inline-items"><div class="author-thumb">'
                <img src="${parse.icon}32${parse.fileType}" width=36, height=36, alt="author">
                </div><div class="notification-event">
                <a href="https://www.google.com/maps/place/${parse.address}" class="h6 notification-friend">${parse.name}</a><span class="chat-message-item">${parse.categoryname}</span>
                </div></li>
                `
                places.push(placesString);
            });
            $('#places_recommendations').html(htmlContent.replace('{places_holder}',places.join("")));
        }
    });
};
