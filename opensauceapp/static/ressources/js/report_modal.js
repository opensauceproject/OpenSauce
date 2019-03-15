// Report
let report_form = document.getElementById("report_form");
let report_button = document.getElementById("report_button");

let report_question_image = document.getElementById("report_question_image");
let report_question_text = document.getElementById("report_question_text");
let report_answer = document.getElementById("report_answer");
let report_category = document.getElementById("report_category");

let current_report_sauce_id;

report_button.addEventListener("click", submit_report);

function submit_report() {
    let inputs = report_form.elements;
    let data = {};
    data["report_categories_ids"] = [];
    for (let i = 0; i < inputs.length; i++) {
        let input = inputs[i];
        if (input.type == "checkbox" && input.checked)
            data["report_categories_ids"].push(input.dataset.report_id);
        else if (input.type == "textarea")
            data["additional_informations"] = input.value;
    }
    data["sauce_id"] = current_report_sauce_id;

    fetch('/report_add/', {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
        },
        redirect: "follow",
        referrer: "no-referrer",
        body: JSON.stringify(data),
    });
}

function load_modal_report(id) {
    //ugly but we cant use jinja syntax with the id
    current_report_sauce_id = id;
    fetch("../../sauce_infos/" + id).then(function(response) {
            return response.json();
        })
        .then(function(sauce) {
            if (sauce.media_type == 0) {
                report_question_text.innerHTML = sauce.question;
                report_question_text.hidden = false;
                report_question_image.hidden = true;
            } else if (sauce.media_type == 1) {
                report_question_image.style = "background-image : url('sauce.question + "')";
                report_question_text.hidden = true;
                report_question_image.hidden = false;
            }
            report_answer.innerHTML = sauce.answer;
            report_category.innerHTML = sauce.sauce_category;
        });
}
