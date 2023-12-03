#!/bin/sh

# Ensure all the necessary node modules are installed
npm install

# Check if NEXT_PUBLIC_PROD is set to true
if [ "$NEXT_PUBLIC_PROD" = "true" ]
then
    echo "Building for production..."
    npm run build
    echo "Starting production server..."
    npm run start
else
    echo "Starting development server..."
    npm run dev
fi
