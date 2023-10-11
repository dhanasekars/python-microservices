import { v4 as uuidv4 } from 'uuid';
import { saveJson } from '../helper.js';
const filepath = 'src/data.json';
const Mutation = {
    createTodo: (parent, args, { db }, info) => {
   
      // Determine doneStatus, if not provided, default to false
      const doneStatus = args.data.doneStatus !== undefined ? args.data.doneStatus : false;
      const todo = {
        id: uuidv4(),
        ...args.data, // babel spread operator to copy all properties from args
        doneStatus
      }
     db.todos.push(todo)
      saveJson(filepath, db.todos);
      return todo
    },
    deleteTodo: (parent, args, { db }, info) => {
      const todoIndex = db.todos.findIndex((todo) => todo.id === args.id)
      if (todoIndex === -1) {
        throw new Error('Todo not found')
      }
      const deletedTodos = db.todos.splice(todoIndex, 1)
      saveJson(filepath, db.todos);
      return deletedTodos[0]
    }
  }


export { Mutation as default }