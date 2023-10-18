# Use an official Node.js runtime as a parent image
FROM node:18-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD ./app /app

# Install frontend dependencies
RUN npm install

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Copy the entrypoint script into the container
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x entrypoint.sh
# Set the entrypoint script as the default command
CMD ["/entrypoint.sh"]
# Start the frontend development server
#CMD ["npm", "start-watch"]
