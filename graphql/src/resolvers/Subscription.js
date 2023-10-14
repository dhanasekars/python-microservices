const Subscription = {
// todoUpdates:{
//     subscribe: (parent, { todoID }, { pubsub }, info) =>
//      pubsub.subscribe(`todoUpdates_${todoID}`)
//     },
countdown:{
    subscribe: async function* (_, { from }) {
        for (let i = from; i >= 0; i--) {
          await new Promise(resolve => setTimeout(resolve, 1000))
          yield { countdown: i }
}
}
}

// countdown:{
//     subscribe: (parent, args, { pubsub }, info) => {
//         // console.log(args.from);
//         let count = 0;
//         setInterval(() => pubsub.publish('countdown', { count: count++ }), 1000);
//         return pubsub.subscribe('countdown');
//     }
// }
}
export { Subscription as default };