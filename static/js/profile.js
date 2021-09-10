function main_entry() {

    $.ajax({
        // send a request for loading information panel
        type: "POST",
        url: "/profile-panel",
        data: {"request": "load_information"},
        success: function (response) {
            parsed_response = JSON.parse(response);
            if (parsed_response.result == "success") {
                $("#profilePanel").append(parsed_response.data);
            }

            else {
                console.log("failed to load information panel.");
            }
        }
    });

    $("#profilePanel").on("click", "#changePassword", function (e) {
        // clear profile panel
        $("#profilePanel").empty();

        // load change password panel
        $.ajax({
            type: "POST",
            url: "/profile-panel",
            data: {"request": "load_password"},
            success: function (response) {
                parsed_response = JSON.parse(response);
                if (parsed_response.result == "success") {
                    $("#profilePanel").append(parsed_response.data);
                }

                else {
                    console.log("failed to load password panel.");
                }
            }
        });
    });

    $("#profilePanel").on("click", "#applyPassword", function (e) {
        // send a request for changing the password
        $.ajax({
            type: "POST",
            url: "/password",
            data: {
                "request": "change",
                "currentPassword": $("#currentPassword").val(),
                "newPasswordOne": $("#newPasswordOne").val(),
                "newPasswordTwo": $("#newPasswordTwo").val()
            },
            success: function (response) {
                console.log()
                parsed_response = JSON.parse(response);
                if (parsed_response.result == "success") {
                    // TODO: Password changed
                    console.log("password changed successfully.");
                    window.location.href = "/logout";
                }

                else {
                    // TODO: Password failed to change
                    console.log("failed to change password.");
                }
            }
        });
    });

    $("#profilePanel").on("click", "#cancelPassword", function (e) {
        // clear profile panel
        $("#profilePanel").empty();

        // load change password panel
        $.ajax({
            type: "POST",
            url: "/profile-panel",
            data: {"request": "load_information"},
            success: function (response) {
                parsed_response = JSON.parse(response);
                if (parsed_response.result == "success") {
                    $("#profilePanel").append(parsed_response.data);
                }

                else {
                    console.log("failed to load information panel.");
                }
            }
        });
    });
}

$(document).ready(main_entry);