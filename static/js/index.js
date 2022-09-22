document.addEventListener("DOMContentLoaded",function() {

    let loginBtn = document.getElementById("login_btn");
    
    loginBtn.addEventListener("click",function(){
        let id = document.getElementById("id_input").value
        let pw = document.getElementById("password_input").value

        $.ajax({
            type: "POST",
            url: "/login",
            data: {"id":id,"password":pw},
            success: function (response) {
                let getResult = response["result"]
                console.log(response);
                if (!getResult) {
                    alert(response["msg"])
                } else {
                    let token = response['token']
                    document.cookie = "token="+token
                    $.ajax({
                        type: "GET",
                        url: "/checkToken",
                        beforeSend: function(xhr){
                            xhr.setRequestHeader("Authorization","Bearer "+ token)
                        },
                        success: function (response) {
                          location.replace("/reservation")
                        }
                    })
                }

            }
        })
    })



})


