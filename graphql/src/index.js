import { createServer } from 'http'
import { createSchema, createYoga } from 'graphql-yoga'

// Demo sample data

const Todo = [{
  id: '1',
  title: 'Learn GraphQL',
  description: 'The main concepts of GraphQL',
  doneStatus: true
},
{
  id: '2',
  title: 'Learn Yoga',
  description: 'The main concepts of Yoga',
  doneStatus: false
},
{
  id: '3',
  title: 'Learn Prisma',
  description: 'The main concepts of Prisma',
  doneStatus: false
}]



const schema = createSchema({
    typeDefs: /* GraphQL */ `
      type Query {
       todo: [Todo!]!
      }

      type Todo {
        id: ID!
        title: String!
        description: String
        doneStatus: Boolean!
      }
    `,
    resolvers: {
      Query: {
        todo: () => Todo
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