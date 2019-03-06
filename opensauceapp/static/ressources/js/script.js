$(document).ready(function(){
    $('#create_lobby_button').attr('disabled',true);
    $('#input_lobby_name').keyup(function(){
        if($(this).val().length !=0){
            $('#create_lobby_button').attr('disabled', false);
        }
        else
        {
            $('#create_lobby_button').attr('disabled', true);
        }
    })
});
