import fs from 'fs';

import { createServer } from 'http'
import { createYoga } from 'graphql-yoga'
import { createSchema } from 'graphql-yoga';
import  Query  from './resolvers/Query.js';
import Mutation from './resolvers/Mutation.js';
import db from './db.js';

const schemaFile = 'src/schema.graphql';
const typeDefs = fs.readFileSync(schemaFile, 'utf8');

const yoga = createYoga({
    schema: createSchema({
        typeDefs,
        resolvers: {
            Query,
            Mutation,
        }
    }),
    context: {
        db
    }
  })
  
const server = createServer(yoga)

server.listen(4000, () =>{
    console.info('🚀 The server is up! Running on http://localhost:4000/graphql')
})
