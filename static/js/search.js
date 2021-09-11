function delay(callback, ms) {
    var timer = 0;
    return function() {
      var context = this, args = arguments;
      clearTimeout(timer);
      timer = setTimeout(function () {
        callback.apply(context, args);
      }, ms || 0);
    };
  }

function main_entry() {
    $("#searchBox").keyup(delay(function (e) {
        $.ajax({
            type: "POST",
            url: "/process-search",
            data: {"search_str": $(this).val()},
            success: function (response) {
                parsed_response = JSON.parse(response)

                if (parsed_response.result == "success") {
                    $("#resultSheet").empty()
                    $("#resultSheet").show()
                    
                    if (parsed_response.result_size == 0) {
                        $("#resultSheet").append("<h2>we could not find anything :(</h2>")
                    }

                    for (let i = 0; i < parsed_response.result_size; i++) {
                        $("#resultSheet").append(parsed_response.data[i])
                    }
                }

                else if (parsed_response.result == "empty") {
                    $("#resultSheet").empty()
                    $("#resultSheet").hide()
                }
                
                else {
                    console.log("failed to search.")
                }
            }
        });
    }, 250));

    $("#resultSheet").on("click", "#addToList0", function (e) { 
        var title_id = $("#addToList0").data("title-id");
        $.ajax({
            type: "POST",
            url: "/process-watchlist",
            data: {
                "request": "add",
                "target": title_id
            },
            success: function (response) {
                parsed_response = JSON.parse(response);
                if (parsed_response.result == "success") {
                    console.log("added to watchlist")
                }
                
                else {
                    console.log("faile to add.")
                }
            }
        });
    });
    
    $("#resultSheet").on("click", "#addToList1", function (e) { 
        var title_id = $("#addToList1").data("title-id");
        $.ajax({
            type: "POST",
            url: "/process-watchlist",
            data: {
                "request": "add",
                "target": title_id
            },
            success: function (response) {
                parsed_response = JSON.parse(response);

                if (parsed_response.result == "success") {
                    console.log("added to watchlist")
                }
                
                else {
                    console.log("faile to add.")
                }
            }
        });
    });

    $("#resultSheet").on("click", "#addToList2", function (e) { 
        var title_id = $("#addToList2").data("title-id");
        $.ajax({
            type: "POST",
            url: "/process-watchlist",
            data: {
                "request": "add",
                "target": title_id
            },
            success: function (response) {
                parsed_response = JSON.parse(response);
                if (parsed_response.result == "success") {
                    console.log("added to watchlist")
                }
                
                else {
                    console.log("faile to add.")
                }
            }
        });
    });
    
}

$(document).ready(main_entry);
