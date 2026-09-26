const API_URL = "http://127.0.0.1:8000";

const todoListElement = document.getElementById("todo-list");
const titleInput = document.getElementById("todo-title");
const descriptionInput = document.getElementById("todo-description");
const addTodoButton = document.getElementById("add-todo-button");


// ----------------------------------
// Get and display todos
// ----------------------------------

function loadTodos() {
    fetch(`${API_URL}/todos`)
        .then((response) => response.json())
        .then((todos) => {

            todoListElement.innerHTML = "";

            todos.forEach((todo) => {
                displayTodo(todo);
            });

        })
        .catch((error) => {
            console.error("Error loading todos:", error);
        });
}


// ----------------------------------
// Display one todo
// ----------------------------------

function displayTodo(todo) {

    const taskElement = document.createElement("div");
    taskElement.classList.add("todo-item");

    if (todo.completed) {
        taskElement.classList.add("completed");
    }


    const checkbox = document.createElement("input");

    checkbox.type = "checkbox";
    checkbox.checked = todo.completed;

    checkbox.addEventListener("change", function () {
        updateTodo(todo.id, checkbox.checked);
    });


    const contentElement = document.createElement("div");


    const titleElement = document.createElement("h3");
    titleElement.textContent = todo.title;


    const descriptionElement = document.createElement("p");
    descriptionElement.textContent = todo.description;


    contentElement.appendChild(titleElement);
    contentElement.appendChild(descriptionElement);


    taskElement.appendChild(checkbox);
    taskElement.appendChild(contentElement);


    todoListElement.appendChild(taskElement);
}


// ----------------------------------
// Add a new todo
// ----------------------------------

function addTodo() {

    const title = titleInput.value.trim();
    const description = descriptionInput.value.trim();


    if (title === "" || description === "") {
        alert("Please enter both a title and description.");
        return;
    }


    fetch(`${API_URL}/todos`, {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            title: title,
            description: description
        })
    })
        .then((response) => response.json())
        .then((createdTodo) => {

            titleInput.value = "";
            descriptionInput.value = "";

            displayTodo(createdTodo);

        })
        .catch((error) => {
            console.error("Error creating todo:", error);
        });
}


// ----------------------------------
// Complete/uncomplete a todo
// ----------------------------------

function updateTodo(todoId, completed) {

    fetch(`${API_URL}/todos/${todoId}`, {
        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            completed: completed
        })
    })
        .then((response) => response.json())
        .then((updatedTodo) => {

            loadTodos();

        })
        .catch((error) => {
            console.error("Error updating todo:", error);
        });
}


// ----------------------------------
// Add button event
// ----------------------------------

addTodoButton.addEventListener("click", addTodo);


// ----------------------------------
// Load todos when page opens
// ----------------------------------

loadTodos();