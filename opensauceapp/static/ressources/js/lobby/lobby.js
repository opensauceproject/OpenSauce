let lobby_socket;

let id;
let hasJoined = false;
let state = null;
let datetime;

let STATES = {
	WAITING_FOR_PLAYERS: 0,
	GAME_START_SOON: 1,
	QUESTION: 2,
	ANSWER: 3,
	GAME_END: 4,
}

let game_message = document.getElementById("game_message");

//Misc
let copy_to_clipboard_url_input = document.getElementById("copy_to_clipboard_url_input");
let copy_to_clipboard_url_button = document.getElementById("copy_to_clipboard_url_button");

//Tables
let players_table_container = document.getElementById("players_table_container");
let players_table = document.getElementById("players_table");
let spectators_table_container = document.getElementById("spectators_table_container");
let spectators_table = document.getElementById("spectators_table");
let history_table_container = document.getElementById("history_table_container");
let history_table = document.getElementById("history_table");

// Game
let current_question = document.getElementById("current_question");
let question_text = document.getElementById("question_text");
let question_image = document.getElementById("question_image");
let category = document.getElementById("category");
let category_container = document.getElementById("category_container");
let date_time = document.getElementById("date_time");
let date_time_container = document.getElementById("date_time_container");
let submit_answer = document.getElementById("submit_answer");

// Login
let when_connected = document.getElementById("when_connected");
let current_pseudo = document.getElementById("current_pseudo");
let leave_button = document.getElementById("leave_button");


let when_disconnected = document.getElementById("when_disconnected");
let pseudo_field = document.getElementById("pseudo_field");
let join_button = document.getElementById("join_button");

leave_button.addEventListener("click", leave);
copy_to_clipboard_url_button.addEventListener("click", copy_to_clipboard_url);

// Join
join_button.addEventListener("click", join);
pseudo_field.addEventListener("keydown", function(e) {
	if (e.keyCode === 13) join();
});

pseudo_field.focus();

try_to_connect();
init_players_table();
init_spectators_table();
init_history_table();
update_login_controls(false);

// To copy the URL to the clipboard
copy_to_clipboard_url_input.value = window.location.href;
function copy_to_clipboard_url() {
	let dummy = document.createElement('input');
	document.body.appendChild(dummy);
	dummy.value = window.location.href;
	dummy.select();
	document.execCommand('copy');
	document.body.removeChild(dummy);
}

window.setInterval(update_date_time, 99);

lobby_socket.addEventListener("message", function(e) {
	let message = JSON.parse(e.data);
	console.log(message);

	let data = message.data;
	datetime = new Date(data.datetime * 1000);

	switch (message.type) {
		// informal state
		case "welcome":
			id = data;
			break;
		case "scoreboard":
			update_players_table(data.players);
			update_spectators_table(data.spectators);
			update_history_table(data.history);
			break;
		case "settings":
			update_settings(data.settings);
			break;
			// game states
		case "waiting_for_players":
			state = STATES.WAITING_FOR_PLAYERS;
			update_waiting_for_players(data.qte);
			break;
		case "game_starts_soon":
			state = STATES.GAME_START_SOON;
			update_game_starts_soon();
			break;
		case "question":
			state = STATES.QUESTION;
            update_question(data.question, data.media_type, data.category);
			break;
		case "answer":
			state = STATES.ANSWER;
            update_question(data.question, data.media_type, data.category);
			update_answer(data.answer);
			break;
		case "game_end":
			state = STATES.GAME_END;
			update_game_end(data.winner);
			break;
	}
});

lobby_socket.addEventListener("close", function(e) {
	game_message.hidden = false;
	date_time_container.hidden = true;
	game_message.innerHTML = "Connetion to the lobby lost, please refresh your page";
	game_message.classList.add("text-danger");
});

submit_answer.addEventListener("keydown", function(e) {
	let message = e.srcElement.value;
	if (e.keyCode === 13 && message.length > 0) {
		send_answer(message);
		e.srcElement.value = "";
	}
});

function try_to_connect() {
	lobby_socket = new WebSocket("ws://" + window.location.host + "/lobby/" + lobby_name + "/");
}

function send_answer(answer) {
	lobby_socket.send(JSON.stringify({
		"type": "submit",
		"answer": answer,
	}));
}

function join() {
	hasJoined = true;
	let pseudo_join = pseudo_field.value;
	lobby_socket.send(JSON.stringify({
		"type": "join",
		"pseudo": pseudo_join
	}));
	current_pseudo.value = pseudo_join;
	submit_answer.focus();
	submit_answer.value = "";
	submit_answer.hidden = state != STATES.QUESTION;
}

function leave() {
	hasJoined = false;
	send_leave();
	update_login_controls(false);
}

function send_leave() {
	lobby_socket.send(JSON.stringify({
		"type": "leave"
	}));
}

function update_login_controls(isPlaying) {
	when_connected.hidden = !isPlaying;
	when_disconnected.hidden = isPlaying;
	submit_answer.hidden = !isPlaying;
	if (!isPlaying) {
		pseudo_field.focus();
		pseudo_field.select();
	}
}

function update_date_time() {
	let t = datetime - Date.now();
	//format

	let tsec = parseInt(t / 1000) + 1;
	if (tsec) {
		if (tsec >= 0) {
			date_time.innerHTML = tsec;
		} else {
			date_time.innerHTML = "Please wait...";
		}
	} else {
		date_time.innerHTML = "";
	}
}

// Update UI on messages
function update_question(question, media_type, category) {
	current_question.hidden = false;
	game_message.innerHTML = "";
	question_text.innerHTML = "";
	question_image.style = "";
	if (0 == media_type) {
		question_text.hidden = false;
		question_image.hidden = true;
		question_text.innerHTML = question;
	} else if (1 == media_type) {
		question_text.hidden = true;
		question_image.hidden = false;
		question_image.style = "background-image : url('" + question + "')";
	}
	category.innerHTML = category;

	date_time_container.hidden = false;
	game_message.hidden = true;
	category_container.hidden = false;
	submit_answer.hidden = !hasJoined;
	category_container.hidden = false;
	submit_answer.value = "";
	submit_answer.focus();
}

function update_answer(answer) {
	game_message.innerHTML = "The answer was : " + answer;
	current_question.hidden = false;
	game_message.hidden = false;
	submit_answer.hidden = true;
	category_container.hidden = true;
	date_time_container.hidden = true;
}

function update_waiting_for_players(qte) {
	game_message.innerHTML = "Waiting for " + qte + " players to join...";
	current_question.hidden = true;
	game_message.hidden = false;
	submit_answer.hidden = true;
	category_container.hidden = true;
	date_time_container.hidden = true;
}

function update_game_starts_soon(qte) {
	game_message.innerHTML = "The game is about to begin !";
	current_question.hidden = true;
	game_message.hidden = false;
	submit_answer.hidden = true;
	category_container.hidden = true;
	date_time_container.hidden = false;
}

function update_game_end(winner) {
	game_message.innerHTML = "The game has ended !" + "<br>Congratulations " + winner + " you are the winner !";
	current_question.hidden = true;
	game_message.hidden = false;
	submit_answer.hidden = true;
	category_container.hidden = true;
	date_time_container.hidden = true;
}

function init_players_table() {
	players_table.innerHTML = '';
	players_table.appendChild(Tools.create_row(["#", "Name", "Score", ""], "th"));
}

function init_spectators_table() {
	spectators_table.innerHTML = '';
	spectators_table.appendChild(Tools.create_row(["Name", ""], "th"));
}

function init_history_table() {
	history_table.innerHTML = '';
	// not the best practice be a bit boring to initalize properly
	history_table.appendChild(Tools.create_row(["Answer", "1<sup>st</sup> <span class=\"badge badge-light\">+5</span>", "2<sup>nd</sup> <span class=\"badge badge-light\">+3</span>", "3<sup>rd</sup> <span class=\"badge badge-light\">+2</span>", " "],
		"th"));
}

function update_players_table(p) {
	init_players_table();
	for (let i = 0; i < p.length; i++) {
		let row = p[i];
		let bonus = (row.points_this_round <= 0 ? "" : " + " + row.points_this_round);
		let classes = [];
		if (bonus != "")
			classes.push("bg-success");
		if (id == row["id"]) {
			classes.push("font-weight-bold");
			submit_answer.hidden = row.points_this_round > 0;
			update_login_controls(true);
		}

		players_table.appendChild(Tools.create_row([i + 1, row["name"], row.score + bonus, get_rights(row)], "td", classes));
	}
}

function update_spectators_table(s) {
	init_spectators_table();
	for (let i = 0; i < s.length; i++) {
		let row = s[i];
		let classes = [];
		if (id == row["id"]) {
			classes.push("font-weight-bold");
			update_login_controls(false);
		}
		spectators_table.appendChild(Tools.create_row([row["name"], get_rights(row)], "td", classes));
	}
}

function get_rights(player) {
	let rights = "";
	if (player.isOwner)
		rights += "isOwner";
	if (player.isAdmin)
		rights += "isAdmin";
	return rights;
}

function update_history_table(h) {
	init_history_table();
	for (let i = 0; i < h.length; i++) {
		let row = h[i];
		players = []
		for (let j = 0; j < 3; j++) {
			if (j < row["players"].length)
				players.push(row["players"][j]);
			else
				players.push("-");
		}
		let answer = document.createElement("span");
		answer.innerHTML = row["answer"];

		let link_report = document.createElement("span");
		link_report.classList.add("float-right");
		link_report.setAttribute("data-toggle", "modal");
		link_report.setAttribute("data-target", "#report_modal");
		link_report.classList.add("cursor-pointer");
		link_report.addEventListener("click", function() {
			load_modal_report(row["id"]);
		});

		let exclamation_mark = document.createElement("i");
		exclamation_mark.classList.add("fas");
		exclamation_mark.classList.add("fa-exclamation");

		let badge_danger = document.createElement("span");
		badge_danger.classList.add("badge");
		badge_danger.classList.add("badge-danger");

		badge_danger.appendChild(exclamation_mark);
		link_report.appendChild(badge_danger);

		history_table.appendChild(Tools.create_row([
			[answer, link_report], ...players
		]));
	}
}
