import fs from 'fs';

import { createServer } from 'http'
import { createYoga, createSchema, createPubSub } from 'graphql-yoga'
import  Query  from './resolvers/Query.js';
import Mutation from './resolvers/Mutation.js';
import Subscription from './resolvers/Subscription.js';
import db from './db.js';

const pubsub = createPubSub();

const schemaFile = 'src/schema.graphql';
const typeDefs = fs.readFileSync(schemaFile, 'utf8');

const yoga = createYoga({
    schema: createSchema({
        typeDefs,
        resolvers: {
            Query,
            Mutation,
            Subscription
        }
    }),
    context: {
        db,
        pubsub
    }
  })
  
const server = createServer(yoga)

server.listen(4000, () =>{
    console.info('🚀 The server is up! Running on http://localhost:4000/graphql')
})
