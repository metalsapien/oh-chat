/* Javascript file to handle all the request/event operations made while chatting */

$(function() {
    /* Function gets called when the page loads the html */

    // Making the conncetion to the server
    var socket = io.connect("http://" + document.domain + ":" + location.port)

    // Resizing the input message field with text overflow.
    autosize(document.querySelectorAll('textarea'))

    // Event that triggers when a user conncets to the server.
    socket.on("connect", function() {
        name = $("#pickup").text()

        // Client sends the login username back to the server for processing.
        socket.emit("username", name)
    })

    // Event that recieves the current user session id and displays it.
    socket.on("id", function(id) {
        $("#sid").append('<span class="id">' + id + '</span>')
    })

    // Event to display all the online users by appeding it to the html list tag.
    socket.on("user_online", function(user) {

        // Broadcasts the message that saying the current user is online.
        $("#total_user").append('<li class="' + user['name'] + 
            '"><i class="fa fa-circle text-success"></i>&nbsp ' + 
            user['name'] + '</li>')

        // Broadcasts the message that saying the current user has joined the room.
        $("#chatbox").append('<br>'+ '<strong class="chat_name">' + user['name'] + 
            '</strong> <span class="text-success">joined the room</span>'
            + ' ' + ' <span class="time">' + user['time'] + '</span>');

        // Updating the document scroll height after receiving the message from the server.
        $("#chatbox").scrollTop($("#chatbox").prop('scrollHeight'));
    })

    // Displaying the total number of users online on the current users HTML page.
    socket.on("anony_user", function(anonymous) {
        for(user in anonymous) {
            $("#total_user").append('<li class="' + anonymous[user] + 
                '"><i class="fa fa-circle text-success"></i>&nbsp ' + anonymous[user] + '</li>')
        }
    })

    // Event to send the message from client to the server.
    $("#send_btn").click(function() {
        var msg = $("#text_input").val();
        socket.emit('message', msg);
        $("#text_input").val("");
    })

    // Event to recieve the message from the server to the client and displaying it.
    socket.on("from server", function(message) {
        $("#chatbox").append('<br>'+ '<strong class="chat_name">' + message['name'] + '</strong>'
                             + ' ' + ' <span class="time">' + message['time'] + 
                             '</span>' + '<br>' + message['msg']);
        
        $("#chatbox").scrollTop($("#chatbox").prop('scrollHeight'))
    })

    // Event to send private message to the server.
    $("#send_pm").click(function() {
        recipient = $("#recipient").val();
        message = $("#pmsg").val();
        socket.emit("private_message", { 'recipient' : recipient, 'message' : message });
        recipient = $("#recipient").val("");
        message = $("#pmsg").val("");
    })

    // Event to recieve the private message from the server to the client and displaying it personally.
    socket.on("sent_pm", function(message) {
        $("#chatbox").append('<br>'+ '<strong class="chat_name">' + message['name'] + '</strong>'
                             + ' ' + ' <span class="time">' + message['time'] + 
                             '</span>' + ' ' + '<strong class="text-danger">(Private)</strong>' + 
                             '<br>' + message['msg']);
        
        $("#chatbox").scrollTop($("#chatbox").prop('scrollHeight'))
    })

    // Event to disconnect the current user by sending the message to the server.
    $("#disconnect").click(function() {
        socket.emit('disconnect_me', "User Disconnected")
    })

    // Event to delete the current users info, html tag and broadcasting it that the current user has disconnceted. 
    socket.on("user_disconnect", function(username) {
        $("#chatbox").append('<br>'+ '<strong class="chat_name">' + username['name'] + 
                            '</strong> <span class="text-danger">left the room</span>'
                             + ' ' + ' <span class="time">' + username['time'] + '</span>');

        $("#chatbox").scrollTop($("#chatbox").prop('scrollHeight'))

        $("li").remove("." + username['name']);
    })

    // Event to refresh the page for redirecting the user to the login page after disconnection.
    socket.on("refresh", function(message) {
        document.location.reload(true);
    })
})
