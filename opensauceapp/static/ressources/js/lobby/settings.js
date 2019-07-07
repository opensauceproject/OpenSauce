let current_settings;
let catergory_difficulty_checkbox = [];

let score_goal_select = document.getElementById("score_goal_select");
let settings_password_text = document.getElementById("settings_password_text");
let settings_save_button = document.getElementById("settings_save_button");
let settings_cancel_button = document.getElementById("settings_cancel_button");
let settings_max_players_number = document.getElementById("settings_max_players_number");
let settings_max_players_value = document.getElementById("settings_max_players_value");


update_settings_max_players_number();
settings_max_players_number.addEventListener("input", update_settings_max_players_number);

settings_save_button.addEventListener("click", send_settings);
settings_cancel_button.addEventListener("click", function() {
	update_settings(current_settings);
});

for (let checkbox of document.getElementsByClassName("catergory-difficulty-checkbox")) {
	catergory_difficulty_checkbox.push({
		checkbox: checkbox,
		category_id: parseInt(checkbox.dataset.category_id),
		difficulty: parseInt(checkbox.dataset.difficulty),
	});
}

function update_settings_max_players_number() {
	settings_max_players_value.innerHTML = settings_max_players_number.value;
}

function update_settings(settings) {
	current_settings = settings;
	settings_password_text.value = settings["password"];
	settings_max_players_number.value = settings["max_players"];
	update_settings_max_players_number();
	for (let i = 0; i < score_goal_select.options.length; i++) {
		let option = score_goal_select.options[i];
		if (parseInt(option.value) == settings["score_goal_value"])
			score_goal_select.selectedIndex = i;
	}
	for (let i = 0; i < catergory_difficulty_checkbox.length; i++) {
		catergory_difficulty_checkbox[i].checkbox.checked = settings["categories"][i].value;
	}
}

function send_settings() {
	let settings = {};
	settings["password"] = settings_password_text.value;
	settings["score_goal_value"] = parseInt(score_goal_select.selectedOptions[0].value);
	settings["categories"] = [];
	settings["max_players"] = settings_max_players_number.value;
	for (let checkbox of catergory_difficulty_checkbox) {
		settings["categories"].push({
			category_id: checkbox.category_id,
			difficulty: checkbox.difficulty,
			value: checkbox.checkbox.checked
		});
	}
	lobby_socket.send(JSON.stringify({
		"type": "settings",
		"settings": settings,
	}));
}

function set_settings_disabled(b) {
	settings_password_text.disabled = b;
	score_goal_select.disabled = b;
	for (let cb of catergory_difficulty_checkbox) {
		cb.checkbox.disabled = b;
	}
	settings_save_button.hidden = b;
}
