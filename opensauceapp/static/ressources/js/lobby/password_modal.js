let modal_password_input = document.getElementById("modal_password_input");
let modal_join_button = document.getElementById("modal_join_button");

modal_password.addEventListener("keydown", function(e) {
	if (e.which == 13)
		login();

    modal_password_input.classList.remove("is-invalid");
});
modal_join_button.addEventListener("click", login);

$('#modal_password').on('shown.bs.modal', function(e) {
	modal_password_input.focus();
});


function login() {
    $('#modal_password').modal("hide");
}
