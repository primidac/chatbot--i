var obj = {
    question: "",
    answer: ""
}

var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function () {
    $messages.mCustomScrollbar();
    setTimeout(function () {
        fakeMessage();
    }, 100);
});

function updateScrollbar() {
    $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
        scrollInertia: 10,
        timeout: 0
    });
}

function setDate() {
    d = new Date();
    if (m != d.getMinutes()) {
        m = d.getMinutes();
        $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
    }
}

function insertMessage() {
    msg = $('.message-input').val();
    if ($.trim(msg) == '') {
        return false;
    }
    $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    $('.message-input').val(null);
    updateScrollbar();
    setTimeout(function () {
        // fakeMessage();
        realMessage(msg);
    }, 1000 + (Math.random() * 20) * 100);
}

$('.message-submit').click(function () {
    insertMessage();
});

$(window).on('keydown', function (e) {
    if (e.which == 13) {
        insertMessage();
        return false;
    }
})

var Fake = [
    'Hi there, I\'m Dele. What would you like to do today?',
];

function fakeMessage() {
    if ($('.message-input').val() != '') {
        return false;
    }
    $('<div class="message loading new"><figure class="avatar"><img src="img/bat.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
    updateScrollbar();

    setTimeout(function () {
        $('.message.loading').remove();
        $('<div class="message new"><figure class="avatar"><img src="img/bat.png" /></figure>' + Fake[i] + '</div>').appendTo($('.mCSB_container')).addClass('new');
        setDate();
        updateScrollbar();
        i++;
    }, 1000 + (Math.random() * 20) * 100);
}

function realMessage(inputMessage) {

    // var inputMessage = $(".message-input").val();
    // var inputMessage = document.getElementById("inputMsg").value;
    $('<div class="message loading new"><figure class="avatar"><img src="img/bat.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
    updateScrollbar();
    var responseMessage = messageRequest(inputMessage);
    console.log(responseMessage);
    setTimeout(function () {
        $('.message.loading').remove();
        $('<div class="message new"><figure class="avatar"><img src="img/bat.png" /></figure>' + responseMessage + '</div>').appendTo($('.mCSB_container')).addClass('new');
        setDate();
        updateScrollbar();
        i++;
    }, 5000 + (Math.random() * 20) * 100);

}

function messageRequest(msg) {

    var settings = {
        'cache': false,
        'dataType': "jsonp",
        "async": true,
        "crossDomain": true,
        "url": "127.0.0.1:5002/chat/"+ msg,
        "methods": "GET",
        "headers":{
            "accept": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
    };

    // var resp = {
    //     name: "yeah"
    // };

    // $.ajax(settings).done(function (res){
    //     console.log(res);
    //     resp.name = res;
    //     // return res;
    // });
    
    // setTimeout(function() {
    //     //Code here
    //     console.log(resp.name);
    //     return resp.name;
    // }, 3000);

    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", 'http://127.0.0.1:5002/chat/' + msg, false);
    // xhttp.open("GET", 'https://5000-dot-12902975-dot-devshell.appspot.com/chat/' + msg, false);    
    xhttp.send();
    return xhttp.responseText;

}