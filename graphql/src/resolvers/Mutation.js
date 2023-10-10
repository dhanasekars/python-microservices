import { v4 as uuidv4 } from 'uuid';
import saveJson from '../utils/saveJson.js';

const Mutation ={
    createTodo: (parent, args, ctx, info) => {
   
      // Determine doneStatus, if not provided, default to false
      const doneStatus = args.data.doneStatus !== undefined ? args.data.doneStatus : false;
      const todo = {
        id: uuidv4(),
        ...args.data, // babel spread operator to copy all properties from args
        doneStatus
      }
      todos.push(todo)
      saveJson(filepath, todos);
      return todo
    },
    deleteTodo: (parent, args, ctx, info) => {
      const todoIndex = todos.findIndex((todo) => todo.id === args.id)
      if (todoIndex === -1) {
        throw new Error('Todo not found')
      }
      const deletedTodos = todos.splice(todoIndex, 1)
      saveJson(filepath, todos);
      return deletedTodos[0]
    }
  }


export { Mutation as default }