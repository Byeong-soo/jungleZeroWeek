document.addEventListener("DOMContentLoaded", function () {

    history.pushState(null, null, "/reservation");

    window.onpopstate = function (event) {
        history.go(1);
    };


    let logoutBtn = document.getElementById("logout_btn");

    logoutBtn.addEventListener("click", function () {

        let cookie = document.cookie
        let token = cookie.split('=')[1]

        $.ajax({
            type: "GET",
            url: "/tokenBlock",
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", "Bearer " + token)
            },
            data: {},
            success: function (response) {
                document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
                alert("안녕히가세요")
                location.replace('/');
            }
        })
    })

    let firstW = document.getElementById("first_w");
    let secondW = document.getElementById("second_w");
    let thirdW = document.getElementById("third_w");

    let firstR = document.getElementById("first_r");
    let secondR = document.getElementById("second_r");
    let thirdR = document.getElementById("third_r");

    let firstX = document.getElementById("first_x");
    let secondX = document.getElementById("second_x");
    let thirdX = document.getElementById("third_x");

    let firstCheck = document.getElementById("first_check");
    let secondCheck = document.getElementById("second_check");
    let thirdCheck = document.getElementById("third_check");

    function deleteClass() {
        firstCheck.classList.remove('img-show')
        secondCheck.classList.remove('img-show')
        thirdCheck.classList.remove('img-show')

        firstCheck.className = 'img-hide'
        secondCheck.className = 'img-hide'
        thirdCheck.className = 'img-hide'
    }

    firstW.addEventListener('click', function () {
        firstR.checked = true;
        deleteClass()
        if(!firstR.disabled){
            firstCheck.className = 'img-show'
            firstCheck.classList.remove('img-hide')
        }
    })

    secondW.addEventListener('click', function () {
        secondR.checked = true;
        deleteClass()
        if(!secondR.disabled){
            secondCheck.className = 'img-show'
            secondCheck.classList.remove('img-hide')
        }
    })

    thirdW.addEventListener('click', function () {
        thirdR.checked = true;
        deleteClass()
        if(!thirdR.disabled){
            thirdCheck.className = 'img-show'
        thirdCheck.classList.remove('img-hide')
        }
    })


    let searchBtn = document.getElementById("search_reservation_btn");

    let doSearchCheck = false;
    let timePicker = document.getElementById("timePicker");
    timePicker.addEventListener('click',function(){
        firstR.checked = false;
        secondR.checked = false;
        thirdR.checked = false;
        doSearchCheck = false;
    })

    searchBtn.addEventListener('click', function () {

        let cookie = document.cookie
        let token = cookie.split('=')[1]

        let in_date = document.getElementById('datePicker').value
        let in_time = document.getElementById('timePicker').value

        if(in_time == "1"){
            alert("시간을 선택후 조회해주세요")
            return false
        }

        deleteClass()

        firstX.classList.remove('img-show')
        secondX.classList.remove('img-show')
        thirdX.classList.remove('img-show')

        firstX.className = 'img-hide'
        secondX.className = 'img-hide'
        thirdX.className = 'img-hide'

        firstR.disabled = false
        secondR.disabled = false
        thirdR.disabled = false

        doSearchCheck = true;
        $.ajax({
            type: "POST",
            url: "/getReservations",
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", "Bearer " + token)
            },
            data: { 'laundry_date': in_date, 'laundry_time': in_time },
            success: function (response) {
                for (let i = 0; i < 3; i++) {
                    if (firstR.value == response.reservation[i]) {
                        firstX.classList.remove('img-hide')
                        firstX.className = 'img-show'
                        firstR.disabled = true
                    } else if (secondR.value == response.reservation[i]) {
                        secondX.classList.remove('img-hide')
                        secondX.className = 'img-show'
                        secondR.disabled = true
                    } else if(thirdR.value == response.reservation[i]){
                        thirdX.classList.remove('img-hide')
                        thirdX.className = 'img-show'
                        thirdR.disabled = true
                    }
                }

            }
        })

    })

    let reservationBtn = document.getElementById("reservation_btn")
    

    reservationBtn.addEventListener("click",function(){
        if(!doSearchCheck){
            alert("조회후 잔여 세탁기를 확인해주세요")
            return false;
        }

        let washer;
        try {
            washer = document.querySelector('input[name="washer"]:checked').value;
        } catch (error) {
            washer = 0;
        }

        if(washer == 0){
            alert("예약된 세탁기가 없습니다")
            return false;
        }


        document.getElementById("reservationForm").submit();
    })




})

