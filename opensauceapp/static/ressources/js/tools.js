class Tools {
    static create_row(values, type = "td", classes = []) {
        let tr = document.createElement("tr");
        for (let i = 0; i < classes.length; i++) {
            tr.classList.add(classes[i]);
        }
        for (let i = 0; i < values.length; i++) {
            let td = document.createElement(type);
            let value = values[i];
            if (Array.isArray(value)) {
                for (let j = 0; j < value.length; j++)
                    td.appendChild(value[j]);
            } else {
                td.innerHTML = values[i];
            }
            tr.appendChild(td);
        }
        return tr;
    }

    static set_class_hidden(cls, bool) {
        let image_only = document.getElementsByClassName(cls);
        for (let i = 0; i < image_only.length; i++) {
            image_only[i].hidden = bool;
        }
    }

    static update_invalide_class(input, condition) {
        if (condition) {
            input.classList.add("is-invalid");
            input.classList.remove("is-valid");
        } else {
            input.classList.add("is-valid");
            input.classList.remove("is-invalid");
        }
        return condition;
    }

    static toggle_alert_timeout(name, t) {
        $(name).show();
        setTimeout(function() {
            $(name).hide();
        }, t);
    }
}