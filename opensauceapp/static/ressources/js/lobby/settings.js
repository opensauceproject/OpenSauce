let score_goal_select = document.getElementById("score_goal_select");
score_goal_select.addEventListener("change", send_settings);

let catergory_difficulty_checkbox = [];
for(let checkbox of document.getElementsByClassName("catergory-difficulty-checkbox"))
{
    catergory_difficulty_checkbox.push({
        checkbox: checkbox,
        category_id: parseInt(checkbox.dataset.category_id),
        difficulty: parseInt(checkbox.dataset.difficulty),
    });
    checkbox.addEventListener("change", send_settings);
}

function update_settings(settings)
{
    // TODO Update settings according to the message
    // score_goal_select. = settings["score_goal_value"];
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