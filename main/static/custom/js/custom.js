$(document).ready(function () {
    $("button").click(function () {
        let id = this.id;
        if(id.slice(-1)==='p'){
            $("#"+this.id).prop('disabled', true);
            $("#"+id.slice(0, -1)).removeClass("w3-dark-gray");
            $("#"+id.slice(0, -1)).removeClass("w3-red");
            $("#"+id.slice(0, -1)).addClass('w3-green');
            $("#"+id.slice(0, -1)+"a").prop('disabled', false);
        }else if(id.slice(-1)==='a'){
            $("#"+this.id).prop('disabled', true);
            $("#"+id.slice(0, -1)).removeClass("w3-dark-gray");
            $("#"+id.slice(0, -1)).removeClass("w3-green");
            $("#"+id.slice(0, -1)).addClass('w3-red');
            $("#"+id.slice(0, -1)+"p").prop('disabled', false);
        }else{
            return true;
        }
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function select_all(student_count) {
    // alert(student_count);
    for (let i = 1; i<student_count+1; i++){
        $("#"+i.toString()+"p").click();
    }
}

function submit(student_count) {
    let states = [];
    for ( let i = 1; i<student_count+1; i++){
        if ($("#"+i.toString()).hasClass("w3-green")){
            states.push(true);
        }
        else if($("#"+i.toString()).hasClass("w3-red")){
            states.push(false);
        }
        else{
            return false;
        }
    }
    $.ajax({
        type: "POST",
        data: {csrfmiddlewaretoken: getCookie('csrftoken'), states:states},
        url: "/attendance/",
        success: function(){
            $("#took-attendance").fadeIn();
            setTimeout(function () {
                $("#took-attendance").fadeOut();
            }, 5000)
        }
    });
}