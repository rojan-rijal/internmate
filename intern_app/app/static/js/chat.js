function getFriendsChats() {
    var friend_rec = "../api/friends/me";
    var chatSideBarHTML = '<ul class="notification-list chat-message" style="height: 500px; overflow: auto">{chat_friends}</ul>'
    var chats = [];
    $.getJSON(friend_rec).done(function(data){
        $.each(data['friends'], function(i, item) {
            var parse = JSON.parse(JSON.stringify(item));
            var chatHtml=`<li onclick=load_message('`+parse.conv_id+`')>
            <div class="author-thumb">
                <img src="`+parse.user_pic+`" width=36, height=36 alt="author">
            </div>
            <div class="notification-event">
                <a href="#" class="h6 notification-friend">`+parse.name+`</a>
            </div>
            </li>`;
            chats.push(chatHtml)
        }); 
        $('#recentmesasages').html(chatSideBarHTML.replace('{chat_friends}',chats.join("")));
    });
};

