const Subscription = {
todoUpdates:{
    subscribe: (parent, { todoID }, { db, pubsub }, info) => {
      console.log(pubsub)
      const todo = db.todos.find(todo => todo.id === todoID)
      if (!todo) {
        throw new Error(`No todo with id ${todoID}`)
      }
        return pubsub.asyncIterator(`todoUpdates ${todoID}`) 
    },
countdown:{
    subscribe: async function* (parent, { from }, { pubsub }, info) {
        for (let i = from; i >= 0; i--) {
          await new Promise(resolve => setTimeout(resolve, 1000))
          yield { countdown: i }
}
}
}

}
}

export { Subscription as default };