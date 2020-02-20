$(document).ready(function () {
    $("button").click(function () {
        let id = this.id;
        if(id.slice(-1)==='p'){
            $("#"+this.id).prop('disabled', true);
            $("#"+id.slice(0, -1)).removeClass("w3-dark-gray");
            $("#"+id.slice(0, -1)).removeClass("w3-red");
            $("#"+id.slice(0, -1)).addClass('w3-green');
            // $("#"+id.slice(0, -1)).addClass('w3-light-green');
            $("#"+id.slice(0, -1)+"a").prop('disabled', false);
        }else if(id.slice(-1)==='a'){
            $("#"+this.id).prop('disabled', true);
            $("#"+id.slice(0, -1)).removeClass("w3-dark-gray");
            $("#"+id.slice(0, -1)).removeClass("w3-green");
            $("#"+id.slice(0, -1)).addClass('w3-red');
            // $("#"+id.slice(0, -1)).addClass('w3-light-green');
            $("#"+id.slice(0, -1)+"p").prop('disabled', false);
        }else{
            return true;
        }
    });
});

function select_all(student_count) {
    // alert(student_count);
    for (i = 1; i<student_count+1; i++){
        $("#"+i.toString()+"p").click();
    }
}