$(document).ready(function () {
    $("button").click(function () {
        let id = this.id;
        $("#"+this.id).prop('disabled', true);
        $("#"+id.slice(0, -1)).removeClass("w3-dark-gray");
        if(id.slice(-1)==='p'){
            $("#"+id.slice(0, -1)).removeClass("w3-red");
            $("#"+id.slice(0, -1)).addClass('w3-green');
            // $("#"+id.slice(0, -1)).addClass('w3-light-green');
            $("#"+id.slice(0, -1)+"a").prop('disabled', false);
        }else{
            $("#"+id.slice(0, -1)).removeClass("w3-green");
            $("#"+id.slice(0, -1)).addClass('w3-red');
            // $("#"+id.slice(0, -1)).addClass('w3-light-green');
            $("#"+id.slice(0, -1)+"p").prop('disabled', false);
        }
    });
});