function createReview(){
    var company_name = $.trim($("#company-name").val());
    var rating = $.trim($("#rating").val());
    var review_body = $.trim($("#review-body").val());
    var review_title = $.trim($("#review_title").val());
    var position = $.trim($("#position").val());
    var location = $.trim($("#location").val());
	var token = $.trim($("#csrf_token_post").val());
	if(post != ""){
		$.post('../api/reviews/add', {company_name:company_name, num_of_stars:rating, comment_body: review_body, comment_title: review_title, job_location: location, position_name: position, csrf_token:token}).done(function(data){
			alert("Data Loaded" + JSON.stringify(data));
		});
	}
};


function loadReviews(company_name){
	var url = '../api/reviews/'+company_name;
	var postHtml = '';
	var posts = []
	// There is def a better way to do the shit i did below. Do not kill me plz
	$.getJSON(url).done(function(data) {
		$.each(data['Review'], function(i, item){
            var post = JSON.parse(JSON.stringify(item));
			var divForPost = '<div class="ui-block"><article class="hentry post">';
			var divForPost = divForPost.concat('<div class="post__author author vcard inline-items"><img src="'+post.image_url+'", width=36, height=36 alt="author">');
			var divForPost = divForPost.concat('<div class="author-date"><a class="h6 post__author-name fn" href="#">'+post.user_name+'</a>');
			var divForPost = divForPost.concat('<div class="post__date"><time class="published" datetime="2020-03-24">2 Hours</time></div></div></div>');
            var divForPost = divForPost.concat('<p>'+post.review_body+'</p></article></div>');
            alert(divForPost);
			posts.push(divForPost);
		});
		$("#reviews").html(posts.join(""));
	});
}