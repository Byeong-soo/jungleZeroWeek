document.addEventListener("DOMContentLoaded", function () {

    let joinBtn = document.getElementById("joinBtn");

    let idType = /^[A-Za-z0-9+]{4,12}$/;

    joinBtn.addEventListener('click',function(){

        let idValue = document.getElementById("id").value;
        if(!idType.test(idValue)){
            alert("영문과 숫자만으로 4~12글자로 입력해주세요")
            return false;
        }

        let passType = /^[a-zA-Z0-9~!@#$%^&*(_+|<>?:{}]{6,16}$/;
        let passwordValue = document.getElementById("password").value;
        if(!passType.test(passwordValue)){
            alert("비밀번호는 6~12글자 사이로 작성해주세요.")
            return false;
        }

        let passwordCheckValue = document.getElementById("passwordCheck").value;

        if(passwordValue != passwordCheckValue){
            alert("비밀번호가 일치하지않습니다.")
            return false;
        }

        document.getElementById('joinForm').submit();
    })
   
});

