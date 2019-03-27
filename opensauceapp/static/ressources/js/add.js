const SAUCE_TYPE = {
    QUOTE: 0,
    IMAGE: 1
};

const DIFFICULTY = {
    NONE: 0,
    EASY: 1,
    MEDIUM: 2,
    HARD: 3
};

const MAX_SIZE = 1024 * 1024 * 2; // 2 MO

let image_menu = document.getElementById("image_menu");
let quote_menu = document.getElementById("quote_menu");

let input_categories = document.getElementById("input_categories");

let input_load_image = document.getElementById("input_load_image");
let input_image_path = document.getElementById("input_image_path");
let feedback_image_container = document.getElementById("feedback_image_container");
let feedback_image = document.getElementById("feedback_image");

let input_difficulty = document.getElementById("input_difficulty");
let input_difficulty_easy = document.getElementById("input_difficulty_easy");
let input_difficulty_medium = document.getElementById("input_difficulty_medium");
let input_difficulty_hard = document.getElementById("input_difficulty_hard");

let alert_success = document.getElementById("alert_success");
let alert_failure = document.getElementById("alert_failure");

let send_button = document.getElementById("send_button");

image_menu.addEventListener("click", show_image_tab);
quote_menu.addEventListener("click", show_quote_tab);

input_load_image.addEventListener("change", update_image);

input_difficulty_easy.addEventListener("click", set_difficulty_easy);
input_difficulty_medium.addEventListener("click", set_difficulty_medium);
input_difficulty_hard.addEventListener("click", set_difficulty_difficult);

send_button.addEventListener("click", send);

let sauce_type;
let sauce_image;
let sauce_quote;
let sauce_answer;
let sauce_difficulty;

if (window.location.hash == "#quote") {
    show_quote_tab();
} else {
    show_image_tab();
}
clear_difficulites();

function update_image(e) {
	//https://stackoverflow.com/questions/3814231/loading-an-image-to-a-img-from-input-file/16153675
	if (e.target.files.length > 0) {
		let selected_file = e.target.files[0];

		let isValid = selected_file.size < MAX_SIZE;

		Tools.update_invalide_class(input_load_image, !isValid);
        feedback_image_container.hidden = !isValid;
		if(isValid)
		{
			let reader = new FileReader();

			input_image_path.innerHTML = selected_file.name;

			reader.addEventListener("load", function(e) {
				feedback_image.src = e.target.result;
				sauce_image = e.target.result;
			});

			reader.readAsDataURL(selected_file);
		}
		else
		{
			feedback_image.src = "";
			sauce_image = undefined;
			return false;
		}

	}
}

function show_image_tab() {
    sauce_type = SAUCE_TYPE.IMAGE;
    Tools.set_class_hidden("image-only", false);
    Tools.set_class_hidden("quote-only", true);
    image_menu.classList.add("active");
    quote_menu.classList.remove("active");
}

function show_quote_tab() {
    sauce_type = SAUCE_TYPE.QUOTE;
    Tools.set_class_hidden("image-only", true);
    Tools.set_class_hidden("quote-only", false);
    image_menu.classList.remove("active");
    quote_menu.classList.add("active");
}

function clear_difficulites() {
    sauce_difficulty = DIFFICULTY.NONE;
    input_difficulty_easy.classList.remove("bg-success");
    input_difficulty_medium.classList.remove("bg-warning");
    input_difficulty_hard.classList.remove("bg-danger");
    input_difficulty_easy.classList.add("text-success");
    input_difficulty_medium.classList.add("text-warning");
    input_difficulty_hard.classList.add("text-danger");
}

function set_difficulty_easy() {
    clear_difficulites();
    sauce_difficulty = DIFFICULTY.EASY;
    input_difficulty_easy.classList.add("bg-success");
    input_difficulty_easy.classList.add("text-white");
    input_difficulty_easy.classList.remove("text-success");
}

function set_difficulty_medium() {
    clear_difficulites();
    sauce_difficulty = DIFFICULTY.MEDIUM;
    input_difficulty_medium.classList.add("bg-warning");
    input_difficulty_medium.classList.add("text-white");
    input_difficulty_medium.classList.remove("text-warning");
}

function set_difficulty_difficult() {
    clear_difficulites();
    sauce_difficulty = DIFFICULTY.HARD;
    input_difficulty_hard.classList.add("bg-danger");
    input_difficulty_hard.classList.add("text-white");
    input_difficulty_hard.classList.remove("text-danger");
}

function validate() {
    let isInvalid = false;

    isInvalid |= Tools.update_invalide_class(input_categories, input_categories.value == "");
    if (sauce_type == SAUCE_TYPE.IMAGE) {
        isInvalid |= Tools.update_invalide_class(input_load_image, sauce_image == "" || sauce_image == undefined);
    } else if (sauce_type == SAUCE_TYPE.QUOTE) {
        isInvalid |= Tools.update_invalide_class(input_quote, input_quote.value == "");
    }
    isInvalid |= Tools.update_invalide_class(input_answer, input_answer.value == "");
    isInvalid |= Tools.update_invalide_class(input_difficulty, sauce_difficulty == 0);
    return !isInvalid;
}

function post_data(url = ``, data = {}) {
    //https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
    // Default options are marked with *
    return fetch(url, {
            method: "POST", // *GET, POST, PUT, DELETE, etc.
            mode: "cors", // no-cors, cors, *same-origin
            cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
            credentials: "same-origin", // include, *same-origin, omit
            headers: {
                "Content-Type": "application/json",
                // "Content-Type": "application/x-www-form-urlencoded",
            },
            redirect: "follow", // manual, *follow, error
            referrer: "no-referrer", // no-referrer, *client
            body: JSON.stringify(data), // body data type must match "Content-Type" header
        })
        .then(response => response.json()); // parses response to JSON
}

function send(e) {
    if (validate()) {
        send_button.disabled = true;
        data = {};
        data["type"] = sauce_type;
        if (sauce_type == SAUCE_TYPE.IMAGE) {
            data["question"] = sauce_image;
        } else if (sauce_type == SAUCE_TYPE.QUOTE) {
            data["question"] = input_quote.value;
        }
        data["answer"] = input_answer.value;
        data["difficulty"] = sauce_difficulty;
        data["sauce_category"] = input_categories.options[input_categories.selectedIndex].value;
        post_data("/add/", data)
            .then(function() {
                send_button.disabled = false;
				Tools.toggle_class_timeout(alert_success, "show", 5000);
                reset_page();
            })
            .catch(function() {
				Tools.toggle_class_timeout(alert_failure, "show", 5000);
			});
    } else {
        e.preventDefault();
    }
}

function reset_page() {
    sauce_image = undefined;
    sauce_quote = undefined;
    sauce_answer = undefined;
    sauce_difficulty = undefined;

    input_categories.selectedIndex = 0;
    input_categories.classList.remove("is-valid");
    input_categories.classList.remove("is-invalid");

    input_image_path.innerHTML = "";
    input_load_image.classList.remove("is-valid");
    input_load_image.classList.remove("is-invalid");

    input_quote.value = "";
    input_quote.classList.remove("is-valid");
    input_quote.classList.remove("is-invalid");

    input_answer.value = "";
    input_answer.classList.remove("is-valid");
    input_answer.classList.remove("is-invalid");

    input_difficulty.classList.remove("is-valid");
    input_difficulty.classList.remove("is-invalid");

    clear_difficulites();
}