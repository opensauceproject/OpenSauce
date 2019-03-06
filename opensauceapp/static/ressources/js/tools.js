class Tools {
	static create_row(values, type = "td", classes = []) {
		let tr = document.createElement("tr");
		for (let i = 0; i < classes.length; i++) {
			tr.classList.add(classes[i]);
		}
		for (let i = 0; i < values.length; i++) {
			let td = document.createElement(type);
			td.innerHTML = values[i];
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
}
