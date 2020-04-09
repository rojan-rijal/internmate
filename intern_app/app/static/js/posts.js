function createPost(){
	var post = $.trim($("#post-content").val());
	var token = $.trim($("#csrf_token_post").val());
	if(post != ""){
		$.post('../api/post/add', {post_body:post,csrf_token:token}).done(function(data){
			alert("Data Loaded" + JSON.stringify(data));
		});
	}
};

