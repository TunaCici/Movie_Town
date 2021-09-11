function animate_in(id) {
    console.log(id)
}

function notify(message, type) {
    if (type == "success") {
        $("#success span").text(message);
        $("#success").show(250);
        setTimeout(hide_notify, 3000, [250]);
    }

    else if (type == "fail") {
        $("#fail span").text(message);
        $("#fail").show(250);
        setTimeout(hide_notify, 3000, [250]);
    }
}

function hide_notify(duration) {  
    $("#success").hide(duration);
    $("#fail").hide(duration);
}

function main_entry() {
    hide_notify(0);

    $.ajax({
        // send a request for loading watchlist
        type: "POST",
        url: "/process-watchlist",
        data: {"request": "load"},
        success: function (response) {
            parsed_response = JSON.parse(response);
            if (parsed_response.result == "success") {
                $("#watchlistSheet").append(parsed_response.data);
            }

            else if (parsed_response.result == "empty") {
                $("#watchlistSheet").append("<h3>your watchlist is empty</h3>");
            }
        }
    });

    $("#watchlistSheet").on("click", "#removeToList0", function (e) { 
        var title_id = $("#removeToList0").data("title-id");
        $.ajax({
            type: "POST",
            url: "/process-watchlist",
            data: {
                "request": "remove",
                "target": title_id
            },
            success: function (response) {
                parsed_response = JSON.parse(response);
                if (parsed_response.result == "success") {
                    notify("removed from watchlist.", "success");
                    location.replace(location.href);
                }
                
                else {
                    notify("failed to remove.", "fail");
                }
            }
        });
    });

    $("#watchlistSheet").on("click", "#removeToList1", function (e) { 
        var title_id = $("#removeToList1").data("title-id");
        $.ajax({
            type: "POST",
            url: "/process-watchlist",
            data: {
                "request": "remove",
                "target": title_id
            },
            success: function (response) {
                parsed_response = JSON.parse(response);
                if (parsed_response.result == "success") {
                    notify("removed from watchlist.", "success");
                    location.replace(location.href);
                }
                
                else {
                    notify("failed to remove.", "fail");
                }
            }
        });
    });

    $("#watchlistSheet").on("click", "#removeToList2", function (e) { 
        var title_id = $("#removeToList2").data("title-id");
        $.ajax({
            type: "POST",
            url: "/process-watchlist",
            data: {
                "request": "remove",
                "target": title_id
            },
            success: function (response) {
                parsed_response = JSON.parse(response);
                if (parsed_response.result == "success") {
                    notify("removed from watchlist.", "success");
                    location.replace(location.href);
                }
                
                else {
                    notify("failed to remove.", "fail");
                }
            }
        });
    });
}

$(document).ready(main_entry);