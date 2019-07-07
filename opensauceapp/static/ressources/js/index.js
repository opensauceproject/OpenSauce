let lobbies_list = document.getElementById("lobbies_list");
let no_lobbies = document.getElementById("no_lobbies");
let create_lobby_button = document.getElementById("create_lobby_button");
let input_lobby_name = document.getElementById("input_lobby_name");
let socket = new WebSocket(lobby_socket_url);

input_lobby_name.addEventListener("input", handle_create_lobby_button);
input_lobby_name.addEventListener("keydown", enter_pressed);

handle_create_lobby_button({
	srcElement: input_lobby_name
});

function handle_create_lobby_button(e) {
	if (e.srcElement.value.length > 0) {
		create_lobby_button.classList.remove('btn-outline-dark', 'disabled');
		create_lobby_button.classList.add('btn-dark');
	} else {
		create_lobby_button.classList.remove('btn-dark');
		create_lobby_button.classList.add('btn-outline-dark', 'disabled');
	}
	create_lobby_button.href = "lobby/" + e.srcElement.value;
}

function enter_pressed(e) {
	if (e.keyCode == 13) {
		window.location.href = create_lobby_button.href;
	}
}

socket.addEventListener("message", function(e) {
	let message = JSON.parse(e.data);
	update_lobbies_list(message.list);
});

function update_lobbies_list(lobbies) {
	lobbies_list.innerHTML = "";

	no_lobbies.hidden = lobbies.length > 0;

	for (let i = 0; i < lobbies.length; i++) {
		let lobby = lobbies[i];
		let lobby_link = document.createElement("a");
		lobby_link.href = "lobby/" + lobby["name"];
		lobby_link.type = "button";
		lobby_link.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-center");

		let right = document.createElement("span");

		let badgePassword = document.createElement("span");
		if (lobby["password"]) {
			badgePassword.classList.add("badge", "badge-danger", "badge-pill");
			badgePassword.innerHTML = '<i class="fas fa-lock"></i>';
		} else {
			badgePassword.classList.add("badge", "badge-success", "badge-pill");
			badgePassword.innerHTML = '<i class="fas fa-lock-open"></i>';
		}

		let badgesPlayers = document.createElement("span");
		badgesPlayers.classList.add("badge", "badge-dark", "badge-pill");
		badgesPlayers.innerHTML = lobby["players"] + ' <i class="fas fa-gamepad"></i>';

		let badgesSpectators = document.createElement("span");
		badgesSpectators.classList.add("badge", "badge-dark", "badge-pill");
		badgesSpectators.innerHTML = lobby["spectators"] + ' <i class="fas fa-eye"></i>';

		lobby_link.innerHTML = lobby["name"];

		right.appendChild(badgesPlayers);
		right.appendChild(badgesSpectators);
		right.appendChild(badgePassword);
		lobby_link.appendChild(right);
		lobbies_list.appendChild(lobby_link);
	}
}
