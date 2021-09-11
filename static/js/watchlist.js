function main_entry() {

    $.ajax({
        // send a request for loading watchlist
        type: "POST",
        url: "/process-watchlist",
        data: {"request": "load"},
        success: function (response) {
            parsed_response = JSON.parse(response);
            if (parsed_response.result == "success") {
                i$("#watchlistSheet").append(parsed_response.data);
            }

            else if (parsed_response.result == "empty") {
                $("#watchlistSheet").append("<h3>your watchlist is empty</h3>");
            }

            else {
                console.log("failed to load watchlist panel.");
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
                    console.log("removed from watchlist")
                    location.replace(location.href)
                }
                
                else {
                    console.log("faile to remove.")
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
                    console.log("removed from watchlist")
                    location.replace(location.href)
                }
                
                else {
                    console.log("faile to remove.")
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
                    console.log("removed from watchlist")
                    location.replace(location.href)
                }
                
                else {
                    console.log("faile to remove.")
                }
            }
        });
    });
}

$(document).ready(main_entry);