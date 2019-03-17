let lobbies_list = document.getElementById("lobbies_list");
let no_lobbies = document.getElementById("no_lobbies");
let create_lobby_button = document.getElementById("create_lobby_button");
let input_lobby_name = document.getElementById("input_lobby_name");

input_lobby_name.addEventListener("keydown", update_link_to_lobby);
input_lobby_name.addEventListener("keydown", handle_create_lobby_button);
input_lobby_name.addEventListener("keydown", handle_enter_key);

update_lobbies_list();
handle_create_lobby_button();

//autorefresh
setInterval(update_lobbies_list, 1000);

function handle_create_lobby_button() {
	if (input_lobby_name.value.length > 0) {
		create_lobby_button.disabled = false;
		create_lobby_button.classList.remove('btn-outline-dark', 'disabled');
		create_lobby_button.classList.add('btn-dark');
	} else {
		create_lobby_button.disabled = true;
		create_lobby_button.classList.remove('btn-dark');
		create_lobby_button.classList.add('btn-outline-dark', 'disabled');
	}
}

function handle_enter_key(e) {
	if (e.keyCode == 13) {
		window.location.href = create_lobby_button.href;
	}
}

function update_link_to_lobby(e) {
	create_lobby_button.href = "lobby/" + e.srcElement.value;
}

function update_lobbies_list() {
	fetch("lobbies_list")
		.then(function(response) {
			return response.json();
		})
		.then(function(json) {
			lobbies_list.innerHTML = "";
			if (json.list.length <= 0) {
				no_lobbies.hidden = false;
			} else {
				for (let i = 0; i < json.list.length; i++) {
					let lobby = json.list[i];
					let lobby_link = document.createElement("a");
					lobby_link.href = "lobby/" + lobby["name"];
					lobby_link.type = "button";
					lobby_link.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-center");

					let right = document.createElement("span");

					let badgesPlayers = document.createElement("span");
					badgesPlayers.classList.add("badge", "badge-dark", "badge-pill");
					badgesPlayers.innerHTML = lobby["players"] + " <i class=\"fas fa-gamepad\"></i>";

					let badgesSpectators = document.createElement("span");
					badgesSpectators.classList.add("badge", "badge-dark", "badge-pill");
					badgesSpectators.innerHTML = lobby["spectators"] + " <i class=\"fas fa-eye\"></i>";

					lobby_link.innerHTML = lobby["name"];

					right.appendChild(badgesPlayers);
					right.appendChild(badgesSpectators);
					lobby_link.appendChild(right);
					lobbies_list.appendChild(lobby_link);
				}
				no_lobbies.hidden = true;
			}
		});
}
