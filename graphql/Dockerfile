# Use an official Node.js runtime as a parent image
FROM node:18

# Set the working directory in the container
WORKDIR /graphql

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of your application code to the working directory
COPY . .

# Expose the port your GraphQL server will listen on (default is 4000)
EXPOSE 4000

# Define the command to run your GraphQL server
CMD ["node", "src/index.js"]
