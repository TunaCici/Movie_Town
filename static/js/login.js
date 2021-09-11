function main_entry() {

    $("#loginForm").on("click", "#submitLogin", function (e) {
        var form = $("#loginForm").serializeArray();
        var username = form[0].value;
        var password = form[1].value;
        
        $.ajax({
            type: "POST",
            url: "/login",
            data: {
                "username": username,
                "passwordOne": password
            },
            success: function (response) {
                parsed_response = JSON.parse(response)
                if (parsed_response.result == "success") {
                    $("#infoTextLogin").text("you have successfully logged in. redirecting to home");
                    window.location.href = "/"
                    $("#infoTextLogin").effect("bounce");
                }

                else {
                    $("#infoTextLogin").text(parsed_response.result);
                    $("#infoTextLogin").effect("shake");
                }
            }
        });
    });
}

$(document).ready(main_entry);