import { createServer } from 'http'
import { createSchema, createYoga } from 'graphql-yoga'


console.log("Hello World!")
// Type definitions (schema)
const typeDefs = `
    type Query {
        hello: String!
    }
`

// Resolvers

const resolvers = {
    Query: {
        hello() {
            return "This is my first query!"
        }
    }  
}

const yoga = createYoga({
    typeDefs,
    resolvers
  })
   

const server = new createServer(yoga)

server.listen(4000, () =>{
    console.info('🚀🚀 The server is up! Running on http://localhost:4000/graphql')
})