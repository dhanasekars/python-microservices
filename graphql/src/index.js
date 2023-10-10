import { createServer } from 'http'
import { createYoga } from 'graphql-yoga'
import { schema } from './schema.js'

const yoga = createYoga({
    schema
  })
   
  

const server = new createServer(yoga)

server.listen(4000, () =>{
    console.info('🚀 The server is up! Running on http://localhost:4000/graphql')
})