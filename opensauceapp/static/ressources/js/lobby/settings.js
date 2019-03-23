let current_settings;
let catergory_difficulty_checkbox = [];

let open_settings = document.getElementById("open_settings");
let score_goal_select = document.getElementById("score_goal_select");
let settings_save_button = document.getElementById("settings_save_button");
let settings_cancel_button = document.getElementById("settings_cancel_button");

settings_save_button.addEventListener("click", send_settings);
settings_cancel_button.addEventListener("click", function() {
    update_settings(current_settings);
});

for(let checkbox of document.getElementsByClassName("catergory-difficulty-checkbox"))
{
    catergory_difficulty_checkbox.push({
        checkbox: checkbox,
        category_id: parseInt(checkbox.dataset.category_id),
        difficulty: parseInt(checkbox.dataset.difficulty),
    });
}

function update_settings(settings)
{
    current_settings = settings;
    for(let i = 0; i < score_goal_select.options.length; i++)
    {
        let option = score_goal_select.options[i];
        if(parseInt(option.value) == settings["score_goal_value"])
            score_goal_select.selectedIndex = i;
    }
    for(let i = 0; i < catergory_difficulty_checkbox.length; i++)
    {
        catergory_difficulty_checkbox[i].checkbox.checked = settings["categories"][i].value;
    }
}

function send_settings()
{
    let settings = {};
    settings["score_goal_value"] = parseInt(score_goal_select.selectedOptions[0].value);
    settings["categories"] = [];
    for(let checkbox of catergory_difficulty_checkbox)
    {
        settings["categories"].push({
            category_id : checkbox.category_id,
            difficulty : checkbox.difficulty,
            value : checkbox.checkbox.checked
        });
    }
    lobby_socket.send(JSON.stringify({
        "type": "settings",
        "settings": settings,
    }));
}

function set_settings_disabled(b){
    score_goal_select.disabled = b;
    for(let cb of catergory_difficulty_checkbox)
    {
        cb.checkbox.disabled = b;
    }
    settings_save_button.hidden = b;
}
