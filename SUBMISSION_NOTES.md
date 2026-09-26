### 1. When a POST request is sent, is the item automatically stored in the database? Why or why not?

No. Sending a POST request only sends data to the backend. The backend must receive and validate the data and then execute an SQL `INSERT` query to store it in the database. The database transaction should also be committed using `connection.commit()` so that the change is permanently saved.

### 2. What must the backend do before the new todo becomes permanent?

The backend must execute an `INSERT` SQL statement with the new todo's data and then call `connection.commit()`. The commit saves the transaction to the SQLite database.

### 3. After creating a todo, how would you make it appear on the page?

After the POST request succeeds, the backend returns the newly-created todo. The JavaScript can then pass that todo to a function such as `displayTodo(createdTodo)` to create the necessary HTML elements and add them to the todo list. Another approach is to call `loadTodos()` again to retrieve and display the updated list.

### 4. How would you avoid displaying thousands of todo items at the same time?

I would use pagination or another form of limited retrieval. For example, the backend could return only a fixed number of todos at a time using SQL `LIMIT` and `OFFSET`, and the frontend could provide Next and Previous controls. This prevents the browser from loading and displaying thousands of records simultaneously.

### 5. What information should the frontend send when a todo is marked complete?

The frontend should send the todo's unique ID and the new completed value. For example, the request could be sent to `PUT /todos/5` with the JSON body:

```json
{
    "completed": true
}
```

The ID identifies which todo should be updated, while the completed value tells the backend the new state.

### 6. Why should SQL queries use parameters instead of placing user values directly inside the query string?

Parameterized queries separate SQL commands from user-supplied data. This helps protect the application against SQL injection and also allows values containing characters such as quotation marks to be handled correctly. For example, using `?` placeholders and supplying the values separately is safer than constructing an SQL statement by directly inserting user input into the query string.
