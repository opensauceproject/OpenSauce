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
$('#modal_password').on('hide.bs.modal', function(e) {
	console.log("a");
});

$('#modal_password').modal("show");

function login() {
	let data = new FormData();
	data.append('password', modal_password_input.value);
	data.append('csrfmiddlewaretoken', csrf_token);
	let options = {
		method: 'POST',
		body: data,
		credentials: 'same-origin',
	};
	fetch(url_password, options)
		.catch(function() {
			console.log("error");
		})
		.then(function(response) {
			return response.json();
		})
		.then(function(json) {
			console.log(json);
			if (!json.lobby_exist)
				window.location.replace("/");
			if (!json.need_password || json.password_ok)
                window.location.replace(url_lobby);
            else
                modal_password_input.classList.add("is-invalid");
		});

}
