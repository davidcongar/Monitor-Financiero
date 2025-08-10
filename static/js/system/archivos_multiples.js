document.getElementById("add-archivo-btn").addEventListener("click", function () {
    // Get the container where the new form elements will be added
    const container = document.getElementById("form-archivos-container");

    // Create a new div for the new file input
    const newFormArchivo = document.createElement("div");
    newFormArchivo.className = "form-archivo flex items-center gap-2 mt-4";

    // Add a new file input
    const newInput = document.createElement("input");
    newInput.type = "file";
    newInput.name = "archivos[]"; // Use an array name to handle multiple files in Flask
    newInput.id = `file-upload-${Date.now()}`; // Unique ID for each file input
    newInput.className = "hidden";

    // Add a new label linked to the input
    const newLabel = document.createElement("label");
    newLabel.className = "btn flex items-center gap-2 bg-primary border border-primary rounded-md text-white transition-all duration-300 hover:bg-primary/[0.85] hover:border-primary/[0.85] cursor-pointer";
    newLabel.setAttribute("for", newInput.id); // Link the label to the input
    newLabel.innerHTML = "Seleccionar archivo";

    // Add a span to display the file name
    const fileNameSpan = document.createElement("span");
    fileNameSpan.className = "file-name text-gray-500 ml-2";
    fileNameSpan.textContent = "No se ha seleccionado ningún archivo";

    // Add a delete button with the SVG
    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "flex items-center justify-center text-red-500 hover:text-red-700 p-2 rounded-full hover:opacity-80 rotate-0 hover:rotate-180 transition-all duration-300";
    deleteButton.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="w-5 h-5">
            <path d="M12.0007 10.5865L16.9504 5.63672L18.3646 7.05093L13.4149 12.0007L18.3646 16.9504L16.9504 18.3646L12.0007 13.4149L7.05093 18.3646L5.63672 16.9504L10.5865 12.0007L5.63672 7.05093L7.05093 5.63672L12.0007 10.5865Z" fill="currentColor"></path>
        </svg>
    `;
    deleteButton.addEventListener("click", function () {
        // Remove the file input container
        container.removeChild(newFormArchivo);
    });

    // Update the span text with the selected file name
    newInput.addEventListener("change", function () {
        const fileName = this.files[0]?.name || "No se ha seleccionado ningún archivo";
        fileNameSpan.textContent = fileName;
    });

    // Append the input, label, span, and delete button to the new div
    newFormArchivo.appendChild(deleteButton);
    newFormArchivo.appendChild(newInput);
    newFormArchivo.appendChild(newLabel);
    newFormArchivo.appendChild(fileNameSpan);

    // Append the new div to the container
    container.appendChild(newFormArchivo);
});