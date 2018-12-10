/* 
The following helper functions facilitate chat with B.E.N.

@sendAjax manages communication between the client and the Django view. 
It accepts user input (i.e., the response to a survey question - the value of "result")
and sends the input to the Index view via a POST request. 

If the Index view return data (i.e., a message from B.E.N.), 
then @sendAjax does the following:
(1) adds this message to the chat
(2) adds options for answers (or a "goodbye" message) and 
sets the value "result" (a global varible used to track user input)
(3) auto-scrolls to the bottom of the chat window
*/

var result;

function sendAjax(botui, input) {
    $.ajax({
        type: "POST",
        url: "/",
        data : { user_input: input },

        success : function(data) {                
            botui.message.add({
                html: true,
                cssClass: 'bot-msg',
                delay: 1500,
                loading: true,
                content: prettyBENMsg(data.text)
            }).then(function () {
                if (data.answers.length != 0) {
                    botui.action.button({
                      action: data.answers
                    }).then(function (res) {
                        result = res.value;
                    });
                } else {
                    botui.message.add({
                        html: true,
                        cssClass: 'bot-msg',
                        delay: 1500,
                        loading: true,
                        content: prettyBENMsg('{% get_settings_value "DECISIONTREE_SESSION_END_MESSAGE" %}')
                    });
                }
            }).then(function () {
                getMessages();
            });
        },
        error: function() {
            return "Internal Server Error";
        }
    });
}

function prettyBENMsg(content) {
    return '<div class="row"><div class="col ben-sidebar"><img src="static/images/ben-icon-03.svg"></div><div class="col"><small><strong>B.E.N.</strong> <em>Bravely Engineered Navigator</em></small></br><div class="mt-2">' + content + '</div></div></div>';
}

function getMessages() {
    var div = $(".scroll");
    var card = $(".card-body");
    div.scrollTop(card.prop('scrollHeight'));
}
