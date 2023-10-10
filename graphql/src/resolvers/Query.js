const Query =  {
    todo(parent, args, ctx, info) {
      if (!args.search){
        return todos
      }

      return todos.filter((todo) => {
        return todo.title.toLowerCase().includes(args.search.toLowerCase())
      })
    }
  }


export { Query as default }