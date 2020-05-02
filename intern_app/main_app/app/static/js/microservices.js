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
                placesString = `<li class="inline-items"><div class="author-thumb">
                <img src="${parse.icon}32${parse.fileType}" style="background-color: rgb(0, 0, 0);" width=36, height=36, alt="author">
                </div><div class="notification-event">
                <a href="https://www.google.com/maps/place/${parse.address}" class="h6 notification-friend">${parse.name}</a><span class="chat-message-item">${parse.categoryName}</span>
                </div></li>
                `
                places.push(placesString);
            });
            $('#places_recommendations').html(htmlContent.replace('{places_holder}',places.join("")));
        }
    });
};

function airbnbs(city, state) {
    var airbnb_url = "https://ab.internmate.tech/airbnb";
    var airbnbs = [];
    $.ajax({
        url:airbnb_url,
        dataType:'json',
        type:'post',
        contentType: 'application/json',
        data: JSON.stringify({"city":city,"state":state}),
        processData:false,
        success: function(data, textStatus, jQxhr){
            dataParsed = JSON.parse(JSON.stringify(data))
            $.each(dataParsed, function(i, item) {
                var parse = JSON.parse(JSON.stringify(item));
                airbnbDatas = `
                <div class="col col-xl-4 col-lg-4 col-md-6 col-sm-6 col-12">
				<div class="shop-product-item">
					<div class="product-thumb">
						<img src="${parse.urls[0]}" alt="product">
					</div>
					<div class="product-content">
						<div class="block-title">
							<a href="#" class="product-category">COFFEE MUGS</a>
							<a href="https://airbnb.com/rooms/${parse.id}" class="h5 title">${parse.name}</a>
						</div>
						<div class="block-price">
							<div class="product-price">${parse.rate}</div>
				
							<a href="https://airbnb.com/${parse.id}" class="in-cart">
								<svg class="olymp-shopping-bag-icon"><use xlink:href="/static/svg-icons/sprites/icons.svg##olymp-shopping-bag-icon"></use></svg>
							</a>
						</div>
					</div>
				</div>
			    </div>
                `
                airbnbs.push(airbnbDatas);
            });
            $('#airbnbLists').html(airbnbs.join(""));
        }
    });
};