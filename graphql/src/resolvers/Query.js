const Query =  {
    todo(parent, args, { db }, info) {
      if (!args.search){
        return db.todos
      }

      return db.todos.filter((todo) => {
        return todo.title.toLowerCase().includes(args.search.toLowerCase())
      })
    }
  }

export { Query as default }