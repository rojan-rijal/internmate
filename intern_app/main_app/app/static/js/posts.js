function createPost(){
	var post = $.trim($("#post-content").val());
	var token = $.trim($("#csrf_token_post").val());
	if(post != ""){
		$.post('../api/post/add', {post_body:post,csrf_token:token}).done(function(data){
			alert("Data Loaded" + JSON.stringify(data));
		});
	}
};


/*
function name: loadAllPosts
function description: This function will be called in the
newsfeed section.
function technical information: Sends either pp or nf on to the backend. pp means profile page, nf means newsfeed
function output:
1) Posts made by user and their friends
2) Number of likes and who liked the posts
3) Comment threads for the post
*/
function loadPosts(pageType){
	var url = '../api/post/load/'+pageType;
	var postHtml = '';
	var posts = []
	// There is def a better way to do the shit i did below. Do not kill me plz
	$.getJSON(url).done(function(data) {
		$.each(data['posts'], function(i, item){
			var post = JSON.parse(JSON.stringify(item));
			var divForPost = '<div class="ui-block"><article class="hentry post">';
			var divForPost = divForPost.concat('<div class="post__author author vcard inline-items"><img src="'+post.author_pic+'", width=36, height=36 alt="author">');
			var divForPost = divForPost.concat('<div class="author-date"><a class="h6 post__author-name fn" href="#">'+post.author_name+'</a>');
			var divForPost = divForPost.concat('<div class="post__date"><time class="published" datetime="2020-03-24">2 Hours</time></div></div></div>');
			var divForPost = divForPost.concat('<p>'+post.body+'</p></article></div>');
			posts.push(divForPost);
		});
		$("#posts").html(posts.join(""));
	});
}

/*
@@function name: likePost
@@parameter: post_id
@@function description: This function takes in a post_id
integer and then sends it to the api call to like the post.
*/
function likePosts(post_id){
	$.post('../api/post/like', {post_id:post_id,csrf_token:token}).done(function(data){
		alert("Data Loaded" + JSON.stringify(data));
	});
};

