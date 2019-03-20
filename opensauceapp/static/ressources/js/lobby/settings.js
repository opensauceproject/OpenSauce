let score_goal_select = document.getElementById("score_goal_select");
score_goal_select.addEventListener("change", send_settings);

let catergory_difficulty_checkbox = document.getElementsByClassName("catergory-difficulty-checkbox");
for(let i = 0; i < catergory_difficulty_checkbox.length; i++)
{
    let checkbox = catergory_difficulty_checkbox[i];
    checkbox.addEventListener("change", send_settings);
}

function update_settings(settings)
{
    // TODO Update settings according to the message
}

function send_settings()
{
    let settings = {};
    settings["score_goal_value"] = parseInt(score_goal_select.selectedOptions[0].value);
    
    console.log(settings);
    // lobby_socket.send(JSON.stringify({
    //     "type": "settings",
    //     "settings": settings,
    // }));
}