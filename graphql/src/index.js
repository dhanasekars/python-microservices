import { createServer } from 'http'
import { createSchema, createYoga } from 'graphql-yoga'


const schema = createSchema({
    typeDefs: /* GraphQL */ `
      type Query {
        id: Int!
        name: String!
        description: String!
        doneStatus: Boolean!
      }
    `,
    resolvers: {
      Query: {
        id: () => '1234',
        name: () => 'Get things done.',
        description: () => 'A GraphQL API for a todo list.',
        doneStatus: () => true
      }
    }
  })

const yoga = createYoga({
    schema
  })
   

const server = new createServer(yoga)

server.listen(4000, () =>{
    console.info('🚀🚀 The server is up! Running on http://localhost:4000/graphql')
})