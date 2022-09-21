document.addEventListener("DOMContentLoaded", function () {

    let modifyBtn = document.getElementById("modify_btn");
    let deleteBtn = document.getElementById("delete_btn");

    let idValue = document.getElementById("id_input").value
    let phoneNumberValue = document.getElementById("phoneNumber_input").value
    let roomNumberValue = document.getElementById("roomNumber_input").value

    modifyBtn.addEventListener("click", function () {

        let cookie = document.cookie
        let token = cookie.split('=')[1]

        $.ajax({
            type: "POST",
            url: "/modifyMember",
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", "Bearer " + token)
            },
            data: { "id": idValue, "phoneNumber": phoneNumberValue, "roomNumber": roomNumberValue },
            success: function (response) {
               alert("회원정보가 수정되었습니다.")
               location.replace("/reservation")
            }
        })

    })

    deleteBtn.addEventListener("click",function(){
      
        let cookie = document.cookie
        let token = cookie.split('=')[1]

        let deleteConfirm = confirm("정말 회원탈퇴 하시겠습니까????");

        if(deleteConfirm){
            $.ajax({
                type: "POST",
                url: "/deleteMember",
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("Authorization", "Bearer " + token)
                },
                data: { "id": idValue},
                success: function (response) {
                   alert("회원탈퇴가 완료되었습니다")

                   document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
                   location.replace("/")
                }
            })
        }
       

    })

});

