const Query =  {
    todo(parent, args, { db }, info) {
      if (!args.search){
        console.log(args); // Add this line to see the arguments in the console
        // console.log(db.todos)
        return db.todos
      }

      return db.todos.filter((todo) => {
        return todo.title.toLowerCase().includes(args.search.toLowerCase())
      })
    }
  }

export { Query as default }