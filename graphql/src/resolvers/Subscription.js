const Subscription = {
    // Channel for individual todo items 

    todoitem:{
    subscribe(parent, { todoID }, { db, pubsub }, info) {
        const todo = db.todos.find((todo) => todo.id === todoID);
        if (!todo) {
            throw new Error('Todo not found');
        }
        // pubsub.subscribe(`todo ${todoID}`);
        return pubsub.subscribe(`todo ${todoID}`);
        }
}
};

export { Subscription as default };


