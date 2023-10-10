import { createSchema } from 'graphql-yoga';
import { loadJson } from './helper.js';
// Demo sample data
const filepath = 'src/data.json';
const todos = loadJson(filepath);

export const schema = createSchema({
    typeDefs: /* GraphQL */ `
      type Query {
       todo(search: String): [Todo!]!
      }
      type Mutation {
        createTodo(data: CreateTodoInput): Todo!
        deleteTodo(id: ID!): Todo!
      }
      input CreateTodoInput {
        title: String!
        description: String
        doneStatus: Boolean
      }
      type Todo {
        id: ID!
        title: String!
        description: String
        doneStatus: Boolean
      }
    `,


    resolvers: {
      
    }
  })