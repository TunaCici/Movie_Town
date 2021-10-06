function main_entry() {

    $("#signupForm").on("click", "#submitSignup", function (e) {
        var form = $("#signupForm").serializeArray();
        console.log(form)
        var name = form[0].value;
        var surname = form[1].value;
        var username = form[2].value;
        var mailAddress = form[3].value;
        var passwordOne = form[4].value;
        var passwordTwo = form[5].value;
        var accept = "off";

        try {
            accept = form[6].value;
        }
        catch(err) {
            accept = "off";
        }

        $.ajax({
            type: "POST",
            url: "/sign-up",
            data: {
                "name": name,
                "surname": surname,
                "username": username,
                "mailAddress": mailAddress,
                "passwordOne": passwordOne,
                "passwordTwo": passwordTwo,
                "accept": accept
            },
            success: function (response) {
                parsed_response = JSON.parse(response)
                if (parsed_response.result == "success") {
                    $("#infoTextSignup").text("you have successfully signed up. redirecting to home");
                    $("#infoTextSignup").effect("bounce");
                    window.location.href = "/"
                }

                else {
                    $("#infoTextSignup").text(parsed_response.result);
                    $("#infoTextSignup").effect("shake");
                }
            }
        });
    });
}

$(document).ready(main_entry);