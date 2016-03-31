var relay = {};

$(init);

function init(){
    setInterval(relay.getRealtimeImg,2000);
}


relay.getRealtimeImg = function(){
    $.ajax({
        type : "get",
        url : "/relay/",
        async : false,
        success : function(data){
             console.log(data);
             $('#relayImg').attr('src',data);
        }
    });
}




