import { createServer } from 'http'
import { createSchema, createYoga } from 'graphql-yoga'
import { v4 as uuidv4 } from 'uuid';
import { loadJson, saveJson } from './helper.js';
// Demo sample data
const filepath = 'src/data.json';
const todos = loadJson(filepath);


const schema = createSchema({
    typeDefs: /* GraphQL */ `
      type Query {
       todo(search: String): [Todo!]!
      }
      type Mutation {
        createTodo(
          title: String!
          description: String
          doneStatus: Boolean
        ): Todo!
      }

      type Todo {
        id: ID!
        title: String!
        description: String
        doneStatus: Boolean
      }
    `,
    resolvers: {
      Query: {
        todo(parent, args, ctx, info) {
          if (!args.search){
            return todos
          }

          return todos.filter((todo) => {
            return todo.title.toLowerCase().includes(args.search.toLowerCase())
          })
        }
      },
      Mutation: {
        createTodo: (parent, args, ctx, info) => {
       
          // Determine doneStatus, if not provided, default to false
          const doneStatus = args.doneStatus !== undefined ? args.doneStatus : false;
          const todo = {
            id: uuidv4(),
            title: args.title,
            description: args.description,
            doneStatus: doneStatus
          }
          todos.push(todo)
          saveJson(filepath, todos);
          return todo
        }
      }
    }
  })

const yoga = createYoga({
    schema
  })
   
  

const server = new createServer(yoga)

server.listen(4000, () =>{
    console.info('🚀 The server is up! Running on http://localhost:4000/graphql')
})