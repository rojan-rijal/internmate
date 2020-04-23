function rejectRequest(userId, token){
	$.post('../api/reject/friend', {friend_id:userId,csrf_token:token}).done(function(data){
		alert("Data Loaded" + JSON.stringify(data));
	});	
};

function addFriend(userId, token){
	$.post('../api/add/friend', {friend_id:userId,csrf_token:token}).done(function(data){
		alert("Data Loaded" + JSON.stringify(data));
	});	
};

function getFriendRecs(csrf_token){
    var friend_rec = "../api/recfriends";
    var htmlContent = '<ul class="widget w-friend-pages-added notification-list friend-requests">{addUser}</ul>';
    var friendRecommends = [];
    $.getJSON(friend_rec).done(function(data){
        $.each(data['recommend'], function(i, item) {
            var parse = JSON.parse(JSON.stringify(item));
            friendRecommends.push('<li class="inline-items"><div class="author-thumb"><img src="'+parse.user_pic+'" width=36, height=36 alt="author"></div><div class="notification-event"><a href="'+parse.user_id+'" class="h6 notification-friend">'+parse.name+'</a><div onclick="addFriend('+parse.user_id+',\''+csrf_token+'\')"><button>Add Friend</button></div></div></li>');
        });
        $('#friend-rec').html(htmlContent.replace('{addUser}',friendRecommends.join("")));
    });

};

function getFriendRequests(csrf_token){
    var friend_rec = "../api/friendrequests";
    var htmlContent = '<ul class="widget w-friend-pages-added notification-list friend-requests">{addUser}</ul>';
    var friendRecommends = [];
    $.getJSON(friend_rec).done(function(data){
        $.each(data['requests'], function(i, item) {
            var parse = JSON.parse(JSON.stringify(item));
            friendRecommends.push('<li class="inline-items"><div class="author-thumb"><img src="'+parse.user_pic+'" height=36, width=36, alt="author"></div><div class="notification-event"><a href="'+parse.user_id+'" class="h6 notification-friend">'+parse.name+'</a><a href="#" onclick="addFriend('+parse.user_id+',\''+csrf_token+'\')"><i class="fa fa-check"></i>   </a><a href="#" onclick="rejectRequest('+parse.user_id+',\''+csrf_token+'\')"><i class="fa fa-times"></i></a></div></li>');
        });
        $('#friend-reqs').html(htmlContent.replace('{addUser}',friendRecommends.join("")));
    });

};

function getFriends(user_id) {
    var friend_rec = "../api/friends/"+user_id;
    var htmlContent = '<ul class="widget w-faved-page js-zoom-gallery">{addUser}</ul>';
    var friends = [];
    $.getJSON(friend_rec).done(function(data){
        $.each(data['friends'], function(i, item) {
            var parse = JSON.parse(JSON.stringify(item));
            friends.push('<li><a href="'+parse.user_id+'"><img src="'+parse.user_pic+'" height=36, width=36, alt="'+parse.name+'"></li>');
        });
        $('#friends').html(htmlContent.replace('{addUser}',friends.join("")));
    });
};
